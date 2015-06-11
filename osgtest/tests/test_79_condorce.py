import os
import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest

class TestStopCondorCE(osgunittest.OSGTestCase):
    def test_01_stop_condorce(self):
        core.skip_ok_unless_installed('condor', 'htcondor-ce', 'htcondor-ce-client', 'htcondor-ce-condor')
        self.skip_ok_unless(core.state['condor-ce.started'], 'did not start server')

        command = ('service', 'condor-ce', 'stop')
        stdout, _, fail = core.check_system(command, 'Stop HTCondor CE')
        self.assert_(stdout.find('FAILED') == -1, fail)
        self.assert_(not os.path.exists(core.config['condor-ce.lockfile']),
                     'HTCondor CE run lock file exists')

    def test_02_restore_config(self):
        core.skip_ok_unless_installed('condor', 'htcondor-ce', 'htcondor-ce-client', 'htcondor-ce-condor')        

        if core.rpm_is_installed('gums-service'):
            files.restore(core.config['condor-ce.lcmapsdb'], 'condor-ce.gums')
            files.restore(core.config['condor-ce.gsi-authz'], 'condor-ce')
            files.restore(core.config['condor-ce.gums-properties'], 'condor-ce')
        files.restore(core.config['condor-ce.condor-cfg'], 'condor-ce')
        files.restore(core.config['condor-ce.condor-ce-cfg'], 'condor-ce')
        files.restore(core.config['condor-ce.lcmapsdb'], 'condor-ce')
