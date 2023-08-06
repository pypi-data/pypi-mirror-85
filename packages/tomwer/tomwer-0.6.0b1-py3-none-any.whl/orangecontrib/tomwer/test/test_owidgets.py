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
from tomwer.gui.qtapplicationmanager import QApplicationManager
from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.test.utils import skip_gui_test, skip_orange_workflows_test

logging.disable(logging.INFO)

app = QApplicationManager()


@unittest.skipIf(skip_orange_workflows_test(), reason="skip orange workflows tests")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestOrangeWidgetsCreations(OrangeWorflowTest):
    """Create dummy workflow to make sure orange widget are correctly created"""

    def setUp(self):
        OrangeWorflowTest.setUp(self)

    def tearDown(self):
        OrangeWorflowTest.tearDown(self)

    def test(self):
        """Simple creation of the following workflow:
        ScanList -> ScanSelector -> nameFilter -> sampleMoved
                                               -> stackSlice
        """
        dataListNode = self.addWidget(
            "orangecontrib.tomwer.widgets.control.DataListOW.DataListOW"
        )
        dataSelectorNode = self.addWidget(
            "orangecontrib.tomwer.widgets.control.DataSelectorOW.DataSelectorOW"
        )
        scanFilterNode = self.addWidget(
            "orangecontrib.tomwer.widgets.control.FilterOW.NameFilterOW"
        )
        sampleMovedNode = self.addWidget(
            "orangecontrib.tomwer.widgets.visualization.SampleMovedOW.SampleMovedOW"
        )
        groupSliceNode = self.addWidget(
            "orangecontrib.tomwer.widgets.visualization.SliceStackOW.SlicesStackOW"
        )

        self.processOrangeEvents()

        self.link(dataListNode, "data", dataSelectorNode, "data")
        self.link(dataSelectorNode, "data", scanFilterNode, "data")
        self.link(scanFilterNode, "data", sampleMovedNode, "data")
        self.link(scanFilterNode, "data", groupSliceNode, "data")
        self.processOrangeEvents()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestOrangeWidgetsCreations,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
