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
contains gui relative frame difference display
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/09/2020"


import os
from silx.gui import qt
from silx.io.url import DataUrl
from silx.utils.enum import Enum as _Enum
from tomwer.gui.reconstruction.axis.CompareImages import CompareImages
from tomwer.io.utils import get_slice_data


class _FrameSelector(qt.QWidget):
    """Selector to select a frame from dark, flat, projection (normalized or
    not) and a reconstruction"""

    sigCorrectionChanged = qt.Signal()
    """signal emitted when the correction changed"""
    sigSelectedUrlChanged = qt.Signal()
    """signal emitted when the selected url changed"""

    class FrameType(_Enum):
        DARKS = "darks"
        FLATS = "flats"
        PROJ = "projections"
        ALIGN_PROJ = "alignment projections"
        RECON_SLICES = "slices reconstructed"

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._scan = None

        self.setLayout(qt.QFormLayout())
        self._frameTypeCB = qt.QComboBox(self)
        for frame_type in _FrameSelector.FrameType:
            self._frameTypeCB.addItem(frame_type.value)
        self.layout().addRow("frame type", self._frameTypeCB)
        self._frameUrlCB = qt.QComboBox(self)
        self.layout().addRow("frame", self._frameUrlCB)
        self._proj_normalized = qt.QCheckBox("corrected", self)
        self.layout().addRow("", self._proj_normalized)

        # connect signal / slot
        self._frameTypeCB.currentIndexChanged.connect(self._typeChanged)
        self._frameUrlCB.currentIndexChanged.connect(self._urlChanged)
        self._proj_normalized.toggled.connect(self._correctionChanged)

        # default settings
        self._proj_normalized.setChecked(True)
        index = self._frameTypeCB.findText(self.FrameType.PROJ.value)
        self._frameTypeCB.setCurrentIndex(index)

    def setScan(self, scan):
        self._scan = scan
        self._typeChanged()

    def getCurrentUrl(self):
        if self._frameUrlCB.currentText() != "":
            return DataUrl(path=self._frameUrlCB.currentData(qt.Qt.UserRole))
        else:
            return None

    def getTypeSelected(self):
        return self.FrameType.from_value(self._frameTypeCB.currentText())

    def _typeChanged(self, *args, **kwargs):
        type_selected = self.FrameType.from_value(self.getTypeSelected())
        self._proj_normalized.setVisible(
            type_selected in (self.FrameType.PROJ, self.FrameType.ALIGN_PROJ)
        )
        if self._scan is None:
            return

        urls = []
        self._frameUrlCB.clear()
        if type_selected == self.FrameType.DARKS:
            if self._scan._normed_darks is not None:
                urls = self._scan._normed_darks.values()
        elif type_selected == self.FrameType.FLATS:
            if self._scan._normed_flats is not None:
                urls = self._scan._normed_flats.values()
        elif type_selected == self.FrameType.PROJ:
            if self._scan.projections is not None:
                urls = self._scan.projections.values()
        elif type_selected == self.FrameType.ALIGN_PROJ:
            if self._scan.alignment_projections is not None:
                urls = self._scan.alignment_projections.values()
        elif type_selected == self.FrameType.RECON_SLICES:
            urls = self._scan.get_reconstructions_urls()
        else:
            raise ValueError("Type {} not managed".format(type_selected))
        urls = sorted(urls, key=lambda url: url.path())
        for url in urls:
            if url.data_slice() is not None:
                text = "?slice=".join(
                    (os.path.basename(url.file_path()), str(url.data_slice()[0]))
                )
            else:
                text = os.path.basename(url.file_path())
            user_data = url.path()
            self._frameUrlCB.addItem(text, user_data)

    def _urlChanged(self, *args, **kwargs):
        self.sigSelectedUrlChanged.emit()

    def _correctionChanged(self, *args, **kwargs):
        self.sigCorrectionChanged.emit()

    def needToNormalize(self):
        """

        :return: True if the data need to be treated by a dark and flat field
                 normalization.
        """
        return self._proj_normalized.isChecked() and self.getTypeSelected() in (
            self.FrameType.PROJ,
            self.FrameType.ALIGN_PROJ,
        )


