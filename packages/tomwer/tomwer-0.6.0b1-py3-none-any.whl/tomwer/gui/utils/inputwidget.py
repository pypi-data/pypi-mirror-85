# coding: utf-8
# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
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
__date__ = "16/08/2018"

from silx.gui import qt
from tomwer.gui import icons
import numpy
import logging

_logger = logging.getLogger(__name__)


class SelectionLineEdit(qt.QWidget):
    """Line edit with several type of selection possible:

    * a single value
    * a range of value on the type min:max:step
    * a list of value: val1, val2, ...
    """

    # SINGLE_MODE = 'single'
    RANGE_MODE = "range"
    LIST_MODE = "list"

    # SELECTION_MODES = (SINGLE_MODE, RANGE_MODE, LIST_MODE)
    SELECTION_MODES = (RANGE_MODE, LIST_MODE)

    _DEFAULT_SELECTION = LIST_MODE

    def __init__(self, text=None, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._qLineEdit = qt.QLineEdit(parent=self)
        fpm = "\\d*\\.?\\d+"  # float or int matching
        qRegExp = qt.QRegExp(
            "(" + fpm + "[;]?[,]?[ ]?){1,}" + "|" + ":".join((fpm, fpm, fpm))
        )
        self._qLineEdit.setValidator(qt.QRegExpValidator(qRegExp))
        self.layout().addWidget(self._qLineEdit)
        self._button = SelectionModeButton(parent=self)
        self.layout().addWidget(self._button)

        # Qobject signal connections
        self._qLineEdit.textChanged.connect(self._checkIfModeChanged)
        self._button.sigModeChanged.connect(self._modeChanged)

        # expose API
        self.setText = self._qLineEdit.setText
        self.editingFinished = self._qLineEdit.editingFinished
        self.textChanged = self._qLineEdit.textChanged
        self.text = self._qLineEdit.text

        if text is not None:
            self._qLineEdit.setText(str(text))

    def getMode(self):
        return self._button.mode

    @property
    def selection(self):
        if self._qLineEdit.hasAcceptableInput():
            if self._button.mode == self.RANGE_MODE:
                _from, _to, _step = self._qLineEdit.text().split(":")
                _from, _to, _step = float(_from), float(_to), float(_step)
                if _from > _to:
                    _logger.warning("to > from, invert %s and %s" % (_from, _to))
                    tmp = _to
                    _to = _from
                    _from = tmp
                num = int((_to - _from) / _step)
                return tuple(
                    numpy.linspace(start=_from, stop=_to, num=num, endpoint=True)
                )
            else:
                vals = self._qLineEdit.text().replace(" ", "")
                vals = vals.replace(";", ",").split(",")
                res = []
                [res.append(float(val)) for val in vals]
                if len(res) == 1:
                    return res[0]
                else:
                    return tuple(res)
        else:
            _logger.warning("Wrong input, unvalid selection")
            return None

    def _checkIfModeChanged(self, _str):
        self._button.blockSignals(True)
        if _str.count(":") > 0:
            self._button.mode = self.RANGE_MODE
        else:
            self._button.mode = self.LIST_MODE
        self._button.blockSignals(False)

    def _modeChanged(self, mode):
        if mode == self.RANGE_MODE:
            text = "from:to:step"
        elif mode == self.LIST_MODE:
            text = "val1; val2; ..."
        else:
            raise ValueError("unknow mode")

        self._qLineEdit.blockSignals(True)
        self._qLineEdit.setText(text)
        self._qLineEdit.selectAll()
        self._qLineEdit.blockSignals(False)


class SelectionModeButton(qt.QToolButton):
    """Base class for Selection QAction.

    :param str mode: the mode of selection of the action.
    :param str text: The name of this action to be used for menu label
    :param str tooltip: The text of the tooltip
    :param triggered: The callback to connect to the action's triggered
                      signal or None for no callback.
    """

    sigModeChanged = qt.Signal(str)

    def __init__(self, parent=None, tooltip=None, triggered=None):
        qt.QToolButton.__init__(self, parent)
        self._states = {}
        self._mode = None
        for mode in SelectionLineEdit.SELECTION_MODES:
            icon = icons.getQIcon("_".join([mode, "selection"]))
            self._states[mode] = (icon, self._getTooltip(mode))

        self._rangeAction = RangeSelAction(parent=self)
        self._listAction = ListSelAction(parent=self)
        for _action in (self._rangeAction, self._listAction):
            _action.sigModeChanged.connect(self._modeChanged)

        menu = qt.QMenu(self)
        menu.addAction(self._rangeAction)
        menu.addAction(self._listAction)
        self.setMenu(menu)
        self.setPopupMode(qt.QToolButton.InstantPopup)
        self.mode = SelectionLineEdit.LIST_MODE

    def _getTooltip(self, mode):
        # if mode == SelectionLineEdit.SINGLE_MODE:
        #     return 'Define only one value for this parameter'
        if mode == SelectionLineEdit.LIST_MODE:
            return (
                "Define a single value or a list of values for this "
                "parameter (va1; val2)"
            )
        elif mode == SelectionLineEdit.RANGE_MODE:
            return "Define a range of value for this parameter (from:to:step)"
        else:
            raise ValueError("unknow mode")

    def _modeChanged(self, mode):
        self.mode = mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        assert mode in SelectionLineEdit.SELECTION_MODES
        if mode != self._mode:
            self._mode = mode
            self.setIcon(icons.getQIcon("_".join([mode, "selection"])))
            self.setToolTip(self._getTooltip(mode))
            self.sigModeChanged.emit(self._mode)


class SelectionAction(qt.QAction):
    """
    Base class of the several selection mode
    """

    sigModeChanged = qt.Signal(str)

    def __init__(self, mode, parent, text):
        icon = icons.getQIcon("_".join([mode, "selection"]))
        qt.QAction.__init__(self, icon, text, parent)
        self.setIconVisibleInMenu(True)
        self._mode = mode
        self.triggered.connect(self._modeChanged)

    def _modeChanged(self, *args, **kwargs):
        self.sigModeChanged.emit(self._mode)


class RangeSelAction(SelectionAction):
    """
    Action to select a range of element on the scheme from:to:step
    """

    def __init__(self, parent=None):
        SelectionAction.__init__(
            self,
            mode=SelectionLineEdit.RANGE_MODE,
            parent=parent,
            text="range selection",
        )


class ListSelAction(SelectionAction):
    """
    Action to select a list of element on the scheme elmt1, elmt2, ...
    """

    def __init__(self, parent=None):
        SelectionAction.__init__(
            self, mode=SelectionLineEdit.LIST_MODE, parent=parent, text="list selection"
        )


if __name__ == "__main__":
    qpp = qt.QApplication([])
    w = SelectionLineEdit(None)
    w.show()
    qpp.exec_()
