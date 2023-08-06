# /*##########################################################################
# Copyright (C) 20016-2017 European Synchrotron Radiation Facility
#
# This file is part of tomogui. Interface for tomography developed at
# the ESRF by the Software group.
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

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "15/09/2017"

import logging
from silx.gui import qt
from silx.gui.plot import PlotWidget
from typing import Union
from collections.abc import Iterable
import numpy

logger = logging.getLogger(__name__)


class QLineSelectorDialog(qt.QDialog):
    """
    The dialog used to select some slice indexes from a radio
    """

    def __init__(self, parent):
        qt.QDialog.__init__(self, parent=parent)
        self.__selection = None
        self.setLayout(qt.QVBoxLayout())
        self.setWindowTitle("select slices on radio")

        self.mainWidget = QLineSelector(parent=self)
        self.layout().addWidget(self.mainWidget)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        # connect signal / slots
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        # expose API
        self.setData = self.mainWidget.setData

    def setSelection(self, selection: Iterable):
        """

        :param rows: define the selection
        :type: Iterable
        """
        if type(selection) is str:
            selection = selection.replace("(", "")
            selection = selection.replace(")", "")
            selection = selection.replace(" ", "")
            selection = selection.replace(",", ";")
            self.__selection = []
            for val in selection.split(";"):
                try:
                    self.__selection.append(int(val))
                except ValueError:
                    pass
        else:
            self.__selection = selection

    def getSelection(self) -> tuple:
        """

        :return: the selection of slices to use
        :rtype: tuple
        """
        return self.__selection

    def exec_(self):
        if not self.mainWidget._has_data:
            mess = "no data set, can't use the selection tool"
            logger.warning(mess)
            qt.QMessageBox.warning(self, "Selection tool not available", mess)
            self.reject()
        else:
            self.mainWidget.setSelection(self.__selection)
            res = qt.QDialog.exec_(self)
            if res == qt.QDialog.Accepted:
                self.setSelection(self.mainWidget.getSelection())
            return res


class QLineSelector(qt.QWidget):
    """Widget to select a set of slices from a plot"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._plot = PlotWidget()
        # invert y axis
        self._plot.setYAxisInverted(True)
        self.__selection = {}
        # dict of markers from the user selection. Keys are item legend, value
        # are items
        self._has_data = False
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._plot)
        # connect signal / slot
        self._plot.sigPlotSignal.connect(self._plotDrawEvent)

    def setData(self, data: numpy.ndarray):
        """
        Define the data from which we can select slices

        :param data: data to plot
        :type: numpy.ndarray
        """
        self._has_data = True
        self._plot.addImage(data)
        assert self._plot.getActiveImage(just_legend=True) is not None

    def getSelection(self) -> tuple:
        """

        :return: the selection of slices to use
        :rtype: tuple
        """
        res = []
        for legend, marker in self.__selection.items():
            res.append(int(marker.getPoints()[0][1]))
        return tuple(sorted(res))

    def _clear(self):
        if len(self.__selection) > 0:
            self.removeSlice(list(self.__selection.keys())[0])
            self._clear()

    def setSelection(self, rows: Iterable) -> None:
        """

        :param rows: define the selection
        :type: Iterable
        """
        assert type(rows) is not str
        self._clear()
        if rows is not None:
            for row in rows:
                self.addSlice(row)

    def addSlice(self, row: Union[float, int]) -> None:
        """
        Add the requested slice to the selection

        :param row:
        :type; Union[float, int]
        """
        row_n = round(float(row))

        if self._plot.getActiveImage(just_legend=True) is not None:
            data_bounds = self._plot.getActiveImage(just_legend=False).getBounds()
            if not (data_bounds[0] <= row_n < data_bounds[1]):
                logger.warning("requested slice out of the data, ignored")
                return

        inf = 10000
        legend = self._getLegend(row_n=row_n)
        self._plot.addItem(
            xdata=numpy.array((-inf, -inf, inf, inf)),
            ydata=numpy.array((row_n, row_n + 1, row_n + 1, row_n)),
            shape="polygon",
            linewidth=1,
            color="pink",
            linestyle="-",
            fill=True,
            legend=legend,
        )
        self.__selection[legend] = self._plot._getItem(kind="item", legend=legend)

    def _getLegend(self, row_n) -> str:
        return str(round(float(row_n)))

    def removeSlice(self, row: Union[float, int]) -> None:
        """
        remove the requested slice from the selection

        :param row:
        :type; Union[float, int]
        """
        legend = self._getLegend(row_n=row)
        if legend in self.__selection:
            self._plot.removeItem(legend)
            del self.__selection[legend]

    def _plotDrawEvent(self, event):
        if "event" in event and event["event"] == "mouseClicked":
            row = event["y"] - 0.5

            if qt.QApplication.keyboardModifiers() & qt.Qt.ControlModifier:
                self.removeSlice(row=row)
            else:
                self.addSlice(row=row)


if __name__ == "__main__":
    app = qt.QApplication([])

    import numpy

    data = numpy.arange(50 * 50).reshape(50, 50)
    widget = QLineSelectorDialog(parent=None)
    widget.setData(data=data)
    widget.exec_()
