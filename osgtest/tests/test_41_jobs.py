import osgtest.library.core as core
import unittest

class TestGlobusJobRun(unittest.TestCase):

    def test_01_fork_job(self):
        if core.missing_rpm('globus-gatekeeper', 'globus-gram-client-tools',
                            'globus-proxy-utils', 'globus-gram-job-manager',
                            'globus-gram-job-manager-fork-setup-poll'):
            return

        command = ('globus-job-run', 'localhost/jobmanager-fork', '/bin/echo',
                   'hello')
        stdout = core.check_system(command, 'globus-job-run on fork job')[0]
        self.assertEqual(stdout, 'hello\n',
                         'Incorrect output from globus-job-run on fork job')

    def test_02_condor_job(self):
        if core.missing_rpm('globus-gram-job-manager-condor',
                            'globus-gram-client-tools', 'globus-proxy-utils'):
            return

        command = ('globus-job-run', 'localhost/jobmanager-condor',
                   '/bin/echo', 'hello')
        stdout = core.check_system(command, 'globus-job-run on Condor job')[0]
        self.assertEqual(stdout, 'hello\n',
                         'Incorrect output from globus-job-run on Condor job')