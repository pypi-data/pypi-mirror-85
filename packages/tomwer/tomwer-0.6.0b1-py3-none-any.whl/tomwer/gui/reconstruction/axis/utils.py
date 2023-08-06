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
"""
contains gui relative to axis calculation using sinogram
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "25/05/2020"


from contextlib import ContextDecorator


class _RadioSinoLocker(ContextDecorator):
    """Simple cntextManager for the radio and sinogram axis synchronization"""

    def __init__(self, parent):
        self.__parent = parent
        self.old_radio = None
        self.old_sinogram = None
        self.__locked = False

    def __enter__(self):
        self.old_radio = self.radioAxis.blockSignals(True)
        self.old_sinogram = self.sinogramAxis.blockSignals(True)

    @property
    def radioAxis(self):
        return self.__parent._radioAxis

    @property
    def sinogramAxis(self):
        return self.__parent._sinogramAxis

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.radioAxis.blockSignals(self.old_radio)
        self.sinogramAxis.blockSignals(self.old_sinogram)

    def isLocked(self):
        return self.__locked

    def setLocked(self, locked):
        if locked == self.__locked:
            return
        else:
            self.__locked = locked
            # block widgets signals
            with self:
                self.radioAxis.setLocked(locked)
                self.sinogramAxis.setLocked(locked)
