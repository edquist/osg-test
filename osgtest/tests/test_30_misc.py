import osgtest.library.core as core
import re
import unittest

class TestMisc(unittest.TestCase):

    def test_01_web100clt(self):
        if core.missing_rpm('ndt'):
            return
        command = ('web100clt', '-v')
        stdout = core.check_system(command, 'NDT client')[0]
        self.assert_(re.search('ndt.+version', stdout, re.IGNORECASE)
                     is not None)

    def test_02_osg_version(self):
        if core.missing_rpm('osg-version'):
            return
        command = ('osg-version',)
        
        # First we verify that osg-version runs
        stdout = core.check_system(command, 'osg-version')[0]
        
        # Then we pull out the version number from the output
        version_pattern = re.compile(r'(\d+\.\d+\.\d+)')
        matches = version_pattern.search(stdout)

        # Is there a version number?
        self.assert_(matches is not None)
        osg_version = matches.group(1)

        # Get the version number from the RPM
        command = ('rpm', '-q', 'osg-version')
        stdout = core.check_system(command, "osg-version RPM version")[0]
        matches = version_pattern.search(stdout)
        self.assert_(matches is not None)

        # Verify that the versions match
        osg_version_rpm_version = matches.group(1)
        self.assert_(osg_version == osg_version_rpm_version)
        
    def test_03_lfc_multilib(self):
        if core.missing_rpm('yum-utils'):
            return

        # We can't test this on 32-bit
        uname_out, _, _ = core.check_system(['uname', '-i'], 'getting arch')
        if re.search(r'i\d86', uname_out):
            core.skip('running on 32-bit')
            return

        cmdbase = ['repoquery', '--plugins']
        for repo in core.options.extrarepos:
            cmdbase.append('--enablerepo=%s' % repo)

        # Find the 32-bit lfc-python rpm
        stdout, _, _ = core.check_system(cmdbase + ['lfc-python.i386'], 'lfc-python multilib (32bit)')
        if stdout.strip() == '':
            self.fail('32-bit lfc-python not found in 64-bit repo')

        # Sanity check: find the 64-bit lfc-python rpm
        stdout, _, _ = core.check_system(cmdbase + ['lfc-python.x86_64'], 'lfc-python multilib (64bit)')
        if stdout.strip() == '':
            self.fail('64-bit lfc-python not found in 64-bit repo')

        # Find the 32-bit lfc-python26 rpm (on el5 only)
        if core.el_release() == 5:
            stdout, _, _ = core.check_system(cmdbase + ['lfc-python26.i386'], 'lfc-python26 multilib (32bit)')
            if stdout.strip() == '':
                self.fail('32-bit lfc-python not found in 64-bit repo')

            # Sanity check: find the 64-bit lfc-python26 rpm
            stdout, _, _ = core.check_system(cmdbase + ['lfc-python26.x86_64'], 'lfc-python26 multilib (64bit)')
            if stdout.strip() == '':
                self.fail('64-bit lfc-python not found in 64-bit repo')
            
        
