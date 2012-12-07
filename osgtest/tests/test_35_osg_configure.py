import os, re, unittest, sys, cStringIO

import osgtest.library.core as core
import osgtest.library.files as files


class TestOSGConfigure(unittest.TestCase):

    required_rpms = ['osg-configure',
                     'osg-configure-tests']

    pathname = os.path.realpath('/usr/share/osg-configure/tests')

    def setUp(self):
        "setup system library path"
        cls = self.__class__
        if cls.pathname not in sys.path:
            sys.path.insert(0, cls.pathname)

    def test_01_version(self):
        if core.missing_rpm(*self.required_rpms):
            return
        command = ('osg-configure', '--version')
        stdout = core.check_system(command, 'osg-configure version check')[0]
        self.assert_(re.search('osg-configure \d+\.\d+\.\d+', 
                               stdout,
                               re.IGNORECASE)
                     is not None)

    def __run_unit_tests(self, test_case):
      """
      Runs a test suite and returns any error messages or failures
      """
      test_suite = unittest.TestSuite()
      test_suite.addTests(unittest.makeSuite(test_case))
      output = cStringIO.StringIO()
      result = unittest.TextTestRunner(stream=output, verbosity=2).run(test_suite)
      core.log_message(output.getvalue())
      output.close()
      if not result.wasSuccessful():
          error_message = "Encountered problems while running osg_configure unit tests (%s):\n" % type(test_case).__name__
          if result.errors != []:
              error_message = "Encountered the following errors: \n"
              for error in result.errors:
                  error_message = "%s:\n %s\n" % (error[0], error[1])
          if result.failures != []:
              error_message = "Encountered the following failures: \n"
              for failure in result.failures:
                  error_message = "%s:\n %s\n" % (failure[0], failure[1])

          return error_message
      return None
    
    
    def test_02_cemon(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.missing_rpm('osg-ce'):
            return
        try:
            import test_cemon
            mesg = self.__run_unit_tests(test_cemon.TestCEMon)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import cemon unit test: " + str(e))

    def test_03_condor(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
          import test_condor
          mesg = self.__run_unit_tests(test_condor.TestCondor)
          if mesg is not None:
            self.fail(mesg)
        except ImportError, e:
          self.fail("Can't import condor unit test: " + str(e))

    def test_04_configfile(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_configfile
            mesg = self.__run_unit_tests(test_configfile.TestConfigFile)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import configfile unit test: " + str(e))

    def test_05_gip(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.missing_rpm('osg-ce'):
            return
        try:
            import test_gip
            mesg = self.__run_unit_tests(test_gip.TestGip)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import gip unit test: " + str(e))

    def test_06_gratia(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.missing_rpm('osg-ce'):
            return
        try:
            import test_gratia
            mesg = self.__run_unit_tests(test_gratia.TestGratia)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import gratia unit test: " + str(e))

    def test_07_local_settings(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_local_settings
            mesg = self.__run_unit_tests(test_local_settings.TestLocalSettings)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import local settings unit test: " + str(e))

    def test_08_lsf(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_lsf
            mesg = self.__run_unit_tests(test_lsf.TestLSF)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import lsf unit test: " + str(e))

    def test_09_managedfork(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_managedfork
            mesg = self.__run_unit_tests(test_managedfork.TestManagedFork)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import managed fork unit test: " + str(e))

    def test_10_misc(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_misc
            mesg = self.__run_unit_tests(test_misc.TestMisc)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import misc unit test: " + str(e))

    def test_11_monalisa(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_monalisa
            mesg = self.__run_unit_tests(test_monalisa.TestMonalisa)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import monalisa unit test: " + str(e))

    def test_12_network(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_network
            mesg = self.__run_unit_tests(test_network.TestNetwork)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import network unit test: " + str(e))

    def test_13_pbs(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_pbs
            mesg = self.__run_unit_tests(test_pbs.TestPBS)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import pbs unit test: " + str(e))

    def test_14_rsv(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.missing_rpm('rsv-core'):
            return
        try:
            import test_rsv
            mesg = self.__run_unit_tests(test_rsv.TestRSV)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import rsv unit test: " + str(e))

    def test_15_sge(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_sge
            mesg = self.__run_unit_tests(test_sge.TestSGE)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import sge unit test: " + str(e))

    def test_16_siteattributes(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_siteattributes
            mesg = self.__run_unit_tests(test_siteattributes.TestSiteAttributes)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import site attributes unit test: " + str(e))

    def test_17_squid(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_squid
            mesg = self.__run_unit_tests(test_squid.TestSquid)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import squid unit test: " + str(e))

    def test_18_storage(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.missing_rpm('osg-ce'):
            return
        try:
            import test_storage
            if not os.path.exists('/tmp/etc'):
                os.mkdir('/tmp/etc')
                os.chmod('/tmp/etc', 0777)
            mesg = self.__run_unit_tests(test_storage.TestStorage)
            if mesg is not None:
                self.fail(mesg)
            os.rmdir('/tmp/etc')
        except ImportError, e:
            self.fail("Can't import storage unit test: " + str(e))

    def test_19_utilities(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_utilities
            mesg = self.__run_unit_tests(test_utilities.TestUtilities)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
          self.fail("Can't import utilities unit test: " + str(e))

    def test_20_validation(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_validation
            mesg = self.__run_unit_tests(test_validation.TestValidation)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import validation unit test: " + str(e))

    def test_21_xml_utilities(self):
        if core.missing_rpm(*self.required_rpms):
            return
        try:
            import test_xml_utilities
            mesg = self.__run_unit_tests(test_xml_utilities.TestXMLUtilities)
            if mesg is not None:
                self.fail(mesg)
        except ImportError, e:
            self.fail("Can't import xml_utilities unit test: " + str(e))

