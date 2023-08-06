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
__date__ = "11/03/2020"

from silx.gui import qt
from Orange.widgets import widget, gui
from tomwer.gui.control.datalist import BlissHDF5DataListDialog
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.web.client import OWClient
from tomwer.core.process.control.nxtomomill import NxTomomillProcess
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Output, Input
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.blissscan import BlissScan
from nxtomomill import converter as nxtomomill_converter
import os
import logging

logger = logging.getLogger(__name__)


class InputDialogWithCache(qt.QDialog):
    """
    Input dialog for get missing information for nxtomomill translation
    Identical to a default QInputDialog adding a CheckBox to store answer.
    """

    def __init__(self, parent, scan, title="", desc="", cache_answer=True):
        qt.QDialog.__init__(self, parent)
        self.setWindowFlags(qt.Qt.MSWindowsFixedSizeDialogHint)

        self.setWindowTitle(title)
        self.setLayout(qt.QGridLayout())

        # entry
        self.layout().addWidget(qt.QLabel("entry:", self), 0, 0, 1, 1)
        self._entryQLE = qt.QLineEdit(scan.entry if scan else "", self)
        self._entryQLE.setReadOnly(True)
        self.layout().addWidget(self._entryQLE, 0, 1, 1, 1)

        # file name
        self.layout().addWidget(qt.QLabel("file:", self), 1, 0, 1, 1)
        self._fileQLE = qt.QLineEdit(scan.master_file if scan else "", self)
        self._fileQLE.setReadOnly(True)
        self.layout().addWidget(self._fileQLE, 1, 1, 1, 1)

        # label message
        self._label = qt.QLabel(desc, self)
        self.layout().addWidget(self._label, 2, 0, 1, 2)

        # input QLineEdit
        self._input = qt.QLineEdit("", self)
        self.layout().addWidget(self._input, 3, 0, 1, 2)

        # cache combobox
        self._cacheAnswerCB = qt.QCheckBox("keep answer in cache", self)
        self._cacheAnswerCB.setToolTip(
            "Will keep in memory the answer for the"
            " 'current cycle'. A cycle starts when "
            "you press 'send all' or "
            "'send selected' and ends when the last"
            " scan as been converted. The cache is "
            "reset after each cycle"
        )
        font = self._cacheAnswerCB.font()
        font.setPixelSize(10)
        self._cacheAnswerCB.setFont(font)
        self.layout().addWidget(self._cacheAnswerCB, 4, 0, 1, 1)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 5, 0, 1, 1)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons.setStandardButtons(types)

        self.layout().addWidget(self._buttons, 4, 0, 1, 2)

        # set up
        self._cacheAnswerCB.setChecked(cache_answer)

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)

    def setLabelText(self, txt):
        self._label.setText(txt)

    def getText(self):
        return self._input.text()

    def setScan(self, entry, file_path):
        self._entryQLE.setText(entry)
        self._fileQLE.setText(file_path)

    def cache_answer(self):
        return self._cacheAnswerCB.isChecked()

    def setBlissScan(self, entry, file_path):
        self._fileQLE.setText(file_path)
        self._entryQLE.setText(entry)

    def clear(self):
        self.setWindowTitle("")
        self._label.setText("")
        self._input.setText("")


class _NXTomomillInput:
    """
    callback provided to nxtomomill if an entry is missing.
    The goal is to ask the user the missing informations

    :param str entry: name of the entry missing
    :param str desc: description of the entry
    :return: user input or None
    """

    def __init__(self, parent=None, scan=None):
        self._dialog = InputDialogWithCache(parent=None, scan=scan)
        self._cache = {}
        """Cache to be used the user want to uase back answer for some question
        """

    def exec_(self, field, desc):
        self._dialog.clear()
        self._dialog.setWindowTitle(field)
        self._dialog.setLabelText(desc)

        if field in self._cache:
            return self._cache[field]
        else:
            if self._dialog.exec_():
                answer = self._dialog.getText()
                if self._dialog.cache_answer():
                    self._cache[field] = answer
                return answer
            else:
                return None

    def setBlissScan(self, entry, file_path):
        self._dialog.setScan(entry=entry, file_path=file_path)

    __call__ = exec_


