# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "15/05/2017"


from tomwer.test.utils import skip_gui_test
import unittest
from ..core import test as test_core
from ..app import test as test_app

if skip_gui_test() is False:
    from ..gui import test as test_gui
    from ..synctools import test as test_synctools
    from . import test_scripts


def suite(loader=None):
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_core.suite())
    test_suite.addTest(test_app.suite())
    if skip_gui_test() is False:
        test_suite.addTest(test_synctools.suite())
        test_suite.addTest(test_gui.suite())
        test_suite.addTest(test_scripts.suite())

    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
