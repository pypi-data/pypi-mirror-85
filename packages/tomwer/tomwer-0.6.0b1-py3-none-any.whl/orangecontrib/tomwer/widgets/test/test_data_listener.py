# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "17/03/2020"


import logging
import unittest
import tempfile
import shutil
import time
import os
from silx.gui import qt
from tomwer.core.utils import ignoreLowMemory
from tomwer.core import settings
from orangecontrib.tomwer.widgets.control.DataListenerOW import DataListenerOW
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import UtilsTest
from tomwer.synctools.datalistener import _mock_acquisition_info
from silx.gui.utils.testutils import TestCaseQt
from silx.gui.utils.testutils import SignalListener
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test


logging.disable(logging.INFO)


@unittest.skip("Need re-work")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestDataListener(TestCaseQt):
    """Test the DataListener Orange Widget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._src_dir = tempfile.mkdtemp()
        nxtomomill_file = "tomo_v2_external.h5"
        nxtomomill_folder = os.path.join(self._src_dir, "tomo_v2")
        os.mkdir(nxtomomill_folder)
        self.nxtomomill_file = os.path.join(nxtomomill_folder, nxtomomill_file)
        shutil.copyfile(
            src=UtilsTest.getH5Dataset(folderID=nxtomomill_file),
            dst=self.nxtomomill_file,
        )

        self.widget = DataListenerOW(parent=None)
        scan_numbers = ["426.1", "427.1", "428.1", "429.1", "430.1", "431.1"]
        self.widget.setMock(
            mock=True,
            acquisitions=(
                _mock_acquisition_info(
                    master_file=self.nxtomomill_file,
                    entry="425.1",
                    waiting_time=0.1,
                    scan_numbers=scan_numbers,
                ),
            ),
        )
        self.nx_file = os.path.join(nxtomomill_folder, "tomo_v2_external_425_1.nx")
        assert not os.path.exists(self.nx_file)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        del self.widget
        self.widget = None
        self.qapp.processEvents()
        shutil.rmtree(self._src_dir)
        TestCaseQt.tearDown(self)

    def test(self):
        self.widget.activate()
        self.widget.show()
        self.qapp.processEvents()
        # check observation is on going
        time.sleep(0.2)
        self.qapp.processEvents()
        self.assertEqual(self.widget._get_n_scan_observe(), 1)
        self.assertEqual(self.widget._get_n_scan_finished(), 0)

        self.qapp.processEvents()
        time.sleep(1.2)
        self.qapp.processEvents()
        # check acquisition is moved to 'finished'
        self.assertEqual(self.widget._get_n_scan_observe(), 0)
        self.assertEqual(self.widget._get_n_scan_finished(), 1)

        self.qapp.processEvents()
        time.sleep(0.2)
        self.qapp.processEvents()
        # check conversion has been made
        self.assertTrue(os.path.exists(self.nx_file))


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
class TestListenerToTransfert(OrangeWorflowTest):
    """class testing the following flow:

    - data listener
    - dark and flat field construction
    - nabu reconstruction
    - data validator
    - data transfert

    This test conversion from bliss .hdf5 to tomonx .nx file then a 'classical'
    workflow
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets

        cls.dataListenerNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListenerOW.DataListenerOW"
        )
        cls.dkrfNode = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW",
        )
        cls.nabuNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuOW.NabuOW"
        )
        cls.dataValidatorNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataValidatorOW.DataValidatorOW"
        )
        cls.dataTransfertNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataTransfertOW.DataTransfertOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.dataListenerNode, "data", cls.dkrfNode, "data")
        cls.link(cls, cls.dkrfNode, "data", cls.nabuNode, "data")
        cls.link(cls, cls.nabuNode, "data", cls.dataValidatorNode, "data")
        cls.link(cls, cls.dataValidatorNode, "data", cls.dataTransfertNode, "data")
        cls.link(
            cls,
            cls.dataValidatorNode,
            "change recons params",
            cls.nabuNode,
            "change recons params",
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.dataListenerWidget = cls.getWidgetForNode(cls, cls.dataListenerNode)
        cls.dkrfWidget = cls.getWidgetForNode(cls, cls.dkrfNode)
        cls.nabuWidget = cls.getWidgetForNode(cls, cls.nabuNode)
        cls.dataValidatorWidget = cls.getWidgetForNode(cls, cls.dataValidatorNode)
        cls.dataTransfertWidget = cls.getWidgetForNode(cls, cls.dataTransfertNode)

        cls.processOrangeEvents(cls)

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        # source directory
        self._src_dir = tempfile.mkdtemp()
        # destination dir
        self._dst_dir = tempfile.mkdtemp()
        settings._set_lbsram_path(self._src_dir)
        settings._set_dest_path(self._dst_dir)

        self._folder_tomo_v2 = os.path.join(self._src_dir, "tomo_v2")
        o_dataset = UtilsTest.getH5Dataset(folderID="tomo_v2")
        shutil.copytree(o_dataset, os.path.join(self._src_dir, "tomo_v2"))
        self.bliss_file = os.path.join(self._src_dir, "tomo_v2", "tomo_v2_external.h5")
        self.final_dest_dir = os.path.join(self._dst_dir, "tomo_v2")

        # warm widget that this is for CI
        self.dkrfWidget.setForceSync(True)
        self.nabuWidget.setDryRun(True)
        # define the acquisition to mock
        scan_numbers = ["426.1", "427.1", "428.1", "429.1", "430.1", "431.1"]
        self.dataListenerWidget.setMock(
            mock=True,
            acquisitions=(
                _mock_acquisition_info(
                    master_file=self.bliss_file,
                    entry="425.1",
                    waiting_time=0.1,
                    scan_numbers=scan_numbers,
                ),
            ),
        )
        self.nx_file = os.path.join(
            self._src_dir, "tomo_v2", "tomo_v2_external_425_1.nx"
        )

        # mock lbsram
        settings.mock_lsbram(True)
        settings._set_lbsram_path(self._src_dir)
        settings._set_dest_path(self._dst_dir)

        # create signal listener
        self._dataTransfertListener = SignalListener()
        self.dataTransfertWidget.scanready.connect(self._dataTransfertListener)
        self.dataTransfertWidget.setForceSync(True)
        ignoreLowMemory(True)

    @classmethod
    def tearDownClass(cls):
        for node in (
            cls.dataListenerNode,
            cls.dkrfNode,
            cls.nabuNode,
            cls.dataValidatorNode,
            cls.dataTransfertNode,
        ):
            cls.removeNode(cls, node)
        cls.dataListenerWidget = None
        cls.dkrfWidget = None
        cls.nabuWidget = None
        cls.dataValidatorWidget = None
        cls.dataTransfertWidget = None
        OrangeWorflowTest.tearDownClass()

    def tearDown(self):
        self.nabuWidget.settingsHandler.removeCallback(
            self.nabuWidget._updateSettingsVals
        )
        self.dataListenerWidget.activate(False)
        # reset default configuration
        ignoreLowMemory(False)
        if os.path.exists(self._src_dir):
            shutil.rmtree(self._src_dir)
        if os.path.exists(self._dst_dir):
            shutil.rmtree(self._dst_dir)
        settings._set_lbsram_path("/lbsram")
        settings._set_dest_path("")

        OrangeWorflowTest.tearDown(self)

    def testFlow(self):
        """
        Make sure all possibles input are managed and processed from one
        widget to the others
        """
        self.assertFalse(os.path.exists(self.final_dest_dir))
        self.process_datalistener()

        # check that synchronization has been done
        self.assertTrue(os.path.exists(self.final_dest_dir))
        self.wait_and_process_datavalidator()
        # make sure everything has been processed
        for i in range(20):
            time.sleep(0.02)
            self.qapp.processEvents()

        # validate the current scan
        self.dataValidatorWidget.validateCurrentScan()
        self.check_data_transfert()

    def process_datalistener(self):
        self.dataListenerWidget.activate()
        self.dataListenerWidget.show()
        self.qapp.processEvents()
        # check observation is on going
        time.sleep(0.2)
        self.qapp.processEvents()
        self.assertEqual(self.dataListenerWidget._get_n_scan_observe(), 1)
        self.assertEqual(self.dataListenerWidget._get_n_scan_finished(), 0)

        self.qapp.processEvents()
        time.sleep(1.2)
        self.qapp.processEvents()
        # check acquisition is moved to 'finished'
        self.assertEqual(self.dataListenerWidget._get_n_scan_observe(), 0)
        self.assertEqual(self.dataListenerWidget._get_n_scan_finished(), 1)

        self.qapp.processEvents()
        time.sleep(0.2)
        self.qapp.processEvents()
        # check conversion has been made
        self.assertTrue(os.path.exists(self.nx_file))

    def wait_and_process_datavalidator(self):
        def wait():
            timeout = 4
            while len(self.dataValidatorWidget._scansToValidate) and timeout >= 0:
                time.sleep(0.05)
                timeout -= 0.05

            if timeout < 0:
                raise TimeoutError("data validator never received a scan")

        wait()
        self.dataValidatorWidget.show()

    def check_data_transfert(self):
        timeout = 20
        while (self._dataTransfertListener.callCount() == 0) and timeout >= 0:
            time.sleep(0.05)
            timeout -= 0.05
            self.qapp.processEvents()

        if timeout < 0:
            raise TimeoutError("Data transfert was never processed")


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestListenerToTransfert, TestDataListener):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
