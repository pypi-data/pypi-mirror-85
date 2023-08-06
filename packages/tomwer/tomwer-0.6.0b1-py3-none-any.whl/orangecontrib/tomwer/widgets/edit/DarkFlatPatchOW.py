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
__date__ = "02/11/2020"


from Orange.widgets.widget import Input, Output
from Orange.widgets import widget, gui
from tomwer.web.client import OWClient
from tomwer.gui.edit.dkrfpatch import DarkRefPatchWidget
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.synctools.stacks.edit.darkflatpatch import DarkFlatPatchProcessStack
from ..utils import WidgetLongProcessing
import logging

_logger = logging.getLogger(__name__)


class DarkFlatPatchOW(widget.OWWidget, OWClient, WidgetLongProcessing):
    """
    Widget to define on the fly the image_key of a HDF5TomoScan
    """

    name = "dark-flat-patch"
    id = "orange.widgets.tomwer.edit.DarkFlatPatchOW.DarkFlatPatchOW"
    description = "Interface to patch dark and flat to an existing NXTomo" "entry"
    icon = "icons/patch_dark_flat.svg"
    priority = 25
    category = "esrfWidgets"
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "dark",
        "patch",
        "ref",
    ]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data_out = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self)
        WidgetLongProcessing.__init__(self)
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._processingStack = DarkFlatPatchProcessStack(self)

        self.widget = DarkRefPatchWidget(parent=self)
        layout.addWidget(self.widget)

        # connect signal / slot
        self._processingStack.sigComputationStarted.connect(self._startProcessing)
        self._processingStack.sigComputationEnded.connect(self._endProcessing)

    @Inputs.data_in
    def process(self, scan):
        if scan is None:
            return
        elif not isinstance(scan, HDF5TomoScan):
            _logger.error("We can only patch dark and flat for HDF5TomoScan")
        else:
            self._processingStack.add(scan, self.getConfiguration())

    def getConfiguration(self):
        return {
            "darks_start": self.widget.getStartDarkUrl(),
            "flats_start": self.widget.getStartFlatUrl(),
            "darks_end": self.widget.getEndDarkUrl(),
            "flats_end": self.widget.getEndFlatUrl(),
        }

    def _endProcessing(self, scan):
        WidgetLongProcessing._endProcessing(self, scan)
        if scan is not None:
            self.Outputs.data_out.send(scan)
