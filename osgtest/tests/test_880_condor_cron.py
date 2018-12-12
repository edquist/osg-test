import osgtest.library.core as core
import osgtest.library.osgunittest as osgunittest
import osgtest.library.service as service

class TestStopCondorCron(osgunittest.OSGTestCase):
    def test_01_stop_condor_cron(self):
        core.skip_ok_unless_installed('condor-cron')
        self.skip_ok_if(core.state['condor-cron.started-service'] == False, 'did not start server')
        service.check_stop('condor-cron')
        core.state['condor-cron.running-service'] = False
