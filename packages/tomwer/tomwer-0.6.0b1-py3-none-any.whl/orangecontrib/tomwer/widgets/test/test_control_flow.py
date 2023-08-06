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
__date__ = "24/01/2017"


import logging
import unittest
import tempfile
import shutil
import os
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import UtilsTest
import time
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test

logging.disable(logging.INFO)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestNXTomomill(OrangeWorflowTest):
    """class testing the flow:
    - NXTomomillOW
    - DataSelector
    - DataSelector (2)

    This allows to insure compatibility of EDF and HDF5 with those widgets
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets

        cls.nxtomomillNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.NXTomomillOW.NXTomomillOW"
        )
        cls.dataSelector1Node = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW"
        )
        cls.dataSelector2Node = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nxtomomillNode, "data", cls.dataSelector1Node, "data")
        cls.link(cls, cls.dataSelector1Node, "data", cls.dataSelector2Node, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.nxtomomillWidget = cls.getWidgetForNode(cls, cls.nxtomomillNode)
        cls.dataSelector1Widget = cls.getWidgetForNode(cls, cls.dataSelector1Node)
        cls.dataSelector2Widget = cls.getWidgetForNode(cls, cls.dataSelector2Node)

        cls.processOrangeEvents(cls)

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self._dataFolder = tempfile.mkdtemp()

        # a file for nxtomomill (with one entry)
        nxtomomill_file = "tomo_v2_external.h5"
        nxtomomill_folder = os.path.join(self._dataFolder, "tomo_v2")
        os.mkdir(nxtomomill_folder)
        self.nxtomomill_file = os.path.join(nxtomomill_folder, nxtomomill_file)
        shutil.copyfile(
            src=UtilsTest.getH5Dataset(folderID=nxtomomill_file),
            dst=self.nxtomomill_file,
        )

        # an hdf5 file to add on the first data selector (with two entries)
        hdf5_file = "frm_edftomomill_twoentries.nx"
        self.hdf5_file = os.path.join(self._dataFolder, hdf5_file)
        shutil.copy(src=UtilsTest.getH5Dataset(hdf5_file), dst=self.hdf5_file)

        # an edf folder to be added on the first data selector
        self.edf_folder = os.path.join(self._dataFolder, "D2_H2_T2_h_")
        shutil.copytree(src=UtilsTest.getEDFDataset("D2_H2_T2_h_"), dst=self.edf_folder)

        # ignore entries
        self.nxtomomillWidget.request_input = False

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nxtomomillNode, cls.dataSelector1Node, cls.dataSelector2Node):
            cls.removeNode(cls, node)
        cls.nxtomomillWidget = None
        cls.dataSelector1Widget = None
        cls.dataSelector2Widget = None
        OrangeWorflowTest.tearDownClass()

    def tearDown(self):
        shutil.rmtree(self._dataFolder)
        OrangeWorflowTest.tearDown(self)

    def testFlow(self):
        """
        Make sure all possibles input are managed and processed from one
        widget to the others
        """
        self.nxtomomillWidget.add(self.nxtomomill_file)
        self.qapp.processEvents()
        self.assertEqual(self.nxtomomillWidget.n_scan(), 5)
        self.assertEqual(len(self.nxtomomillWidget.widget.datalist.items), 5)
        # move to the first data selector
        self.nxtomomillWidget.start()
        # need some time to accumulate the scans
        for i in range(5):
            time.sleep(0.05)
            self.qapp.processEvents()

        self.assertEqual(self.dataSelector1Widget.n_scan(), 5)
        # check bliss file have been converted

        hdf5_urls = self.dataSelector1Widget.widget.dataList.items
        _, file_path = list(hdf5_urls.keys())[0].split("@")
        self.assertTrue(file_path.endswith(".nx"))

        # add the hdf5_file and the edf folder
        self.dataSelector1Widget.add(self.hdf5_file)
        self.qapp.processEvents()
        self.assertEqual(self.dataSelector1Widget.n_scan(), 7)
        self.dataSelector1Widget.add(self.edf_folder)
        self.qapp.processEvents()
        self.assertEqual(self.dataSelector1Widget.n_scan(), 8)

        # move to the second data selector
        self.qapp.processEvents()
        self.dataSelector1Widget.selectAll()
        self.dataSelector1Widget.send()
        for i in range(8):
            time.sleep(0.05)
            self.qapp.processEvents()
        self.assertEqual(self.dataSelector2Widget.n_scan(), 8)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestNXTomomill,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
