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
__date__ = "13/08/2020"

import logging
import unittest
from tomwer.test.utils import skip_gui_test
from orangecontrib.tomwer.test.utils import OrangeWorflowTest

logging.disable(logging.INFO)


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestVolumeWidget(OrangeWorflowTest):
    """Insure connection of the following widgets:

    - NabuOW
    - NabuVolumeOW
    - VolumeViewerOW
    """

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        cls.nabuSlice = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuOW.NabuOW"
        )
        cls.nabuVolume = cls.addWidget(
            cls, "orangecontrib.tomwer.widgets.reconstruction.NabuVolumeOW.NabuVolumeOW"
        )
        cls.volumeViewer = cls.addWidget(
            cls,
            "orangecontrib.tomwer.widgets.visualization.VolumeViewerOW.VolumeViewerOW",
        )

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # linking the workflow
        cls.link(cls, cls.nabuSlice, "data", cls.nabuVolume, "data")
        cls.link(cls, cls.nabuVolume, "data", cls.volumeViewer, "data")

        # Let Orange process events (node creations)
        cls.processOrangeEvents(cls)

        # getting the widgets
        cls.nabuSliceWidget = cls.getWidgetForNode(cls, cls.nabuSlice)
        cls.nabuVolumeWidget = cls.getWidgetForNode(cls, cls.nabuVolume)
        cls.volumeViewerWidget = cls.getWidgetForNode(cls, cls.volumeViewer)

    @classmethod
    def tearDownClass(cls):
        for node in (cls.nabuSlice, cls.nabuVolume, cls.volumeViewer):
            cls.removeNode(cls, node)
        del cls.nabuSlice
        del cls.nabuVolume
        del cls.volumeViewer
        OrangeWorflowTest.tearDownClass()

    def testWorkflow(self):
        """Test construction is possible (in fact test is on the setUpClass
        part for now)"""
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestVolumeWidget,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
