import os
import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest
import socket
import shutil
import tempfile
import unittest

class TestGridFTP(osgunittest.OSGTestCase):

    __data_path = '/usr/share/osg-test/test_gridftp_data.txt'

    def test_01_copy_local_to_server(self):
        core.skip_ok_unless_installed('globus-gridftp-server-progs', 'globus-ftp-client',
                                      'globus-proxy-utils', 'globus-gass-copy-progs')

        hostname = socket.getfqdn()
        temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, 0777)
        gsiftp_url = 'gsiftp://%s%s/copied_file.txt' % (hostname, temp_dir)
        command = ('globus-url-copy', 'file://' + TestGridFTP.__data_path,
                   gsiftp_url)

        status, stdout, stderr = core.system(command, True)
        fail = core.diagnose('GridFTP copy, local to URL',
                             status, stdout, stderr)
        file_copied = os.path.exists(os.path.join(temp_dir, 'copied_file.txt'))
        shutil.rmtree(temp_dir)
        self.assertEqual(status, 0, fail)
        self.assert_(file_copied, 'Copied file missing')

    def test_02_copy_server_to_local(self):
        core.skip_ok_unless_installed('globus-gridftp-server-progs', 'globus-ftp-client',
                                      'globus-proxy-utils', 'globus-gass-copy-progs')

        hostname = socket.getfqdn()
        temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, 0777)
        gsiftp_url = 'gsiftp://' + hostname + TestGridFTP.__data_path
        local_path = temp_dir + '/copied_file.txt'
        command = ('globus-url-copy', gsiftp_url, 'file://' + local_path)

        status, stdout, stderr = core.system(command, True)
        fail = core.diagnose('GridFTP copy, URL to local',
                             status, stdout, stderr)
        file_copied = os.path.exists(local_path)
        shutil.rmtree(temp_dir)
        self.assertEqual(status, 0, fail)
        self.assert_(file_copied, 'Copied file missing')
