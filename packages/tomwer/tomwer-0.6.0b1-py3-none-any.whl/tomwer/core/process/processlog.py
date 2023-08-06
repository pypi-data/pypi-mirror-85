# coding: utf-8
# ##########################################################################
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
# ###########################################################################
"""
Simple logs levels definition relative to process status
"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/09/2017"

import logging


PROCESS_ENDED_LEVEL = 35
PROCESS_SKIPPED_LEVEL = 36

logging.addLevelName(PROCESS_ENDED_LEVEL, "PROCESS_ENDED")
logging.addLevelName(PROCESS_SKIPPED_LEVEL, "PROCESS_SKIPPED")


def processEnded(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(PROCESS_ENDED_LEVEL):
        self._log(PROCESS_ENDED_LEVEL, message, args, **kws)


def processSkipped(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(PROCESS_SKIPPED_LEVEL):
        self._log(PROCESS_SKIPPED_LEVEL, message, args, **kws)


logging.Logger.processEnded = processEnded
logging.Logger.processSkipped = processSkipped
