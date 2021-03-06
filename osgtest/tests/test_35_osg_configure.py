import os
import re
import unittest
import sys
import cStringIO

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest

class TestOSGConfigure(osgunittest.OSGTestCase):

    required_rpms = ['osg-configure',
                     'osg-configure-tests']
    required_rpms_ce = required_rpms + ['osg-ce']

    pathname = os.path.realpath('/usr/share/osg-configure/tests')
    sys_path_saved = None

    def test_00_setup(self):
        cls = self.__class__
        if cls.pathname not in sys.path:
            cls.sys_path_saved = list(sys.path)
            sys.path.insert(0, cls.pathname)

    def test_01_version(self):
        core.skip_ok_unless_installed(*self.required_rpms)
        command = ('osg-configure', '--version')
        stdout = core.check_system(command, 'osg-configure version check')[0]
        self.assert_(re.search('osg-configure \d+\.\d+\.\d+', 
                               stdout,
                               re.IGNORECASE)
                     is not None)

    def test_02_run_unit_tests(self):
        core.skip_ok_unless_installed(*self.required_rpms)
        if core.rpm_is_installed('rsv-core'):
            command = ('/usr/share/osg-configure/tests/run-osg-configure-tests',)
        else:
            command = ('/usr/share/osg-configure/tests/run-osg-configure-tests', '--exclude-test', 'test_rsv')
        
        status, stdout, stderr = core.system(command, 'run osg-configure unit tests')
        if status != 0:
            clean_output = re.sub(r'Ran \d+.*', '', stdout) # scrub output for the sake of reporting (SOFTWARE-1818)
            fail_msg = core.diagnose('osg-configure unit tests failed', command, status, clean_output, stderr)
            self.fail(fail_msg)

