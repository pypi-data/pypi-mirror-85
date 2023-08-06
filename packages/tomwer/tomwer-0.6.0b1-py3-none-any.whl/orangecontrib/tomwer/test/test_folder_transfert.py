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
__date__ = "10/10/2019"

from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from silx.gui.utils.testutils import SignalListener
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.scan.scanfactory import ScanFactory
import unittest
import tempfile
import shutil
import time
import os


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
class TestCopyNFolder(OrangeWorflowTest):
    """test the following workflow and behavior.
    Workflow is :
        - DataListOW
        - FTSerieWidget
        - DataTransfertOW

    A list of folder into ScanList them go through FTserieWidget and to
    FolderTransfert. Make sure all the data have been copied
    """

    TIMEOUT_TEST = 20

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.scanListNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.FTSerieNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW"
        )
        cls.folderTransfertNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataTransfertOW.DataTransfertOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.scanListNode, "data", cls.FTSerieNode, "data")
        cls.link(cls, cls.FTSerieNode, "data", cls.folderTransfertNode, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.scanListWidget = cls.getWidgetForNode(cls, cls.scanListNode)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.FTSerieNode)
        cls.transfertWidget = cls.getWidgetForNode(cls, cls.folderTransfertNode)

        cls.processOrangeEvents(cls)

        # set mock mode for FTSerieWidget
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)
        cls.ftserieWidget._ftserie.setForceSync(True)
        cls.transfertWidget.turn_off_print = True
        # to avoid one folder transfert to use a thread
        cls.transfertWidget.setForceSync(True)
        # add signal listener
        cls.dataTransfertListener = SignalListener()
        cls.transfertWidget.scanready.connect(cls.dataTransfertListener)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.scanListNode, cls.FTSerieNode, cls.folderTransfertNode):
            cls.removeNode(cls, node)
        cls.scanListWidget = None
        cls.ftserieWidget = None
        cls.transfertWidget = None
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)

        # reset signal listener
        self.dataTransfertListener.clear()

        # Create n folder
        self.folders = []
        for i in range(1):
            inputFolder = tempfile.mkdtemp()
            self.folders.append(inputFolder)
            # copy files directly
            MockEDF.fastMockAcquisition(inputFolder)

        self.outputdir = tempfile.mkdtemp()

    def tearDown(self):
        # remove input folders if any
        for f in self.folders:
            if os.path.isdir(f):
                shutil.rmtree(f)

        # remove output folders if any
        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)

        OrangeWorflowTest.tearDown(self)

    def testCopy(self):
        # add outputdir to transfertFolderWidget
        self.assertTrue(os.path.isdir(self.outputdir))
        self.transfertWidget.setDestDir(self.outputdir)

        # add all fodler into the scanList
        for f in self.folders:
            assert os.path.isdir(f)
            self.scanListWidget.add(ScanFactory.create_scan_object(scan_path=f))
            self.app.processEvents()
            self.processOrangeEventsStack()

        # make sure nothing has been copied
        self.assertTrue(self.outpudirIsEmpty())

        # then start workflow run by asking the scanListWidget to notice action
        # to the next widget
        self.scanListWidget.start()

        timeout = self.TIMEOUT_TEST
        while timeout > 0 and self.dataTransfertListener.callCount() == 0:
            timeout = timeout - 0.2
            self.app.processEvents()
            self.processOrangeEventsStack()
            time.sleep(0.2)

        self.assertTrue(self.dataHasBeenCopied())
        self.app.processEvents()

    def outpudirIsEmpty(self):
        return len(os.listdir(self.outputdir)) == 0

    def dataHasBeenCopied(self):
        return len(os.listdir(self.outputdir)) == 1


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestCopyNFolder,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
