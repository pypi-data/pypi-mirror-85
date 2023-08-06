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
__date__ = "25/03/2019"


import os
import shutil
import tempfile
import unittest

from orangecontrib.tomwer.test.utils import OrangeWorflowTest

from tomwer.core.utils.scanutils import MockEDF
from tomwer.synctools.ftseries import _QDKRFRP, _QAxisRP, QReconsParams
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.reconstruction.darkref.params import Method as DkrfMethod
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test
import time

import logging
import logging

logging.disable(logging.INFO)

_logger = logging.getLogger(__name__)


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
@unittest.skip("Fail on CI...")
class TestReconstructionWidgets(OrangeWorflowTest):
    """Test behavior for several scans with the following scheme

        * DataSelector
        * DarkRefs orange widget (reconstruct both dark and flat)
        * Ftaxis orange widget
        * Ftseries orange widget

    Then process the workflow and check if the different values of ReconsParams
    are valid. And that in all case, pass all processes
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.dataSelectorNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW"
        )
        cls.darkRefNode = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW.DarkRefAndCopyOW",
        )
        cls.ftAxisNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.AxisOW.AxisOW"
        )
        cls.ftSeriesNode = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.FtseriesOW.FtseriesOW"
        )
        cls.processOrangeEvents(cls)

        cls.link(cls, cls.dataSelectorNode, "data", cls.darkRefNode, "data")
        cls.link(cls, cls.darkRefNode, "data", cls.ftAxisNode, "data")
        cls.link(cls, cls.ftAxisNode, "data", cls.ftSeriesNode, "data")
        cls.processOrangeEvents(cls)

        cls.dataSelectorWidget = cls.getWidgetForNode(cls, cls.dataSelectorNode)
        cls.darkRefWidget = cls.getWidgetForNode(cls, cls.darkRefNode)
        cls.axisWidget = cls.getWidgetForNode(cls, cls.ftAxisNode)
        cls.ftSeriesWidget = cls.getWidgetForNode(cls, cls.ftSeriesNode)

        # Set we only want to simulate the reconstruction
        cls.ftSeriesWidget._ftserie.reconsStack.setMockMode(True)
        cls.ftSeriesWidget._ftserie.setForceSync(True)
        cls.darkRefWidget.setForceSync(True)
        cls.axisWidget.setLocked(True)

    @classmethod
    def tearDownClass(cls):
        for node in (
            cls.dataSelectorNode,
            cls.darkRefNode,
            cls.ftAxisNode,
            cls.ftSeriesNode,
        ):
            cls.removeNode(cls, node)
        _logger.info("all nodes removed")
        cls.dataSelectorWidget = None
        cls.darkRefWidget = None
        cls.axisWidget = None
        cls.ftSeriesWidget = None
        OrangeWorflowTest.tearDownClass()

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        self._source_dir = tempfile.mkdtemp()

        def create_scan(folder_name):
            _dir = os.path.join(self._source_dir, folder_name)
            MockEDF.mockScan(scanID=_dir, nRadio=10, scan_range=180, n_extra_radio=2)
            return ScanFactory.create_scan_object(_dir)

        # tune scans
        # scan_1 has no reconstruction parameters
        self.scan_1 = create_scan("scan_1")
        # scan_2 has only dark_ref reconstructions parameters
        self.scan_2 = create_scan("scan_2")
        self.scan_2.ftseries_recons_params = QReconsParams(empty=True)
        self.scan_2.ftseries_recons_params.dkrf = _QDKRFRP()
        self.scan_2.ftseries_recons_params.dkrf.ref_calc_method = "None"
        # scan_3 has only ftaxis reconstructions parameters
        self.scan_3 = create_scan("scan_3")
        self.scan_3.ftseries_recons_params = QReconsParams(empty=False)
        self.scan_3.ftseries_recons_params.copy(self.scan_2.ftseries_recons_params.dkrf)
        # scan_4 has default reconstruction parameters
        self.scan_4 = create_scan("scan_4")
        self.scan_4.ftseries_recons_params = QReconsParams()
        self.scan_4.ftseries_recons_params.axis = _QAxisRP()
        self.scan_4.ftseries_recons_params.axis.to_the_center = False

        # tune processes
        self.darkRefWidget.recons_params.ref_calc_method = "Median"
        self.darkRefWidget.recons_params._set_skip_if_exist(False)
        self.axisWidget.recons_params.to_the_center = False
        self.axisWidget.recons_params.plot_figure = False

        # deactivate dark and ref copy
        self.darkRefWidget.widget._refCopyWidget.setChecked(False)

        self.ftSeriesWidget.recons_params.ref_calc_method = "Average"
        self.ftSeriesWidget.recons_params.dkrf._set_skip_if_exist(True)
        self.ftSeriesWidget.recons_params.plot_figure = True
        self.ftSeriesWidget.recons_params.to_the_center = True

        self._scans = (self.scan_1, self.scan_2, self.scan_3, self.scan_4)
        for _scan in self._scans:
            self.dataSelectorWidget.addScan(_scan)
        self.app.processEvents()

        # skip axis pop up
        self.axisWidget._skip_exec(True)

    def tearDown(self):
        shutil.rmtree(self._source_dir)
        OrangeWorflowTest.tearDown(self)

    def testProcessing(self):
        """Test the different values of reconstruction parameters during the
        workflow execution"""
        # validate all scans
        for _scan in self._scans:
            self.app.processEvents()
            assert isinstance(_scan, TomwerScanBase)
            self.dataSelectorWidget.setActiveScan(_scan)

            # emit scan to the be managed by darkref
            self.dataSelectorWidget.widget._selectActiveScan()
            self.processOrangeEventsStack()

            # here we are in darkrefs. Recons params should be copy from darkref
            # to scan.ftseries_recons_params
            self.assertTrue(
                self.darkRefWidget.recons_params.ref_calc_method is DkrfMethod.median
            )
            self.assertTrue(
                _scan.ftseries_recons_params.dkrf.ref_calc_method is DkrfMethod.median
            )
            self.assertTrue(self.darkRefWidget.recons_params.overwrite_ref is True)
            self.assertTrue(_scan.ftseries_recons_params.dkrf.overwrite_ref is True)
            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))
            self.assertTrue(isinstance(_scan.ftseries_recons_params.dkrf, _QDKRFRP))

            for t in range(0, 5):
                time.sleep(0.1)
                self.processOrangeEventsStack()
                self.app.processEvents()

            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))

            # here we are in ftaxis. Axis parameters should also be copied from
            # AxisOW.recons_params to TomoBase.ftseries_recons_params.axis
            self.assertTrue(self.axisWidget.recons_params.plot_figure is False)
            self.assertTrue(isinstance(_scan.ftseries_recons_params, QReconsParams))
            self.processOrangeEventsStack()

            # here we are in ftseries. ftseries copy parameters from axis and
            # dkrf if any.
            self.assertTrue(
                self.ftSeriesWidget.recons_params.dkrf.ref_calc_method
                is DkrfMethod.median
            )
            self.assertTrue(
                _scan.ftseries_recons_params.dkrf.ref_calc_method is DkrfMethod.median
            )
            self.assertTrue(
                self.ftSeriesWidget.recons_params.dkrf.overwrite_ref is True
            )
            self.assertTrue(_scan.ftseries_recons_params.dkrf.overwrite_ref is True)
            self.app.processEvents()

        while self.app.hasPendingEvents():
            self.app.processEvents()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReconstructionWidgets,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
