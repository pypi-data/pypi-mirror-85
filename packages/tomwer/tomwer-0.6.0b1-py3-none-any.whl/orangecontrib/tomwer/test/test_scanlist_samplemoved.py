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
__date__ = "22/03/2018"


import tempfile
import logging
import unittest
import shutil
import time
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from tomwer.core.utils.scanutils import MockHDF5


logging.disable(logging.INFO)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestScanListSampleMovedWorkflow(OrangeWorflowTest):
    """Make sure the sample moved is correctly connecting to the orange-canvas
    and that it will display requested scans
    """

    def setUp(self):
        super(TestScanListSampleMovedWorkflow, self).setUp()
        dataset = "D2_H2_T2_h_"
        self.EDFdataTestDir = UtilsTest.getEDFDataset(dataset)

        self.output_folder = tempfile.mkdtemp()

        self._hdf5_n_proj = 10
        self._hdf5_n_alignment = 2
        hdf5_mock = MockHDF5(
            scan_path=self.output_folder,
            n_ini_proj=self._hdf5_n_proj,
            n_proj=self._hdf5_n_proj,
            scan_range=180,
        )
        hdf5_mock.add_alignment_radio(index=self._hdf5_n_alignment, angle=90)
        hdf5_mock.add_alignment_radio(index=self._hdf5_n_alignment + 1, angle=0)
        self.hdf5_scan = hdf5_mock.scan

        self.sampleMovedWidget.clear()
        self.scanListWidget.clear()
        self.qapp.processEvents()

    def tearDow(self):
        shutil.rmtree(self.output_folder)
        super(TestScanListSampleMovedWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create widgets
        cls.nodeScanList = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.nodeSampleMoved = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.visualization.SampleMovedOW.SampleMovedOW",
        )
        cls.processOrangeEvents(cls)

        cls.link(cls, cls.nodeScanList, "data", cls.nodeSampleMoved, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.sampleMovedWidget = cls.getWidgetForNode(cls, cls.nodeSampleMoved)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeSampleMoved):
            cls.removeNode(cls, node)
        cls.scanListWidget = None
        cls.sampleMovedWidget = None
        super().tearDownClass()


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestScanListSampleMovedWorkflowEDF(TestScanListSampleMovedWorkflow):
    def testEDF(self):
        self.assertEqual(len(self.sampleMovedWidget._mainWidget._images), 0)

        self.scanListWidget.add(self.EDFdataTestDir)
        self.scanListWidget._sendList()
        for i in range(20):
            time.sleep(0.05)
            self.qapp.processEvents()
        self.assertEqual(len(self.sampleMovedWidget._mainWidget._images), 3605)


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestScanListSampleMovedWorkflowHDF5(TestScanListSampleMovedWorkflow):
    def testHDF5(self):
        self.assertEqual(len(self.sampleMovedWidget._mainWidget._images), 0)
        self.assertTrue(self.sampleMovedWidget._scanNameQLabel.text() == "")

        self.scanListWidget.add(self.hdf5_scan)
        self.scanListWidget._sendList()
        for i in range(20):
            time.sleep(0.05)
            self.qapp.processEvents()
        n_total_proj = self._hdf5_n_proj + self._hdf5_n_alignment
        self.assertEqual(len(self.sampleMovedWidget._mainWidget._images), n_total_proj)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestScanListSampleMovedWorkflow,
        TestScanListSampleMovedWorkflowEDF,
        TestScanListSampleMovedWorkflowHDF5,
    ):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
