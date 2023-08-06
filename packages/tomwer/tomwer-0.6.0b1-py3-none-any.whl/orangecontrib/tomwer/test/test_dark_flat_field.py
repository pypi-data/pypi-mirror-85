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
from glob import glob

from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core import utils
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.settings import mock_lsbram
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from silx.gui import qt
from silx.gui.utils.testutils import SignalListener
from tomwer.core.scan.scanfactory import ScanFactory

logging.disable(logging.INFO)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestConstructionDarkAndFlatField(OrangeWorflowTest):
    """
    test the workflow composed of the following widgets :
        - DataWatcherOW
        - DarkRefsCopy : Make sure the refCopy is correctly make
    """

    TIMEOUT = 20

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nodeDataWatcher = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataWatcherOW.DataWatcherOW"
        )
        cls.nodeDarkRefs = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW",
        )
        cls.darkRefListener = SignalListener()
        cls.datawatcherListener = SignalListener()
        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nodeDataWatcher, "data", cls.nodeDarkRefs, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.datawatcherWidget = cls.getWidgetForNode(cls, cls.nodeDataWatcher)
        cls.darkRefsWidget = cls.getWidgetForNode(cls, cls.nodeDarkRefs)

        # set mock mode for FTSerieWidget
        # set data watcher ready for observation
        cls.datawatcherWidget.displayAdvancement = False
        # force Dark ref to be sync
        cls.darkRefsWidget.setForceSync(True)
        cls.darkRefsWidget.widget.sigScanReady.connect(cls.darkRefListener)
        cls.datawatcherWidget._widget.sigScanReady.connect(cls.datawatcherListener)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeDataWatcher, cls.nodeDarkRefs):
            cls.removeNode(cls, node)
        cls.app.processEvents()
        del cls.datawatcherWidget
        del cls.darkRefsWidget
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)

        def prepareRefFolder():
            datasetID = "test10"
            self.inputFolder = tempfile.mkdtemp()
            self.scanFolder = os.path.join(self.inputFolder, datasetID)
            self.copytree = shutil.copytree(
                src=UtilsTest().getEDFDataset(datasetID), dst=self.scanFolder
            )

            [
                os.remove(f)
                for f in DarkRefs.getRefHSTFiles(self.scanFolder, prefix="refHST")
            ]
            [
                os.remove(f)
                for f in DarkRefs.getDarkHSTFiles(self.scanFolder, prefix="darkHST")
            ]

        prepareRefFolder()

        def prepareScanToProcess():
            self._refParentFolder = tempfile.mkdtemp()
            datasetRef = "test01"
            self.refFolder = os.path.join(self._refParentFolder, datasetRef)
            shutil.copytree(
                src=UtilsTest().getEDFDataset(datasetRef), dst=self.refFolder
            )
            # copy .info file to have coherent REf_N values
            shutil.copyfile(
                src=os.path.join(self._refParentFolder, "test01", "test01.info"),
                dst=os.path.join(self.scanFolder, "test10.info"),
            )
            assert len(glob(os.path.join(self.refFolder, "refHST*"))) > 0
            # dark file should be dark.edf and not darkHST.edf
            dark_HST = os.path.join(self.refFolder, "darkHST0000.edf")
            if os.path.exists(dark_HST):
                os.rename(dark_HST, os.path.join(self.refFolder, "dark.edf"))
            assert len(glob(os.path.join(self.refFolder, "dark.edf"))) == 1

        prepareScanToProcess()

        self.datawatcherWidget.setFolderObserved(self.inputFolder)
        self.darkRefsWidget.recons_params._set_skip_if_exist(True)
        self.darkRefsWidget.setRefsFromScan(
            ScanFactory.create_scan_object(self.refFolder)
        )
        self.darkRefsWidget.setModeAuto(False)
        utils.mockLowMemory(False)
        mock_lsbram(True)

        # reset listeners
        self.darkRefListener.clear()
        self.datawatcherListener.clear()

    def tearDown(self):
        self.datawatcherWidget._widget.stop()
        self.datawatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.datawatcherWidget.close()
        self.datawatcherWidget = None
        shutil.rmtree(self._refParentFolder)
        shutil.rmtree(self.inputFolder)
        OrangeWorflowTest.tearDown(self)

    def testWorkflow(self):
        assert not self.datawatcherWidget._widget.isObserving
        self.datawatcherWidget.startObservation()
        timeout = TestConstructionDarkAndFlatField.TIMEOUT
        # wait until find the scan
        while self.datawatcherListener.callCount() < 1 and timeout > 0:
            self.app.processEvents()
            timeout -= 0.2
            time.sleep(0.2)

        if timeout < 0:
            raise TimeoutError("data watcher can't find any scan")

        # let dark ref process time to end
        timeout = TestConstructionDarkAndFlatField.TIMEOUT
        while timeout > 0 and self.darkRefListener.callCount() < 1:
            self.app.processEvents()
            timeout -= 0.2
            time.sleep(0.2)

        self.app.processEvents()
        if timeout < 0:
            raise TimeoutError("darkef didn't process")

        self.assertTrue(
            len(DarkRefs.getDarkHSTFiles(self.scanFolder, prefix="refHST")) > 0
        )
        self.assertTrue(
            len(DarkRefs.getRefHSTFiles(self.scanFolder, prefix="dark.edf")) > 0
        )
        while self.app.hasPendingEvents():
            self.app.processEvents()

        self.assertTrue(self.darkRefListener.callCount() == 1)
        self.assertTrue(self.datawatcherListener.callCount() == 1)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConstructionDarkAndFlatField,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
