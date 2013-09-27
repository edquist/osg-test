import os
import pwd
import unittest

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest
import osgtest.library.certificates as certs

class TestGUMS(osgunittest.OSGTestCase):

    def test_01_set_x509_env(self):
        core.skip_ok_unless_installed('gums-service', 'gums-client')

        try: 
            core.config['gums.old_x509_cert'] = os.environ['X509_USER_CERT']
        except KeyError:
            # X509_USER_CERT isn't defined
            pass

        try:
            core.config['gums.old_x509_key'] = os.environ['X509_USER_KEY']
        except KeyError:
            # X509_USER_KEY isn't defined
            pass

        os.putenv('X509_USER_CERT', '/etc/grid-security/hostcert.pem')
        os.putenv('X509_USER_KEY', '/etc/grid-security/hostkey.pem')

    def test_02_manual_group_add(self):
        core.skip_ok_unless_installed('gums-service', 'gums-client')

        core.state['gums.added_user'] = False

        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        user_dn, _ = certs.certificate_info(cert_path)
        
        command = ('gums-service', 'manualGroupAdd', 'gums-test', user_dn)
        stdout = core.check_system(command, 'Add VDT DN to manual group')[0]
        core.state['gums.added_user'] = True

    def test_03_map_user(self):
        core.skip_ok_unless_installed('gums-service', 'gums-client')
        self.skip_bad_unless(core.state['gums.added_user'] == True, 'User not added to manualUserGroup')
        
        host_dn, _ = certs.certificate_info(core.config['certs.hostcert'])
        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        user_dn, _ = certs.certificate_info(cert_path)
        command = ('gums-host', 'mapUser', user_dn) # using gums-host since it defaults to the host cert
        stdout = core.check_system(command, 'Map GUMS user')[0]
        self.assert_('GumsTestUserMappingSuccessful' in stdout)

    def test_04_unset_x509_env(self):
        core.skip_ok_unless_installed('gums-service', 'gums-client')

        try:
            os.putenv('X509_USER_CERT', core.config['gums.old_x509_cert'])
        except KeyError:
            # If the core.config value isn't there, there was no original $X509_USER_CERT
            os.unsetenv('X509_USER_CERT')

        try:
            os.putenv('X509_USER_KEY', core.config['gums.old_x509_key'])
        except KeyError:
            # If the core.config value isn't there, there was no original $X509_USER_KEY
            os.unsetenv('X509_USER_KEY')
