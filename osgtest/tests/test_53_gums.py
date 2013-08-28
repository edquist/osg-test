import os
import pwd
import unittest

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.tomcat as tomcat
import osgtest.library.osgunittest as osgunittest

class TestGUMS(osgunittest.OSGTestCase):

    def test_01_manual_group_add(self):
        core.skip_ok_unless_installed('gums-service')

        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        user_dn, _ = core.certificate_info(cert_path)
        command = ('gums-service', 'manualGroupAdd', 'gums-test', user_dn)
        stdout = core.check_system(command, 'Add VDT DN to manual group')[0]
        
    def test_02_map_user(self):
        core.skip_ok_unless_installed('gums-service')

        host_dn, _ = core.certificate_info(core.config['certs.hostcert'])
        pwd_entry = pwd.getpwnam(core.options.username)
        cert_path = os.path.join(pwd_entry.pw_dir, '.globus', 'usercert.pem')
        user_dn, _ = core.certificate_info(cert_path)
        command = ('gums-host', 'mapUser', '-d', user_dn)
        stdout = core.check_system(command, 'Map GUMS user')[0]
        self.assert_('null' not in stdout,
                     'User mapping returned null')
