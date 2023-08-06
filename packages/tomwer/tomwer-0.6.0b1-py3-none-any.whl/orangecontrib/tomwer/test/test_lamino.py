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
import time
import unittest

from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core.process.reconstruction.lamino.tofu import has_tofu
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test

logging.disable(logging.INFO)

app = QApplicationManager()


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
@unittest.skipIf(has_tofu() is False, "Tofu missing")
class TestLaminoWidget(OrangeWorflowTest):
    """
    test the workflow composed of the following widgets :
        - Datawatcher
        - Lamino widget
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nodeDataWatcher = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataWatcherOW.DataWatcherOW"
        )
        cls.nodeTofu = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.TofuOW.TofuOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nodeDataWatcher, "data", cls.nodeTofu, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.dataWatcherWidget = cls.getWidgetForNode(cls, cls.nodeDataWatcher)
        cls.tofuWidget = cls.getWidgetForNode(cls, cls.nodeTofu)

    @classmethod
    def tearDownClass(cls):
        cls.dataWatcherWidget.close()
        for node in (cls.nodeDataWatcher, cls.nodeTofu):
            cls.removeNode(cls, node)
        del cls.dataWatcherWidget
        del cls.tofuWidget
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self.folder = tempfile.mkdtemp()
        datasetID = "test10"
        self.folder = os.path.join(self.folder, datasetID)
        shutil.copytree(src=UtilsTest().getEDFDataset(datasetID), dst=self.folder)

        self.dataWatcherWidget.setFolderObserved(self.folder)

    def tearDown(self):
        shutil.rmtree(self.folder)
        OrangeWorflowTest.tearDown(self)

    def testWorkflow(self):
        self.dataWatcherWidget._widget.mockObservation(self.folder)

        # let dark ref process time to end
        for _t in (1, 1):
            app.processEvents()
            time.sleep(_t)
            app.processEvents()
        self.assertTrue(
            self.tofuWidget._mainWidget._mainWidget._tabs._inputWidget.getPixelSize()
            == 3.02e-06
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLaminoWidget,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
