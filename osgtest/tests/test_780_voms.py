import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.service as service
import osgtest.library.osgunittest as osgunittest
import osgtest.library.voms as voms


class TestStopVOMS(osgunittest.OSGTestCase):

    # ==========================================================================

    def test_01_stop_voms(self):
        voms.skip_ok_unless_installed()
        self.skip_ok_unless(core.state['voms.started-server'], 'did not start server')

        service.check_stop(core.config['voms_service'])

    def test_02_restore_vomses(self):
        voms.skip_ok_unless_installed()

        voms.destroy_lsc(core.config['voms.vo'])
        files.restore('/etc/vomses', 'voms')


    def test_03_remove_vo(self):
        voms.skip_ok_unless_installed()

        if core.rpm_is_installed('voms-admin-server'):
            # Ask VOMS Admin to remove VO
            command = ('voms-admin-configure', 'remove',
                       '--vo', core.config['voms.vo'],
                       '--undeploy-database')
            stdout, _, fail = core.check_system(command, 'Remove VO')
            self.assert_('Database undeployed correctly!' in stdout, fail)
            self.assert_(' succesfully removed.' in stdout, fail)

        # Really remove database -- the voms-admin-configure command above does
        # not actually destroy the mysql database.
        voms.destroy_db(core.config['voms.vo'], core.config['voms.dbusername'])
        voms.destroy_voms_conf(core.config['voms.vo'])


    def test_04_remove_certs(self):
        core.state['voms.removed-certs'] = False
        # Do the keys first, so that the directories will be empty for the certs.
        core.remove_cert('certs.vomskey')
        core.remove_cert('certs.vomscert')
        core.remove_cert('certs.httpkey')
        core.remove_cert('certs.httpcert')
        core.state['voms.removed-certs'] = True
