# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
__date__ = "03/05/2019"


from orangecontrib.tomwer.widgets.reconstruction.AxisOW import AxisOW
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from tomwer.test.utils import UtilsTest
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.settings import mock_lsbram
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core import utils
from tomwer.core.utils.scanutils import MockEDF, MockHDF5
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
import numpy
import shutil
import tempfile
import unittest
import time
import os


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestOWAxis(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self._window = AxisOW()
        self.recons_params = self._window.recons_params
        self.scan_path = UtilsTest.getEDFDataset("D2_H2_T2_h_")
        self._window.getAxis().mode = AxisMode.centered
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()

    def testAxisLock(self):
        """Test behavior when locking the axis position. Could not be included
        in the tomwer/gui because the lock action is only available for the OW
        """
        assert self._window.getAxis().mode in (AxisMode.centered, AxisMode.global_)
        radio_axis = self._window._widget._axisWidget._radioAxis
        main_widget = self._window._widget._axisWidget
        self.assertFalse(main_widget._controlWidget._lockBut.isLocked())
        self.assertTrue(radio_axis._controlWidget._mainWidget.isEnabled())
        self.mouseClick(main_widget._controlWidget._lockBut, qt.Qt.LeftButton)
        self.qapp.processEvents()
        self.assertTrue(main_widget._controlWidget._lockBut.isLocked())
        # when the lock button is activated we should automatically switch to
        # the manual mode
        self.assertTrue(self._window.getAxis().mode is AxisMode.manual)
        self.assertFalse(radio_axis._controlWidget._mainWidget.isEnabled())


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestWindowAxisComputation(TestCaseQt):
    @staticmethod
    def _long_computation(scan):
        time.sleep(5)
        return -1

    """Test that the axis widget work correctly"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow.recons_params
        self._window = self._mainWindow._widget
        self.scan_path = ScanFactory.create_scan_object(
            UtilsTest.getEDFDataset("D2_H2_T2_h_")
        )
        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)

    def tearDown(self):
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._window = None
        TestCaseQt.tearDown(self)

    def testFailedComputation(self):
        """Test gui if the axis position fails"""
        self.qapp.processEvents()
        self.recons_params.set_position_frm_par_file("not existing", force=True)
        self.assertEqual(self.recons_params.mode, AxisMode.read)
        radio_axis = self._window._axisWidget._radioAxis
        self.assertEqual(radio_axis.getMode(), AxisMode.read)
        self._mainWindow.process(self.scan_path)
        self.assertEqual(radio_axis.getMode(), AxisMode.read)
        self.assertEqual(self.recons_params.value_ref_tomwer, None)
        self.assertEqual(self.recons_params.mode, AxisMode.read)
        position_info_widget = self._window._axisWidget._controlWidget._positionInfo
        self.assertEqual(position_info_widget._tomwerPositionLabel.text(), "?")

    def testLongComputation(self):
        """Test behavior if some time consuming axis computation is made"""
        # monkey patch the method used
        radioAxis = self._mainWindow._widget._axisWidget._radioAxis
        self._mainWindow._processingStack._computationThread.patch_calc_method(
            AxisMode.centered, TestWindowAxisComputation._long_computation
        )
        self.recons_params.mode = AxisMode.centered
        self.qapp.processEvents()
        self.assertTrue(radioAxis.getMode() == AxisMode.centered)
        self._mainWindow.process(self.scan_path)
        self.qapp.processEvents()
        # need the data to be loaded from thread and the cor calculation thread
        # to be launch
        time.sleep(0.5)
        self.qapp.processEvents()
        self.assertFalse(radioAxis._controlWidget._mainWidget.isEnabled())
        position_info_widget = self._window._axisWidget._controlWidget._positionInfo
        # self.assertEqual(position_info_widget._positionLabel.text(),
        #                  '...')

        # then wait for the computation end
        self._mainWindow._processingStack.wait_computation_finished()
        self.qapp.processEvents()
        time.sleep(0.5)
        self.qapp.processEvents()

        # check result is correctly computed
        radio_axis = self._window._axisWidget._radioAxis
        self.assertTrue(radio_axis._controlWidget._mainWidget.isEnabled())
        res = position_info_widget._tomwerPositionLabel.text()
        self.assertTrue(float(res) == -1.0)
        self.assertTrue(self.recons_params.value_ref_tomwer, -1.0)

    def testComputationSucceed(self):
        """Test gui if the axis position is correctly computed"""
        self.recons_params.mode = AxisMode.manual
        self.recons_params.set_value_ref_tomwer(2.345)
        self._mainWindow.process(self.scan_path)
        self.qapp.processEvents()
        radio_axis = self._window._axisWidget._radioAxis
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        self.assertEqual(self.recons_params.value_ref_tomwer, 2.345)
        position_info_widget = self._window._axisWidget._controlWidget._positionInfo
        self.assertEqual(position_info_widget._tomwerPositionLabel.text(), "2.345")


global _computation_res
_computation_res = 0


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestAxisStack(TestCaseQt):
    """Test axis computation of a stack of scan"""

    @staticmethod
    def _test_computation(scan):
        global _computation_res
        _computation_res += 1
        return _computation_res

    def setUp(self):
        # not working due to OW
        TestCaseQt.setUp(self)
        self._scan1 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan2 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan3 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow._axis_params
        self._mainWindow._skip_exec(True)

        global _computation_res
        _computation_res = 0

        self._mainWindow.patch_calc_method(
            AxisMode.centered, TestAxisStack._test_computation
        )
        self.recons_params.mode = AxisMode.centered

        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)

    def tearDown(self):
        for scan in (self._scan1, self._scan2, self._scan3):
            shutil.rmtree(scan.path)
        utils.mockLowMemory(False)
        mock_lsbram(False)
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._recons_params = None
        self.qapp.processEvents()
        # not working due to OW
        TestCaseQt.tearDown(self)

    def testLowMemory(self):
        """Make sure the axis computation will be skip if we are in low memory"""
        utils.mockLowMemory(True)
        mock_lsbram(True)
        for scan in (self._scan1, self._scan2, self._scan3):
            self.qapp.processEvents()
            self._mainWindow.new_data_in(scan)

        self.assertEqual(self._scan1.axis_params, None)
        self.assertEqual(self._scan2.axis_params, None)
        self.assertEqual(self._scan3.axis_params, None)

    def testUnlockStack(self):
        """Check that all axis position will be computed properly if we set a
        stack of scan"""
        self._mainWindow.recons_params.set_value_ref_tomwer(1.0)
        for scan in (self._scan1, self._scan2, self._scan3):
            self._mainWindow.process(scan)

        for i in range(5):
            self.qapp.processEvents()
            time.sleep(0.2)
            self.qapp.processEvents()

        self.assertNotEqual(self._scan1.axis_params, None)
        self.assertNotEqual(self._scan2.axis_params, None)
        self.assertNotEqual(self._scan3.axis_params, None)

    def testLockStack(self):
        """Check that axis position will be simply copy if we are in a lock
        stack"""
        self.recons_params.mode = AxisMode.manual
        position_value = 0.36
        self.recons_params.set_value_ref_tomwer(position_value)

        for scan in (self._scan1, self._scan2, self._scan3):
            self._mainWindow.process(scan)

        for i in range(5):
            self.qapp.processEvents()
            time.sleep(0.2)
            self.qapp.processEvents()

        self.assertEqual(self._scan1.axis_params.value_ref_tomwer, position_value)
        self.assertEqual(self._scan2.axis_params.value_ref_tomwer, position_value)
        self.assertEqual(self._scan3.axis_params.value_ref_tomwer, position_value)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class AxisInWorkflow(OrangeWorflowTest):
    """Test behavior of the axis widget with the following workflow:

       * five HDF5Scan
       * DataList -> Axis -> DataList
       * Axis is set to the 'acccurate' algorithm and the processing is lock.

    We make sure once the processing is finished each has a cor value and
    end in the second DataList.
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.dataList1Node = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.axisNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.AxisOW.AxisOW"
        )
        cls.dataList2Node = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.processOrangeEvents(cls)

        cls.link(cls, cls.dataList1Node, "data", cls.axisNode, "data")
        cls.link(cls, cls.axisNode, "data", cls.dataList2Node, "data")
        cls.processOrangeEvents(cls)

        cls.dataList1Widget = cls.getWidgetForNode(cls, cls.dataList1Node)
        cls.axisWidget = cls.getWidgetForNode(cls, cls.axisNode)
        cls.dataList2Widget = cls.getWidgetForNode(cls, cls.dataList2Node)

        # Set we only want to simulate the reconstruction
        cls.axisWidget.setMode("centered")
        cls.axisWidget._setModeLockFrmSettings(True)

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self._source_dir = tempfile.mkdtemp()

        def create_scan(folder_name):
            _dir = os.path.join(self._source_dir, folder_name)
            return MockHDF5(
                scan_path=_dir,
                n_ini_proj=10,
                n_proj=10,
                n_alignement_proj=2,
                create_final_ref=False,
                create_ini_dark=True,
                create_ini_ref=True,
                n_refs=1,
                dim=1000,
            ).scan

        # create scans
        self.scan_1 = create_scan("scan_1")
        self.scan_2 = create_scan("scan_2")
        self.scan_3 = create_scan("scan_3")
        self.scan_4 = create_scan("scan_4")
        self.scan_5 = create_scan("scan_5")
        self.scans = [self.scan_1, self.scan_2, self.scan_3, self.scan_4, self.scan_5]

    def tearDown(self):
        shutil.rmtree(self._source_dir)
        OrangeWorflowTest.tearDown(self)

    def test(self):
        """
        Make sure if the scan receive 5 scan in 'normal way' then it will
        compute axis for each of them and move then to the DataList
        """
        for scan in self.scans:
            self.dataList1Widget.add(scan)

        # start the workflow
        self.dataList1Widget._sendList()
        for i in range(10):
            time.sleep(0.2)
            self.app.processEvents()
        self.assertEqual(self.dataList2Widget.n_scan(), 5)


