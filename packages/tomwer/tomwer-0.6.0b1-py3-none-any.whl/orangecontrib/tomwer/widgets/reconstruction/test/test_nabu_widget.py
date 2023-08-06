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
__date__ = "27/03/2020"


import logging
import os
import shutil
import tempfile
import unittest
from silx.gui import qt
from orangecontrib.tomwer.widgets.reconstruction.NabuOW import NabuOW
from tomwer.core.utils.scanutils import MockHDF5
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.synctools.ftseries import QReconsParams
from tomwer.core.process.reconstruction.nabu.utils import _NabuMode
from tomwer.test.utils import UtilsTest
from silx.gui.utils.testutils import TestCaseQt
from silx.gui.utils.testutils import SignalListener
from tomwer.core.settings import mock_lsbram
from tomwer.core import utils
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomoscan.scanbase import _FOV
from glob import glob
import time
import h5py

logging.disable(logging.INFO)


class TestNabuWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._recons_params = QReconsParams()
        self.widget = NabuOW(parent=None)
        self.scan_dir = tempfile.mkdtemp()
        # create dataset
        self.master_file = os.path.join(self.scan_dir, "frm_edftomomill_twoentries.nx")
        shutil.copyfile(
            UtilsTest.getH5Dataset(folderID="frm_edftomomill_twoentries.nx"),
            self.master_file,
        )
        self.scan = HDF5TomoScan(scan=self.master_file, entry="entry0000")
        # create listener for the nabu widget
        self.signal_listener = SignalListener()

        # connect signal / slot
        self.widget.sigScanReady.connect(self.signal_listener)

        # set up
        utils.mockLowMemory(True)
        mock_lsbram(True)
        self.widget.setDryRun(dry_run=True)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None

        utils.mockLowMemory(False)
        mock_lsbram(False)

        TestCaseQt.tearDown(self)

    def testLowMemory(self):
        """Make sure no reconstruction is started if we are low in memory in
        lbsram"""
        self.assertEqual(len(glob(os.path.join(self.scan_dir, "*.cfg"))), 0)
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(len(glob(os.path.join(self.scan_dir, "*.cfg"))), 0)

    def wait_processing(self):
        timeout = 10
        while timeout >= 0 and self.signal_listener.callCount() == 0:
            timeout -= 0.1
            time.sleep(0.1)
        if timeout <= 0.0:
            raise TimeoutError("nabu widget never end processing")

    def patch_fov(self, value: str):
        with h5py.File(self.scan.master_file, mode="a") as h5s:
            for entry in ("entry0000", "entry0001"):
                entry_node = h5s[entry]
                if "instrument/detector/field_of_view" in entry_node:
                    del entry_node["instrument/detector/field_of_view"]
                entry_node["instrument/detector/field_of_view"] = value

    def testSetConfiguration(self):
        """Make sure the configuration evolve from scan information"""
        self.assertEqual(self.widget.getMode(), _NabuMode.FULL_FIELD)
        self.patch_fov(value=_FOV.HALF.value)
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(self.widget.getMode(), _NabuMode.HALF_ACQ)
        self.patch_fov(value=_FOV.FULL.value)
        self.scan.clear_caches()
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(self.widget.getMode(), _NabuMode.FULL_FIELD)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestNabuWithBunchOfScan(OrangeWorflowTest):
    """
    Test the nabu widget with a bunch ot HDF5Scan and make sure all are
    returner
    """

    """Test behavior of the axis widget with the following workflow:

       * five HDF5Scan
       * NabuReconstruction -> Axis -> DataList

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
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuOW.NabuOW"
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
        # TODO: add some dark and flat

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
        self.assertEqual(self.dataList2Widget.n_scan(), 5)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestNabuWidget, TestNabuWithBunchOfScan):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
