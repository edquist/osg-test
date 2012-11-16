import os
import osgtest.library.core as core
import osgtest.library.files as files
import socket
import shutil
import tempfile
import unittest
import pwd


class TestXrootd(unittest.TestCase):

    __data_path = '/usr/share/osg-test/test_gridftp_data.txt'
    __fuse_path = '/mnt/xrootd_fuse_test'

    def test_01_xrdcp_local_to_server(self):
        if core.missing_rpm('xrootd-server', 'xrootd-client'):
            return

        hostname = socket.getfqdn()
        if core.config['xrootd.gsi'] == "ON":
            temp_dir="/tmp/vdttest"
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
                user = pwd.getpwnam('vdttest')
                os.chown(temp_dir, user[2], user[3])
        else:
            temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, 0777)
        xrootd_url = 'root://%s/%s/copied_file.txt' % (hostname, temp_dir)
        command = ('xrdcp', TestXrootd.__data_path , xrootd_url)

        status, stdout, stderr = core.system(command, True)

        fail = core.diagnose('xrdcp copy, local to URL',
                             status, stdout, stderr)
        file_copied = os.path.exists(os.path.join(temp_dir, 'copied_file.txt'))
        shutil.rmtree(temp_dir)
        self.assertEqual(status, 0, fail)
        self.assert_(file_copied, 'Copied file missing')

    def test_02_xrdcp_server_to_local(self):
        if core.missing_rpm('xrootd-server', 'xrootd-client'):
            return

        hostname = socket.getfqdn()
        temp_source_dir = tempfile.mkdtemp()
        temp_target_dir = tempfile.mkdtemp()
        os.chmod(temp_source_dir, 0777)
        os.chmod(temp_target_dir, 0777)
        f=open(temp_source_dir+"/copied_file.txt","w")
        f.write("This is some test data for an xrootd test.")
        f.close()
        xrootd_url = 'root://%s/%s/copied_file.txt' % (hostname, temp_source_dir)
        local_path = temp_target_dir + '/copied_file.txt'
        command = ('xrdcp', xrootd_url, local_path)

        status, stdout, stderr = core.system(command, True)
        
        fail = core.diagnose('Xrootd xrdcp copy, URL to local',
                             status, stdout, stderr)
        file_copied = os.path.exists(local_path)
        shutil.rmtree(temp_source_dir)
        shutil.rmtree(temp_target_dir)
        self.assertEqual(status, 0, fail)
        self.assert_(file_copied, 'Copied file missing')

    def test_03_xrootd_fuse(self):
        # This tests xrootd-fuse using a mount in /mnt 
        if core.missing_rpm('xrootd-server', 'xrootd-client','xrootd-fuse'):
            return
        if not os.path.exists("/mnt"):
            core.log_message("/mnt did not exist, skipping xrootd fuse test")
            return
        if not os.path.exists(TestXrootd.__fuse_path):
            os.mkdir(TestXrootd.__fuse_path)
        if core.config['xrootd.gsi'] == "ON":
            core.log_message("fuse incompatible with GSI, skipping xrootd fuse")
            return
        hostname = socket.getfqdn()
        #command = ('xrootdfs',TestXrootd.__fuse_path,'-o','rdr=xroot://localhost:1094//tmp','-o','uid=xrootd')
        command = ('mount', '-t','fuse','-o','rdr=xroot://localhost:1094//tmp,uid=xrootd','xrootdfs',TestXrootd.__fuse_path)
        command_str= ' '.join(command)

        #For some reason, sub process hangs on fuse processes, use os.system
        #status, stdout, stderr = core.system(command_str,shell=True)
        os.system(command_str)
       
        # Copy a file in and see if it made it into the fuse mount
        xrootd_url = 'root://%s/%s/copied_file.txt' % (hostname, "/tmp")
        command = ('xrdcp', TestXrootd.__data_path , xrootd_url)
        status, stdout, stderr = core.system(command, True)
       
        command = ('ls', "/tmp/copied_file.txt")
        stdout, stderr, fail = core.check_system(command, "Checking file is copied to xrootd fuse mount correctly", user=True)


        command = ('umount',TestXrootd.__fuse_path)
        status, stdout, stderr = core.system(command)
        os.rmdir(TestXrootd.__fuse_path)
        files.remove("/tmp/copied_file.txt")



