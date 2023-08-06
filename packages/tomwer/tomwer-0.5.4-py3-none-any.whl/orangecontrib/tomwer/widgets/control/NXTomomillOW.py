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
from tomwer.core.utils import logconfig
from tomwer.gui.control.datalist import HDF5DataListDialog
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.web.client import OWClient
from tomwer.core.process.nxtomomill import NxTomomillProcess
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Output
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.blissscan import BlissScan
from nxtomomill import converter as nxtomomill_converter
import os
import logging
logger = logging.getLogger(__name__)


def _nxtomomill_input_callback(entry, desc):
    """
    callback provided to nxtomomill if an entry is missing.
    The goal is to ask the user the missing informations

    :param entry:
    :param desc:
    :return:
    """
    text, ok_pressed = qt.QInputDialog.getText(None, 'fill missing entry {}'.format(entry),
                                               desc)

    if ok_pressed:
        return text
    else:
        return None


class NXTomomillOW(widget.OWWidget, OWClient):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """
    name = "nxtomomill"
    id = "orange.widgets.tomwer.control.NXTomomillOW.NXTomomillOW"
    description = "Read a bliss .h5 file and extract from it all possible" \
                  "NxTomo. When validated create a TomwerBaseScan for each " \
                  "file and entry"
    icon = "icons/nxtomomill.svg"
    priority = 120
    category = "esrfWidgets"
    keywords = ["hdf5", "nexus", "tomwer", 'file', "convert", "NXTomo",
                "tomography"]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    _scans = Setting(list())

    class Outputs:
        data_out = Output(name='data',
                          type=TomwerScanBase,
                          doc='one scan to be process')

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self)
        self.widget = HDF5DataListDialog(parent=self)
        self.widget.setScanIDs(self._scans)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        self.widget._sendButton.clicked.connect(self._sendList)
        self.__request_input = True
        # do we ask the user for input if missing

        # expose API
        self.add = self.widget.add
        self.n_scan = self.widget.n_scan

        # alias used for the 'simple workflow' for now
        self.start = self._sendList

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def _sendList(self):
        """Send a signal for each list to the next widget"""
        for bliss_url in self.widget.datalist.items:
            logger.processStarted(
                'Start translate {} to NXTomo'.format(str(bliss_url)))

            entry, file_path = bliss_url.split('@')
            bliss_scan = BlissScan(master_file=file_path, entry=entry,
                                   proposal_file=None)
            output_file_path = NxTomomillProcess.deduce_output_file_path(file_path, entry=entry)

            if os.path.exists(output_file_path):
                if not self._userAgreeForOverwrite(output_file_path):
                    continue
            try:
                conv = nxtomomill_converter.h5_to_nx(input_file_path=file_path,
                                                     output_file=output_file_path,
                                                     entries=(entry,),
                                                     single_file=True,
                                                     ask_before_overwrite=False,
                                                     request_input=self.request_input,
                                                     file_extension='.nx',
                                                     input_callback=_nxtomomill_input_callback)
            except Exception as e:
                logger.processFailed(
                    'Fail to convert from bliss file: %s to NXTomo. '
                    'Conversion error is: %s' % (bliss_url, e))
            else:
                if len(conv) != 1:
                    logger.processFailed(
                        'Something went wrong during file conversion. '
                        'Unable to process the file.')
                else:
                    conv_file, conv_entry = conv[0]
                    scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
                    mess = '{} has been translated to {}' \
                           ''.format(str(bliss_scan), str(scan_converted))
                    logger.processSucceed(mess)
                    self.Outputs.data_out.send(scan_converted)

    def _userAgreeForOverwrite(self, file_path):
        msg = qt.QMessageBox(self)
        msg.setIcon(qt.QMessageBox.Question)
        types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
        msg.setStandardButtons(types)
        text = "NXtomomill will overwrite \n %s. Do you agree ?" % file_path
        msg.setText(text)
        return msg.exec_() == qt.QMessageBox.Ok
