import os
import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest
import unittest

class TestStopXrootd(osgunittest.OSGTestCase):

    def test_01_stop_xrootd(self):
        if (core.config['xrootd.gsi'] == "ON") and (core.state['xrootd.backups-exist'] == True):
            files.restore('/etc/xrootd/xrootd-clustered.cfg',"xrootd")
            files.restore('/etc/xrootd/auth_file',"xrootd")
            files.restore('/etc/grid-security/xrd/xrdmapfile',"xrootd")
        core.skip_ok_unless_installed('xrootd')
        self.skip_ok_if(['xrootd.started-server'] == False, 'did not start server')

        command = ('service', 'xrootd', 'stop')
        stdout, _, fail = core.check_system(command, 'Stop Xrootd server')
        self.assert_(stdout.find('FAILED') == -1, fail)
        self.assert_(not os.path.exists(core.config['xrootd.pid-file']),
                     'Xrootd server PID file still present')
