# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "29/05/2017"


import unittest
from . import test_conditions
from . import test_control_flow
from . import test_darkref
from . import test_data_listener
from . import test_datawatcher
from . import test_foldertransfert
from . import test_ftseries
from . import test_reconstruction
from . import test_scanvalidator
from . import test_viewer
from ..reconstruction.test import suite as reconstruction_suite
from ..control.test import suite as control_suite


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        [
            test_conditions.suite(),
            test_control_flow.suite(),
            test_darkref.suite(),
            test_data_listener.suite(),
            test_foldertransfert.suite(),
            test_ftseries.suite(),
            test_reconstruction.suite(),
            test_scanvalidator.suite(),
            test_datawatcher.suite(),
            test_viewer.suite(),
            reconstruction_suite(),
            control_suite(),
        ]
    )
    return test_suite
