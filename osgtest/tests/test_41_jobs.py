import osgtest.library.core as core
import unittest

class TestGlobusJobRun(unittest.TestCase):

    def contact_string(self, jobmanager):
        return core.get_hostname() + '/jobmanager-' + jobmanager

    def test_01_fork_job(self):
        if core.missing_rpm('globus-gatekeeper', 'globus-gram-client-tools',
                            'globus-proxy-utils', 'globus-gram-job-manager',
                            'globus-gram-job-manager-fork-setup-poll'):
            return

        
        command = ('globus-job-run', self.contact_string('fork'), '/bin/echo', 'hello')
        stdout = core.check_system(command, 'globus-job-run on fork job', user=True)[0]
        self.assertEqual(stdout, 'hello\n',
                         'Incorrect output from globus-job-run on fork job')

    def test_02_condor_job(self):
        if core.missing_rpm('globus-gram-job-manager-condor',
                            'globus-gram-client-tools', 'globus-proxy-utils'):
            return

        command = ('globus-job-run', self.contact_string('condor'), '/bin/echo', 'hello')
        stdout = core.check_system(command, 'globus-job-run on Condor job', user=True)[0]
        self.assertEqual(stdout, 'hello\n',
                         'Incorrect output from globus-job-run on Condor job')

    def test_03_pbs_job(self):
        if core.missing_rpm('globus-gram-job-manager-pbs',
                            'globus-gram-client-tools',
                            'globus-proxy-utils'):
            return

        if (not core.state['torque.pbs-configured'] or
            not core.state['torque.pbs-mom-running'] or
            not core.state['torque.pbs-server-running'] or
            not core.state['globus.pbs_configured']):
          core.skip('pbs not running or configured')
          return

        command = ('globus-job-run', self.contact_string('pbs'), '/bin/echo', 'hello')
        stdout = core.check_system(command, 'globus-job-run on PBS job', user=True)[0]
        self.assertEqual(stdout, 'hello\n',
                         'Incorrect output from globus-job-run on PBS job')
