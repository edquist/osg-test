import os
import pwd
import re
import shutil
import socket
import stat
import unittest

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest

class TestStartGUMS(osgunittest.OSGTestCase):

    # ==========================================================================
    # START: (MOSTLY) COPIED FROM test_20_voms.py
    # Should be refactored, but I am in a hurry!!!
    # ==========================================================================

    def check_file_and_perms(self, file_path, owner_name, permissions):
        """Return True if the file at 'file_path' exists, is owned by
        'owner_name', is a file, and has the given permissions; False otherwise

        """
        owner_uid = pwd.getpwnam(owner_name)
        try:
            file_stat = os.stat(file_path)
            return (file_stat.st_uid == owner_uid and
                    file_stat.st_mode & 07777 == permissions and
                    stat.S_ISREG(file_stat.st_mode))
        except OSError: # file does not exist
            return False


    # Carefully install a certificate with the given key from the given
    # source path, then set ownership and permissions as given.  Record
    # each directory and file created by this process into the config
    # dictionary; do so immediately after creation, so that the
    # remove_cert() function knows exactly what to remove/restore.
    def install_cert(self, target_key, source_key, owner_name, permissions):
        target_path = core.config[target_key]
        target_dir = os.path.dirname(target_path)
        source_path = core.config[source_key]
        user = pwd.getpwnam(owner_name)

        # Using os.path.lexists because os.path.exists return False for broken symlinks
        if os.path.lexists(target_path):
            backup_path = target_path + '.osgtest.backup'
            shutil.move(target_path, backup_path)
            core.state[target_key + '-backup'] = backup_path

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            core.state[target_key + '-dir'] = target_dir
            os.chown(target_dir, user.pw_uid, user.pw_gid)
            os.chmod(target_dir, 0755)

        shutil.copy(source_path, target_path)
        core.state[target_key] = target_path
        os.chown(target_path, user.pw_uid, user.pw_gid)
        os.chmod(target_path, permissions)

    def test_01_config_certs(self):
        core.config['certs.hostcert'] = '/etc/grid-security/hostcert.pem'
        core.config['certs.hostkey'] = '/etc/grid-security/hostkey.pem'
        core.config['certs.httpcert'] = '/etc/grid-security/http/httpcert.pem'
        core.config['certs.httpkey'] = '/etc/grid-security/http/httpkey.pem'

    def test_02_install_http_certs(self):
        core.skip_ok_unless_installed('gums-service')
        httpcert = core.config['certs.httpcert']
        httpkey = core.config['certs.httpkey']
        self.skip_ok_if(self.check_file_and_perms(httpcert, 'tomcat', 0644) and
                        self.check_file_and_perms(httpkey, 'tomcat', 0400),
                        'HTTP cert exists and has proper permissions')
        self.install_cert('certs.httpcert', 'certs.hostcert', 'tomcat', 0644)
        self.install_cert('certs.httpkey', 'certs.hostkey', 'tomcat', 0400)

    # ==========================================================================
    # END: (MOSTLY) COPIED FROM test_20_voms.py
    # ==========================================================================

    def test_03_gums_configuration(self):
        core.config['gums.password'] = 'osgGUMS!'

    def test_04_gums_cert_symlinks(self):
        core.skip_ok_unless_installed('gums-service')

        # gums-service expects a cert in /root/.globus/ for the admin added in test_05
        root_pwd = pwd.getpwnam('root')
        core.config['gums.certdir'] = os.path.join(root_pwd.pw_dir, '.globus')
        core.config['gums.backup-certdir'] = core.config['gums.certdir'] + '.gums'
        self.assert_(os.path.exists(core.config['gums.backup-certdir']) == False, 'Backup dir already exists')
        try:
            shutil.move(core.config['gums.certdir'], core.config['gums.backup-certdir'])
        except IOError as e:
            if e.errno == 2:
                # suppress no such file or directory error
                pass
            else:
                raise

        # Create links to hostcert since we added it as an admin in test_05 
        os.mkdir(core.config['gums.certdir'])
        cert_link_path = os.path.join(core.config['gums.certdir'], 'usercert.pem')
        key_link_path = os.path.join(core.config['gums.certdir'], 'userkey.pem')
        os.symlink(core.config['certs.hostcert'], cert_link_path)
        os.symlink(core.config['certs.hostkey'], key_link_path)

    def test_05_setup_gums_database(self):
        core.skip_ok_unless_installed('gums-service')
        command = ('gums-setup-mysql-database', '--noprompt', '--user', 'gums', '--host', 'localhost:3306',
                   '--password', core.config['gums.password'])
        stdout = core.check_system(command, 'Set up GUMS MySQL database')[0]
        self.assert_('ERROR' not in stdout,
                     'gums-setup-mysql-database failure message')

    def test_06_add_mysql_admin(self):
        core.skip_ok_unless_installed('gums-service')
        host_dn, host_issuer = core.certificate_info(core.config['certs.hostcert'])
        mysql_template_path = '/usr/lib/gums/sql/addAdmin.mysql'
        self.assert_(os.path.exists(mysql_template_path), 'GUMS MySQL template exists')
        mysql_template = files.read(mysql_template_path, as_single_string=True).strip()
        core.log_message(mysql_template)

        mysql_command = re.sub(r'@ADMINDN@', host_dn, mysql_template)
        core.log_message(mysql_command)

        command = ('mysql', '--user=gums', '-p' + core.config['gums.password'], '--execute=' + mysql_command)
        core.check_system(command, 'Could not add GUMS MySQL admin')

