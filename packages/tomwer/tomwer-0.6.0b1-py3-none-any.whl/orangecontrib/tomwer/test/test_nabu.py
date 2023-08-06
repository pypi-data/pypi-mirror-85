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
__date__ = "09/02/2018"

import logging
import os
import shutil
import tempfile
from glob import glob
import unittest

from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test

logging.disable(logging.INFO)

app = QApplicationManager()


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestNabuWidget(OrangeWorflowTest):
    """
    test the workflow composed of the following widgets :
        - DataList
        - nabu reconstruction
        - data validator
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nodeDataList = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.nodeNabu = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuOW.NabuOW"
        )
        cls.nodeValidator = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataValidatorOW.DataValidatorOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nodeDataList, "data", cls.nodeNabu, "data")
        cls.link(cls, cls.nodeNabu, "data", cls.nodeValidator, "data")
        cls.link(
            cls,
            cls.nodeValidator,
            "change recons params",
            cls.nodeNabu,
            "change recons params",
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.dataListWidget = cls.getWidgetForNode(cls, cls.nodeDataList)
        cls.nabuWidget = cls.getWidgetForNode(cls, cls.nodeNabu)
        cls.dataValidatorWidget = cls.getWidgetForNode(cls, cls.nodeValidator)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeDataList, cls.nodeNabu, cls.nodeValidator):
            cls.removeNode(cls, node)
        del cls.dataListWidget
        del cls.nabuWidget
        del cls.dataValidatorWidget
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        dataset = "D2_H2_T2_h_"
        self.folder = tempfile.mkdtemp()
        dataset_folder = os.path.join(self.folder, dataset)
        shutil.copytree(src=UtilsTest().getEDFDataset(dataset), dst=dataset_folder)
        self.dataListWidget.add(dataset_folder)
        self.scan = ScanFactory.create_scan_object(scan_path=dataset_folder)
        # make sure there is no .cfg file inside
        assert len(self.getCfgFiles()) == 0

        self.nabuWidget.setDryRun(True)
        self.nabuWidget.setConfiguration({"tomwer_slices": None})

        # monkey patch exec_ to check behavior
        self.nabuWidget._replaceExec_()

    def tearDown(self):
        shutil.rmtree(self.folder)
        OrangeWorflowTest.tearDown(self)

    def testWorkflow(self):
        self.dataListWidget._sendList()

        # wait until the reconstruction is made and the data watcher pop
        self.qWaitForWindowExposed(self.dataValidatorWidget, timeout=10)

        # check .cfg files are here and validator is treating the current scan
        for i in range(10):
            self.qapp.processEvents()
            import time

            time.sleep(0.1)
            self.qapp.processEvents()
        current_scan_path = self.dataValidatorWidget.getCurrentScanID()
        self.assertEqual(current_scan_path, self.scan.path)
        self.assertEqual(len(self.getCfgFiles()), 1)
        # validate the scan
        self.dataValidatorWidget.changeReconsParamCurrentScan()
        self.qapp.processEvents()

        # wait for ftseries to be pop up within the dialog
        self.qWaitForWindowExposed(self.nabuWidget, timeout=10)

    def getCfgFiles(self):
        return glob(self.scan.path + os.sep + "*.cfg")


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestNabuWidget,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
