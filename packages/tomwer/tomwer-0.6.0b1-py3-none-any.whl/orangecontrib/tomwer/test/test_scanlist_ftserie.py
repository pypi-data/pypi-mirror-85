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

import copy
import logging
import os
import shutil
import tempfile
import unittest
import time
from silx.gui.utils.testutils import SignalListener

from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import (
    FastSetupAll,
)
from tomwer.synctools.stacks.reconstruction.ftseries import _ReconsFtSeriesThread
from tomwer.test.utils import UtilsTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from tomwer.core.utils.scanutils import MockEDF

logging.disable(logging.INFO)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestScanListFTSerieWorkflow(OrangeWorflowTest):
    """Make sure the reconstruction of the second scan is executed with the
    correct reconstruction parameters.
    Set up is as following :
        - ScanList contains two datasets. Those scan can contains or not some .h5
        - FTSerie is activated with or without H5Exploration option
    """

    def setUp(self):
        super(TestScanListFTSerieWorkflow, self).setUp()
        self.inputDir = tempfile.mkdtemp()

        # define reconstruction parameters
        ft = FastSetupAll()
        self.default = copy.deepcopy(ft.structures)
        assert "FT" in ft.structures
        assert "NUM_PART" in ft.structures["FT"]
        assert ft.structures["FT"]["NUM_PART"] not in (1, 2)
        ft.structures["FT"]["NUM_PART"] = 1
        self.st1 = copy.deepcopy(ft.structures)
        ft.structures["FT"]["NUM_PART"] = 2
        self.st2 = copy.deepcopy(ft.structures)

    def tearDow(self):
        if os.path.isdir(self.inputDir):
            shutil.rmtree(self.inputDir)
        super(TestScanListFTSerieWorkflow, self).tearDow()

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nodeScanList = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.nodeFTSerie = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.FtseriesOW.FtseriesOW"
        )
        cls.processOrangeEvents(cls)

        cls.link(cls, cls.nodeScanList, "data", cls.nodeFTSerie, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.nodeFTSerie)
        _ReconsFtSeriesThread.setCopyH5FileReconsIntoFolder(True)

        # Set we only want to simulate the reconstruction
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeFTSerie):
            cls.removeNode(cls, node)
        del cls.scanListWidget
        del cls.ftserieWidget
        OrangeWorflowTest.tearDownClass()

    def initData(self, data01H5, data10H5):
        """Init the two datasets and set the given .h5 file if any given
        The order of scanning is always : first dataset01, second dataset10

        :param data01H5: the values of the structures to save as a h5 file.
            Apply on the daset01.
            If None given then no H5 file will be saved
        :param data10H5: the values of the structures to save as a h5 file.
            Apply on the daset10.
            If None given then no H5 file will be saved
        """

        dataDir01 = UtilsTest.getEDFDataset("test01")
        dataDir10 = UtilsTest.getEDFDataset("test10")
        # removing any previous scan
        self.clearInputFolder()

        # set new scan
        self.dest01 = os.path.join(self.inputDir, os.path.basename(dataDir01))
        shutil.copytree(src=dataDir01, dst=self.dest01)
        # make sure no h5 exists yet
        for f in os.listdir(dataDir01):
            assert not f.lower().endswith(".h5")
        self.dest10 = os.path.join(self.inputDir, os.path.basename(dataDir10))
        for f in os.listdir(dataDir10):
            assert not f.lower().endswith(".h5")
        shutil.copytree(src=dataDir10, dst=self.dest10)

        # if needed create some h5 file from structure
        data_and_dir = (data01H5, self.dest01), (data10H5, self.dest10)
        for data, dataDir in data_and_dir:
            if data is not None:
                ft = FastSetupAll()
                ft.structures = data
                path = os.path.join(dataDir, "reconsH5File.h5")
                ft.writeAll(path, 3.8)

        # update scanList
        self.scanListWidget.clear()
        self.scanListWidget.add(self.dest01)
        self.scanListWidget.add(self.dest10)

    def clearInputFolder(self):
        for subFolder in os.listdir(self.inputDir):
            folder = os.path.join(self.inputDir, subFolder)
            assert os.path.isdir(folder)
            # should never store something else than a folder
            shutil.rmtree(folder)

    def setH5Exploration(self, b):
        """Activate or not the exploration"""
        self.ftserieWidget.setH5Exploration(b)

    def runAndTestList(self, structures, results, caseMsg):
        """Check that the reconstruction are send in the same order as the list
        is sending them
        """
        # 1.0 processing
        self.initData(structures[0], structures[1])
        self.scanListWidget._sendList()

        # first folder
        self.processOrangeEvents()
        # # second folder
        # self.processOrangeEvents()

        # 2.0 testing
        # check the first scan is correct
        output01 = os.path.join(self.dest01, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output01))
        ft01 = FastSetupAll()
        ft01.readAll(output01, 3.8)

        # with self.subTest(msg=name):
        with self.subTest(
            msg="test reconstruction parameters used - folder1 : " + caseMsg,
            value=int(ft01.structures["FT"]["NUM_PART"]),
            expected=int(results[0]["FT"]["NUM_PART"]),
        ):
            self.assertEqual(
                int(ft01.structures["FT"]["NUM_PART"]),
                int(results[0]["FT"]["NUM_PART"]),
            )
        os.remove(output01)

        # check the second scan is correct
        output10 = os.path.join(self.dest10, _ReconsFtSeriesThread.copyH5ReconsName)
        self.assertTrue(os.path.isfile(output10))
        ft10 = FastSetupAll()
        ft10.readAll(output10, 3.8)

        with self.subTest(
            msg="test reconstruction parameters used - folder2 : " + caseMsg,
            value=ft10.structures["FT"]["NUM_PART"],
            expected=results[1]["FT"]["NUM_PART"],
        ):
            self.assertTrue(
                ft10.structures["FT"]["NUM_PART"] == results[1]["FT"]["NUM_PART"]
            )
        os.remove(output10)

    def getTestMsg(self, ftserieStatus, structures, results):
        """Return the message fitting with the structures we are setting to
        test01 and test10 and to the restul we want"""
        msg = "FTSerieWidget status : " + ftserieStatus
        msg += "\nConfiguration of folders : "
        msg += "\n    - Folder 1 contains "
        msg += (
            "no .h5"
            if structures[0] is self.default
            else "h5 with "
            + ("st1" if structures[0] is self.st1 else "st2")
            + " structure"
        )
        msg += "\n    - Folder 2 contains "
        msg += (
            "no .h5"
            if structures[1] is self.default
            else "h5 with "
            + ("st1" if structures[1] is self.st1 else "st2")
            + " structure"
        )
        msg += "\nResults in folder should be :"
        msg += "\n   - for first folder :"
        msg += (
            "default"
            if results[0] is self.default
            else ("st1" if results[0] is self.st1 else "ft2")
        )
        msg += "\n   - for second folder :"
        msg += (
            "default"
            if results[1] is self.default
            else ("st1" if results[1] is self.st1 else "ft2")
        )
        return msg


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
@unittest.skip("Fail on CI...")
class TestLocalReconstructions(OrangeWorflowTest):
    """test with three widgets : ScanList, FTSerieWidget and ImageStackViewerWidget.
    Make sure that when path with data set:
        - scanList is sending signals
        - FTSerieWidget is reconstructing and emitting a signal
        - viewer is displaying a set of data (receiving the information)
    """

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self.inputdir = tempfile.mkdtemp()

        # copy files directly
        MockEDF.fastMockAcquisition(self.inputdir)
        self.ftserieListener = SignalListener()
        self.ftserieWidget.sigScanReady.connect(self.ftserieListener)

    def tearDow(self):
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nodeScanList = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.nodeFTSerie = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW"
        )
        cls.nodeViewer = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.visualization.ImageStackViewerOW.ImageStackViewerOW",
        )
        cls.processOrangeEvents(cls)

        cls.link(cls, cls.nodeScanList, "data", cls.nodeFTSerie, "data")
        cls.link(cls, cls.nodeFTSerie, "data", cls.nodeViewer, "data")
        cls.processOrangeEvents(cls)

        cls.scanListWidget = cls.getWidgetForNode(cls, cls.nodeScanList)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.nodeFTSerie)
        cls.viewerWidget = cls.getWidgetForNode(cls, cls.nodeViewer)

        # Set we only want to simulate the reconstruction
        cls.ftserieWidget._ftserie.reconsStack.setMockMode(True)
        # cls.ftserieWidget._ftserie.setForceSync(True)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeScanList, cls.nodeFTSerie, cls.nodeViewer):
            cls.removeNode(cls, node)
        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""
        # add the path to the directory
        self.scanListWidget.add(self.inputdir)
        self.assertTrue(self.ftserieWidget._ftserie._scan is None)

        self.assertTrue(self.viewerWidget.viewer.getCurrentScanFolder() == "")
        self.assertTrue(self.viewerWidget.viewer.ftseriereconstruction is None)
        self.app.processEvents()
        self.scanListWidget.show()
        self.qWaitForWindowExposed(self.scanListWidget)
        # start the workflow by sending the list of path
        self.scanListWidget._sendList()

        timeout = 5
        loop_duration = 0.01
        while self.ftserieListener.callCount() < 1 and timeout > 0:
            self.app.processEvents()
            time.sleep(loop_duration)
            timeout -= loop_duration

        if timeout <= 0:
            raise TimeoutError("viewer is never activated")

        self.app.processEvents()

        self.assertEqual(self.viewerWidget.viewer.getCurrentScanFolder(), self.inputdir)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanListFTSerieWorkflow, TestLocalReconstructions):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
