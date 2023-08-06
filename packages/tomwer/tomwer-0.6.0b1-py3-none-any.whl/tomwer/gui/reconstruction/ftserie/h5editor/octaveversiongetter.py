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
__date__ = "15/06/2017"

from silx.gui import qt


class OctaveVersionGetter(qt.QGroupBox):
    """Simple class to set the octave version"""

    # bad hack : should be a boolean and not a string. Because we are looking
    # only if bellow 3.8 or not
    valueHasChanged = qt.Signal(float)

    def __init__(self, title, parent=None):
        """

        :param str title: the name of the groupbox
        :param QObject parent: the QObject parent of the GroupBox
        """
        qt.QGroupBox.__init__(self, title=title, parent=parent)
        self.setLayout(qt.QHBoxLayout())

        self._qrbInf3_8 = qt.QRadioButton("version < 3.8", parent=self)
        self._qrbInf3_8.setChecked(True)
        self.layout().addWidget(self._qrbInf3_8)
        self._qrbInf3_8.toggled.connect(self.valueChanged)
        self._qrbSup3_8 = qt.QRadioButton("version >= 3.8", parent=self)
        self.layout().addWidget(self._qrbSup3_8)
        self._qrbSup3_8.toggled.connect(self.valueChanged)

    def setVersionInf3_8(self, b):
        """

        :param boolean b: if true then target the octave version < 3.8
        """
        if b:
            self._qrbInf3_8.setChecked(True)
        else:
            self._qrbSup3_8.setChecked(True)

    def isVersionInf3_8(self):
        """
        :return: True if the octave version we are trying to load is oldest
            than 3.8
        """
        return self._qrbInf3_8.isChecked()

    def valueChanged(self):
        self.valueHasChanged.emit(3.6 if self.isVersionInf3_8() else 3.8)