class _FramesSelector(qt.QWidget):
    """Selector to select a frame from dark, flat, projection (normalized or
    not) and a reconstruction"""

    sigLeftFrameUpdateReq = qt.Signal()
    """signal emitted when a left frame update is requested"""
    sigRightFrameUpdateReq = qt.Signal()
    """signal emitted when a right frame update is requested"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._leftSelector = _FrameSelector(parent=self)
        self.layout().addWidget(self._leftSelector)
        self._rightSelector = _FrameSelector(parent=self)
        self.layout().addWidget(self._rightSelector)

        # TODO: add signal / slot connection
        self._leftSelector.sigCorrectionChanged.connect(self._leftFrameUpdReq)
        self._rightSelector.sigCorrectionChanged.connect(self._rightFrameUpdReq)
        self._leftSelector.sigSelectedUrlChanged.connect(self._leftFrameUpdReq)
        self._rightSelector.sigSelectedUrlChanged.connect(self._rightFrameUpdReq)

    def setScan(self, scan):
        self._leftSelector.setScan(scan)
        self._rightSelector.setScan(scan)

    def getLeftUrl(self):
        return self._leftSelector.getCurrentUrl()

    def needToNormalizeLeft(self):
        return self._leftSelector.needToNormalize()

    def needToNormalizeRight(self):
        return self._rightSelector.needToNormalize()

    def getRightUrl(self):
        return self._rightSelector.getCurrentUrl()

    def _rightFrameUpdReq(self):
        self.sigRightFrameUpdateReq.emit()

    def _leftFrameUpdReq(self):
        self.sigLeftFrameUpdateReq.emit()


class DiffFrameViewer(qt.QMainWindow):
    """
    Widget used to compare two frames using the silx CompareImages widget.

    User can select a reconstruction, a projection (normalized or not), flat
    or dark.
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self._scan = None

        self.setWindowFlags(qt.Qt.Widget)

        self._framesSelector = _FramesSelector(parent=self)
        self._framesSelectorDW = qt.QDockWidget(parent=self)
        self._framesSelectorDW.setWidget(self._framesSelector)
        self._framesSelectorDW.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.TopDockWidgetArea, self._framesSelectorDW)

        self._mainWidget = CompareImages(parent=self)
        self._mainWidget.setVisualizationMode(
            CompareImages.VisualizationMode.COMPOSITE_A_MINUS_B
        )

        self.setCentralWidget(self._mainWidget)

        # connect signal / slot
        self._framesSelector.sigRightFrameUpdateReq.connect(self._resetRightFrame)
        self._framesSelector.sigLeftFrameUpdateReq.connect(self._resetLeftFrame)

    def setScan(self, scan):
        self._scan = scan
        self._framesSelector.setScan(scan=scan)
        self._resetLeftFrame()
        self._resetRightFrame()

    def _resetLeftFrame(self):
        if self._scan is None:
            return
        url = self._framesSelector.getLeftUrl()
        if url is None:
            return
        data = get_slice_data(url)
        if self._framesSelector.needToNormalizeLeft():
            data = self._scan.flat_field_correction(
                data=data, index=self._scan.get_url_proj_index(url)
            )
        self._mainWidget.setImage1(data)

    def _resetRightFrame(self):
        if self._scan is None:
            return
        url = self._framesSelector.getRightUrl()
        if url is None:
            return
        data = get_slice_data(url)
        if self._framesSelector.needToNormalizeRight():
            data = self._scan.flat_field_correction(
                data=data, index=self._scan.get_url_proj_index(url)
            )
            pass
        self._mainWidget.setImage2(data)
