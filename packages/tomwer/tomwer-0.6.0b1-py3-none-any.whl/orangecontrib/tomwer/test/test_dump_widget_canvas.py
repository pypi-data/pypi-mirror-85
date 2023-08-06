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
__date__ = "28/01/2019"

import logging
import unittest

from orangecontrib.tomwer.test.utils import OrangeWorflowTest
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.test.utils import skip_gui_test

logging.disable(logging.INFO)

app = QApplicationManager()


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestDumpWidgets(OrangeWorflowTest):
    """
    simply create orange widgets in the orange canvas to make instances
    of those are made correctly
    """

    def testTimer(self):
        timer_node = self.addWidget(
            "orangecontrib.tomwer.widgets.control.TimerOW.TimerOW"
        )
        self.processOrangeEventsStack()
        timer_widget = self.getWidgetForNode(timer_node)
        self.assertTrue(timer_widget is not None)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDumpWidgets,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
