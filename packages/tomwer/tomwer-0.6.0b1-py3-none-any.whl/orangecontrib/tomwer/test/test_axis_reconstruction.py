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
"""contains test for relation between axis and ftseries"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "23/10/2019"


import unittest
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
from tomwer.core.utils.scanutils import MockHDF5, MockEDF
from silx.gui.utils.testutils import SignalListener
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.process.reconstruction.axis.axis import AxisProcess
from tomwer.core.process.reconstruction.nabu.nabuslices import NabuSlices
import tempfile
import shutil
import time
import glob
import os
import h5py


TIMEOUT_TEST = 10


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestAxisFtseriesEDF(OrangeWorflowTest):
    """Check the orange widget 'Axis' with an edf scan"""

    """
    Create the following workflow:
    datawatcherOW -> axisOW -> ftseriesOW
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nodeDataWatcher = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataWatcherOW.DataWatcherOW"
        )
        cls.nodeAxis = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.AxisOW.AxisOW"
        )
        cls.nodeFTSerie = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW"
        )
        cls.dataSelectorNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nodeDataWatcher, "data", cls.nodeAxis, "data")
        cls.link(cls, cls.nodeAxis, "data", cls.nodeFTSerie, "data")
        cls.link(cls, cls.nodeFTSerie, "data", cls.dataSelectorNode, "data")
        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.datawatcherWidget = cls.getWidgetForNode(cls, cls.nodeDataWatcher)
        cls.axisWidget = cls.getWidgetForNode(cls, cls.nodeAxis)
        cls.ftserieWidget = cls.getWidgetForNode(cls, cls.nodeFTSerie)

    @classmethod
    def tearDownClass(cls):
        cls.datawatcherWidget.stopObservation()
        for node in (cls.nodeAxis, cls.nodeFTSerie, cls.nodeDataWatcher):
            cls.removeNode(cls, node)
        cls.app.processEvents()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        self.root_dir = tempfile.mkdtemp()
        self.scan_1_path = os.path.join(self.root_dir, "scan1")
        self.scan_2_path = os.path.join(self.root_dir, "scan2")
        self.scan_3_path = os.path.join(self.root_dir, "scan3")
        self.scan_dirs = [self.scan_1_path, self.scan_2_path, self.scan_3_path]

        self.mocks = []
        for scan_dir in self.scan_dirs:
            mock = MockEDF(scan_path=scan_dir, n_radio=20, n_ini_radio=20)
            assert os.path.exists(scan_dir)
            self.mocks.append(mock)

        # set up axis, ftseries and data watcher
        self.datawatcherWidget.setFolderObserved(self.root_dir)
        assert os.path.exists(self.root_dir)
        self.axisWidget._axis_params.mode = "manual"
        self.ftserieWidget._ftserie.dry_run = True
        self.ftserieWidget.recons_params.axis.do_axis_correction = True
        self.ftserieWidget.recons_params.axis.use_tomwer_axis = True
        self.ftserieWidget.recons_params.axis.use_old_tomwer_axis = False

        self.axisWidget._skip_exec(True)

        # create listeners
        self.axisListener = SignalListener()
        self.ftseriesListener = SignalListener()

        # signal / slot connection
        self.axisWidget.sigScanReady.connect(self.axisListener)
        self.ftserieWidget.sigScanReady.connect(self.ftseriesListener)

    def tearDown(self) -> None:
        shutil.rmtree(self.root_dir)
        super().tearDown()

    def testScenario(self):
        """
        scenario:
        1. scan1 is detected, axis should wait for an answer, then the axis is
           computed but not locked, ftseries should use the axis value computed.
        2. scan2 is detected, axis should wait for an answer, then axis is
           computed and lock this time, ftseries should use the axis value
           computed.
        3. scan3 is detected, it should pass directly through axis and the
           cor value set and used by ftseries
        """
        assert os.path.exists(self.scan_1_path)
        assert os.path.exists(self.scan_2_path)
        assert os.path.exists(self.scan_3_path)

        def _wait(timeout):
            timeout = timeout - 0.1
            self.app.processEvents()
            self.processOrangeEventsStack()
            time.sleep(0.1)
            return timeout

        # 1.
        self.datawatcherWidget.startObservation()
        self.axisWidget._axis_params.set_value_ref_tomwer(12.0)
        self.mocks[0].end_acquisition()

        # wait until we can validate
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisWidget._n_skip == 0:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis never ended calculation")
        validate_btn = self.axisWidget._widget._radioAxis._applyBut
        validate_btn.click()

        # wait until the axis windows expose (so scan should have been received)
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisListener.callCount() < 1:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis was never validated")

        timeout = TIMEOUT_TEST
        while timeout > 0 and self.ftseriesListener.callCount() < 1:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("ftserie never ended reconstruction")

        scan_1_processes_file = os.path.join(self.scan_1_path, "tomwer_processes.h5")

        self.assertTrue(os.path.exists(scan_1_processes_file))
        with h5py.File(scan_1_processes_file, "r") as h5f:
            self.assertTrue("entry" in h5f)
            self.assertTrue("tomwer_process_0" in h5f["entry"])
            self.assertTrue("results" in h5f["entry"]["tomwer_process_0"])
            results = h5f["entry"]["tomwer_process_0"]["results"]
            self.assertTrue("center_of_rotation" in results)
            self.assertAlmostEqual(results["center_of_rotation"][()], 12.0)

        # 2.
        self.axisWidget._axis_params.set_value_ref_tomwer(-6.369)
        self.mocks[1].end_acquisition()

        # wait until we can validate
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisWidget._n_skip == 1:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis never ended calculation")
        validate_btn = self.axisWidget._widget._radioAxis._applyBut
        validate_btn.click()

        # wait until the axis windows expose (so scan should have been received)
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisListener.callCount() < 2:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis was never validated")

        timeout = TIMEOUT_TEST
        while timeout > 0 and self.ftseriesListener.callCount() < 2:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("ftserie never ended reconstruction")
        scan_2_tomwer_processes = os.path.join(self.scan_2_path, "tomwer_processes.h5")
        self.assertTrue(os.path.exists(scan_2_tomwer_processes))
        with h5py.File(scan_2_tomwer_processes, "r") as h5f:
            self.assertTrue("entry" in h5f)
            self.assertTrue("tomwer_process_0" in h5f["entry"])
            self.assertTrue("results" in h5f["entry"]["tomwer_process_0"])
            results = h5f["entry"]["tomwer_process_0"]["results"]
            self.assertTrue("center_of_rotation" in results)
            self.assertAlmostEqual(results["center_of_rotation"][()], -6.369)

        # 3.
        # lock the result
        self.axisWidget.setLockValue(True)
        self.mocks[2].end_acquisition()

        # wait until the axis windows expose (so scan should have been received)
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisListener.callCount() < 3:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis was never validated")

        timeout = TIMEOUT_TEST
        while timeout > 0 and self.ftseriesListener.callCount() < 3:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("ftserie never ended reconstruction")

        scan_3_tomwer_processes = os.path.join(self.scan_3_path, "tomwer_processes.h5")
        self.assertTrue(os.path.exists(scan_3_tomwer_processes))
        with h5py.File(scan_3_tomwer_processes, "r") as h5f:
            self.assertTrue("entry" in h5f)
            self.assertTrue("tomwer_process_0" in h5f["entry"])
            self.assertTrue("results" in h5f["entry"]["tomwer_process_0"])
            results = h5f["entry"]["tomwer_process_0"]["results"]
            self.assertTrue("center_of_rotation" in results)
            self.assertAlmostEqual(results["center_of_rotation"][()], -6.369)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestAxisFtseriesHDF5(OrangeWorflowTest):
    """Check the orange widget 'Axis' with an hdf5 scan"""

    """
    Create the following workflow:
    DataListOW -> DarkRefOW -> AxisOW -> nabuOW
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nodeDataList = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        cls.nodeDarkRef = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW",
        )
        cls.nodeAxis = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.AxisOW.AxisOW"
        )
        cls.nodeNabu = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuOW.NabuOW"
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nodeDataList, "data", cls.nodeDarkRef, "data")
        cls.link(cls, cls.nodeDarkRef, "data", cls.nodeAxis, "data")
        cls.link(cls, cls.nodeAxis, "data", cls.nodeNabu, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.dataListWidget = cls.getWidgetForNode(cls, cls.nodeDataList)
        cls.darkRefWidget = cls.getWidgetForNode(cls, cls.nodeDarkRef)
        cls.axisWidget = cls.getWidgetForNode(cls, cls.nodeAxis)
        cls.nabuWidget = cls.getWidgetForNode(cls, cls.nodeNabu)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nodeDataList, cls.nodeDarkRef, cls.nodeAxis, cls.nodeNabu):
            cls.removeNode(cls, node)
        cls.app.processEvents()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        self.root_dir = tempfile.mkdtemp()
        self.scan_1_path = os.path.join(self.root_dir, "scan1")
        self.scan_2_path = os.path.join(self.root_dir, "scan2")
        self.scan_3_path = os.path.join(self.root_dir, "scan3")
        scan_dirs = (self.scan_1_path, self.scan_2_path, self.scan_3_path)

        self.mocks = []
        self.scans = []
        for scan_dir in scan_dirs:
            mock = MockHDF5(scan_path=scan_dir, n_proj=20, n_ini_proj=20)
            assert os.path.exists(scan_dir)
            self.mocks.append(mock)
            self.scans.append(mock.scan)

        # set up axis, ftseries and data watcher
        for mock in self.mocks:
            self.dataListWidget.add(mock.scan)

        self.axisWidget._axis_params.mode = "manual"
        self.nabuWidget.setDryRun(True)
        # only ask for the creaation of the configuration file for the volume
        self.nabuWidget.setConfiguration({"tomwer_slices": None})

        # monkey patch exec_ to check behavior
        self.nabuWidget._replaceExec_()

        self.axisWidget._skip_exec(True)
        self.axisWidget.setModeLock("global")

        # create listeners
        self.axisListener = SignalListener()
        self.nabuListener = SignalListener()
        self.darkrefListener = SignalListener()

        # signal / slot connection
        self.axisWidget.sigScanReady.connect(self.axisListener)
        self.nabuWidget.sigScanReady.connect(self.nabuListener)
        self.darkRefWidget.sigScanReady.connect(self.darkrefListener)

    def tearDown(self) -> None:
        shutil.rmtree(self.root_dir)
        super().tearDown()

    def testScenario(self):
        """
        scenario:
        scan1, scan2 and scan 3 are all send to the pipeline
        DarkRef, axis, nabu.
        Lock the reconstruction method to global.
        Insure:
         - those widgets are able to work together
         - dark ref is created
         - axis is computed and value pass to nabu.
         - those processes update the tomwer_processes file
        """
        assert os.path.exists(self.scan_1_path)
        assert os.path.exists(self.scan_2_path)
        assert os.path.exists(self.scan_3_path)

        def _wait(timeout):
            timeout = timeout - 0.1
            self.app.processEvents()
            self.processOrangeEventsStack()
            time.sleep(0.1)
            return timeout

        for scan in self.scans:
            self.assertFalse(os.path.exists(scan.process_file))

        # 1. start workflow
        self.dataListWidget._sendList()

        # 2. check dark ref
        # wait until all scan pass dark ref process
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.darkrefListener.callCount() < 3:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("dark ref listener didn't received all the " "scans")

        # 2.1 make sure DarkRef process has been registered in tomwer_processes.h5
        # and a value has been saved and are valid
        for scan in self.scans:
            self.assertTrue(os.path.exists(scan.process_file))
            self.assertEqual(
                len(
                    DarkRefs.get_darks_frm_process_file(
                        process_file=scan.process_file, entry=scan.entry
                    )
                ),
                1,
            )
            self.assertEqual(
                len(
                    DarkRefs.get_flats_frm_process_file(
                        process_file=scan.process_file, entry=scan.entry
                    )
                ),
                1,
            )

        # 3. check axis
        # wait until all scan pass axis process
        timeout = TIMEOUT_TEST
        while timeout > 0 and self.axisListener.callCount() < 3:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("axis listener didn't received all the " "scans")
        # 3.1 make sure Axis process has been registered in tomwer_processes.h5
        # and a value has been saved
        for i_scan, scan in enumerate(self.scans):
            cor_value = AxisProcess.get_cor_frm_process_file(
                process_file=scan.process_file, entry=scan.entry
            )
            self.assertTrue(cor_value is not None)
            self.assertTrue(-scan.dim_1 / 2 <= cor_value <= scan.dim_1 / 2)

        # 4. check nabu
        # wait until all scan pass nabu process

        timeout = TIMEOUT_TEST
        while timeout > 0 and self.nabuListener.callCount() < 3:
            timeout = _wait(timeout)
        if timeout < 0:
            raise TimeoutError("nabu listener didn't received all the " "scans")

        # 4.1 make sure each scan contains now a nabu .cfg file
        for scan in self.scans:
            self.assertEqual(len(glob.glob(os.sep.join((scan.path, "*.cfg")))), 1)

        # 4.2 make sure Nabu process has been registered in tomwer_processes.h5
        for scan in self.scans:
            nabu_proc_rec = NabuSlices.get_process_frm_process_file(
                process_file=scan.process_file, entry=scan.entry
            )
            self.assertTrue(nabu_proc_rec is not None)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestAxisFtseriesEDF, TestAxisFtseriesHDF5):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