#
# @unittest.skipIf(skip_gui_test(), reason="skip gui test")
# class TestHalf(TestCaseQt):
#     """Test that the interface is updated according to the scan type"""
#
#     def setUp(self):
#         # TestCaseQt.setUp(self)
#         self._source_dir = tempfile.mkdtemp()
#
#         dir_1 = os.path.join(self._source_dir, "full_field_acq")
#         self._full_field_scan = MockHDF5(
#             scan_path=dir_1,
#             n_ini_proj=10,
#             n_proj=10,
#             n_alignement_proj=2,
#             create_final_ref=False,
#             create_ini_dark=True,
#             create_ini_ref=True,
#             n_refs=1,
#             dim=100,
#             field_of_view="Full",
#         ).scan
#         dir_2 = os.path.join(self._source_dir, "half_field_acq_1")
#         self._half_field_scan_1 = MockHDF5(
#             scan_path=dir_2,
#             n_ini_proj=10,
#             n_proj=10,
#             n_alignement_proj=2,
#             create_final_ref=False,
#             create_ini_dark=True,
#             create_ini_ref=True,
#             n_refs=1,
#             dim=100,
#             field_of_view="Half",
#             estimated_cor_frm_motor=-12,
#         ).scan
#         dir_3 = os.path.join(self._source_dir, "half_field_acq_2")
#         self._half_field_scan_2 = MockHDF5(
#             scan_path=dir_3,
#             n_ini_proj=10,
#             n_proj=10,
#             n_alignement_proj=2,
#             create_final_ref=False,
#             create_ini_dark=True,
#             create_ini_ref=True,
#             n_refs=1,
#             dim=100,
#             field_of_view="Half",
#             estimated_cor_frm_motor=None,
#         ).scan
#
#         self._window = AxisOW()
#         self.recons_params = self._window.recons_params
#         self._window.getAxis().mode = AxisMode.centered
#         self._window.show()
#         self.qWaitForWindowExposed(self._window)
#
#     def tearDown(self):
#         shutil.rmtree(self._source_dir)
#         self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
#         self._window.close()
#         # TestCaseQt.tearDown(self)
#
#     def testScenario1(self):
#         """insure behavior work when self half without estimated cor, then
#         full field acquisition, then half field with estimated cor"""
#         self.assertEqual(self._window.getRadioMode(), AxisMode.centered)
#         self._window.new_data_in(self._half_field_scan_2)
#         self.assertEqual(self._window.getRadioMode(), AxisMode.near)
#         self.assertEqual(self._window.getEstimatedCor(), 0.0)
#         self._window.new_data_in(self._full_field_scan)
#         self.assertEqual(self._window.getRadioMode(), AxisMode.centered)
#         self.assertEqual(self._window.getEstimatedCor(), 0.0)
#         self._window.new_data_in(self._half_field_scan_1)
#         self.assertEqual(self._window.getRadioMode(), AxisMode.near)
#         self.assertEqual(self._window.getEstimatedCor(), -12.0)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestOWAxis,
        TestWindowAxisComputation,
        TestAxisStack,
        AxisInWorkflow,
        # TestHalf,
    ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