class _OverwriteMessage(qt.QDialog):
    def __init__(self, parent, message=""):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self._label = qt.QLabel(message, self)
        self.layout().addWidget(self._label, 0, 0, 1, 2)

        self._canOverwriteAllCB = qt.QCheckBox("overwrite all", self)
        self._canOverwriteAllCB.setToolTip(
            "Will keep in memory the right to overwrite nxtomomill output "
            "files for the 'current cycle'. A cycle starts when you press "
            "'send all' or 'send selected' and ends when the last scan as been"
            " converted. The cache is reset after each cycle"
        )
        font = self._canOverwriteAllCB.font()
        font.setPixelSize(10)
        self._canOverwriteAllCB.setFont(font)
        self.layout().addWidget(self._canOverwriteAllCB, 2, 0, 1, 1)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 3, 0, 1, 1)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.No
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons, 8, 0, 1, 1)

        # signal / slot connection
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.No).clicked.connect(self.reject)

    def setText(self, msg):
        self._label.setText(msg)

    def canOverwriteAll(self):
        return self._canOverwriteAllCB.isChecked()


class NXTomomillOW(widget.OWWidget, OWClient):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "nxtomomill"
    id = "orange.widgets.tomwer.control.NXTomomillOW.NXTomomillOW"
    description = (
        "Read a bliss .h5 file and extract from it all possible"
        "NxTomo. When validated create a TomwerBaseScan for each "
        "file and entry"
    )
    icon = "icons/nxtomomill.svg"
    priority = 120
    category = "esrfWidgets"
    keywords = ["hdf5", "nexus", "tomwer", "file", "convert", "NXTomo", "tomography"]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    _scans = Setting(list())

    class Inputs:
        data_in = Input(
            name="bliss data", type=BlissScan, doc="bliss scan to be process"
        )

    class Outputs:
        data_out = Output(
            name="data", type=TomwerScanBase, doc="one scan to be process"
        )

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self)
        self.widget = BlissHDF5DataListDialog(parent=self)
        self.widget.setScanIDs(self._scans)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        self.widget._sendButton.clicked.connect(self._sendAll)
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.__request_input = True
        # do we ask the user for input if missing
        self._inputGUI = None
        """Gui with cache for missing field in files to be converted"""
        self._canOverwriteOutputs = False
        """Cache to know if we have to ask user permission for overwriting"""

        # expose API
        self.add = self.widget.add
        self.n_scan = self.widget.n_scan

        # alias used for the 'simple workflow' for now
        self.start = self._sendAll

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def _sendSelected(self):
        """Send a signal for selected scans found to the next widget"""
        self._inputGUI = _NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            entry, file_path = bliss_url.text().split("@")
            self._inputGUI.setBlissScan(entry=entry, file_path=file_path)
            self._process(bliss_url.text())

    def _sendAll(self):
        """Send a signal for each scan found to the next widget"""
        self._inputGUI = _NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.items:
            entry, file_path = bliss_url.split("@")
            self._inputGUI.setBlissScan(entry=entry, file_path=file_path)
            self._process(bliss_url)

    def _process(self, bliss_url):
        """

        :param str bliss_url: string at entry@file format
        """
        logger.processStarted("Start translate {} to NXTomo".format(str(bliss_url)))

        entry, file_path = bliss_url.split("@")
        bliss_scan = BlissScan(master_file=file_path, entry=entry, proposal_file=None)
        self.treatBlissScan(bliss_scan=bliss_scan)

    def _userAgreeForOverwrite(self, file_path):
        if self._canOverwriteOutputs:
            return True
        else:
            msg = _OverwriteMessage(self)
            text = "NXtomomill will overwrite \n %s. Do you agree ?" % file_path
            msg.setText(text)
            if msg.exec_():
                self._canOverwriteOutputs = msg.canOverwriteAll()
                return True
            else:
                return False

    @Inputs.data_in
    def treatBlissScan(self, bliss_scan):
        if bliss_scan is None:
            return
        output_file_path = NxTomomillProcess.deduce_output_file_path(
            bliss_scan.master_file, entry=bliss_scan.entry
        )
        if os.path.exists(output_file_path):
            if not self._userAgreeForOverwrite(output_file_path):
                return
        try:
            conv = nxtomomill_converter.h5_to_nx(
                input_file_path=bliss_scan.master_file,
                output_file=output_file_path,
                entries=(bliss_scan.entry,),
                single_file=True,
                ask_before_overwrite=False,
                request_input=self.request_input,
                file_extension=".nx",
                input_callback=self._inputGUI,
                show_progress=False,
            )
        except Exception as e:
            logger.processFailed(
                "Fail to convert from bliss file: %s to NXTomo."
                "Conversion error is: %s" % (bliss_scan, e)
            )
        else:
            if len(conv) != 1:
                logger.processFailed(
                    "Something went wrong during file conversion. "
                    "Unable to process the file {}."
                    "".format(bliss_scan.master_file)
                )
            else:
                conv_file, conv_entry = conv[0]
                scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
                logger.processSucceed(
                    "{} has been translated to {}" "".format(bliss_scan, scan_converted)
                )
                self.Outputs.data_out.send(scan_converted)
