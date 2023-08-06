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
__date__ = "04/03/2019"


from ..utils import WidgetLongProcessing
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from Orange.widgets.widget import Input, Output
from tomwer.synctools.stacks.reconstruction.axis import AxisProcessStack
from tomwer.core.process.reconstruction.axis import AxisProcess
from tomwer.synctools.axis import QAxisRP
from tomwer.gui.reconstruction.axis import AxisWindow
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from silx.gui import qt
from tomwer.core import settings
from tomwer.core import utils
import functools
import copy

import logging

logger = logging.getLogger(__name__)


class AxisOW(widget.OWWidget, WidgetLongProcessing):
    """
    Widget used to defined the center of rotation axis to be used for a
    reconstruction.

    :param bool _connect_handler: True if we want to store the modifications
                      on the setting. Need for unit test since
                      keep alive qt widgets.
    """

    name = "center of rotation calculation"
    id = "orange.widgets.tomwer.axis"
    description = "use to compute the center of rotation"
    icon = "icons/axis.png"
    priority = 14
    category = "esrfWidgets"
    keywords = [
        "tomography",
        "axis",
        "tomwer",
        "reconstruction",
        "rotation",
        "position",
        "ftseries",
    ]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = True
    compress_signal = False

    settingsHandler = CallbackSettingsHandler()

    sigScanReady = qt.Signal(TomwerScanBase)
    """Signal emitted when a scan is ready"""
    if qt._qt.BINDING == "PyQt4":
        sigComputationStarted = qt.Signal()
        """need redefinition for pyqt4"""
        sigComputationEnded = qt.Signal()
        """need redefinition for pyqt4"""
    _rpSetting = Setting(dict())
    "AxisRP store as dict"

    class Inputs:
        data_in = Input(
            name=AxisProcess.inputs[0].name,
            type=AxisProcess.inputs[0].type,
            doc=AxisProcess.inputs[0].doc,
        )
        data_recompute_axis = Input(
            name=AxisProcess.inputs[1].name,
            type=AxisProcess.inputs[1].type,
            doc=AxisProcess.inputs[1].doc,
        )

    assert len(AxisProcess.outputs) == 1

    class Outputs:
        data_out = Output(
            name=AxisProcess.outputs[0].name,
            type=AxisProcess.outputs[0].type,
            doc=AxisProcess.outputs[0].doc,
        )

    def __init__(self, parent=None, axis_params=None):
        """

        :param parent: QWidget parent or None
        :param _connect_handler: used for CI, because if connected fails CI
        :param QAxisRP axis_params: reconstruction parameters
        """
        self._axis_params = axis_params or QAxisRP()
        if self._rpSetting != dict():
            try:
                self._axis_params.load_from_dict(self._rpSetting)
            except Exception as e:
                logger.error("fail to load reconstruction settings:", str(e))

        self.__lastAxisProcessParamsCache = None
        # used to memorize the last (reconstruction parameters, scan)
        self.__scan = None
        self.__skip_exec = False
        self._n_skip = 0
        self._patches = []
        """patches for processing"""

        WidgetLongProcessing.__init__(self)
        widget.OWWidget.__init__(self, parent)
        self._processingStack = AxisProcessStack(axis_params=self._axis_params)

        self._widget = AxisWindow(parent=self, axis_params=self._axis_params)

        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._widget)

        # expose API
        self.setMode = self._widget.setMode
        self.getRadioMode = self._widget.getRadioMode
        self.getEstimatedCor = self._widget.getEstimatedCor
        self.getAxis = self._widget.getAxis
        self.setValueLock = self._widget.setValueLock
        self._setModeLockFrmSettings = self._widget._setModeLockFrmSettings
        self._setValueLockFrmSettings = self._widget._setValueLockFrmSettings

        # load settings
        if self._rpSetting != dict():
            if "gui" in self._rpSetting:
                if "mode_is_lock" in self._rpSetting["gui"]:
                    self._setModeLockFrmSettings(self._rpSetting["gui"]["mode_is_lock"])
                if "value_is_lock" in self._rpSetting["gui"]:
                    if self._rpSetting["gui"]["value_is_lock"] is True:
                        self._setValueLockFrmSettings(
                            bool(self._rpSetting["gui"]["value_is_lock"])
                        )
        # connect Signal / Slot
        self._widget.sigComputationRequested.connect(self.__compute)
        self._widget.sigApply.connect(self.__validate)
        self._widget.sigAxisEditionLocked.connect(self.__lockReconsParams)
        self._processingStack.sigComputationStarted.connect(self._processingStart)
        self._processingStack.sigComputationEnded.connect(self._scanProcessed)

        self._axis_params.sigChanged.connect(self._updateSettingsVals)
        self._widget.sigAxisEditionLocked.connect(self._updateSettingsVals)
        self._widget.sigMethodChanged.connect(self._updateSettingsVals)
        self._widget.sigLockModeChanged.connect(self._updateSettingsVals)

        # connect sinogram calculation signal
        # self._widget._axisWidget._sinogramAxis.sigSinoLoadStarted.connect(
        #     self._processingStart
        # )
        # self._widget._axisWidget._sinogramAxis.sigSinoLoadEnded.connect(
        #     self._endProcessing
        # )

    def _processingStart(self, *args, **kwargs):
        self._widget._disableForProcessing()
        WidgetLongProcessing._startProcessing(self)

    def _scanProcessed(self, scan):
        assert isinstance(scan, TomwerScanBase)
        WidgetLongProcessing._endProcessing(self, scan)
        self._widget._enableForProcessing()
        if self.isValueLock() or self.isModeLocked():
            self.__scan = scan
            self.__validate()
        else:
            self.__scan = scan
            self.activateWindow()
            self.raise_()
            self.show()

    def __compute(self):
        if self.__scan:
            self.__lastAxisProcessParamsCache = (
                self._axis_params.to_dict(),
                str(self.__scan),
            )
            callback = functools.partial(self._updatePosition, self.__scan)
            self._processingStack.add(
                scan=self.__scan,
                configuration=self._axis_params.to_dict(),
                callback=callback,
            )

    def __validate(self):
        """Validate the current scan and move the scan to the next process.
        The Axis will process the next scan in the stack.
        """
        if self.__scan:
            self.accept()
            self.scan_ready(scan=self.__scan)
        self.hide()

    def __lockReconsParams(self, lock):
        self.lock_position_value(lock)

    def scan_ready(self, scan):
        assert isinstance(scan, TomwerScanBase)
        self.Outputs.data_out.send(scan)
        self.sigScanReady.emit(scan)

    def _informNoProjFound(self, scan):
        msg = qt.QMessageBox(self)
        msg.setIcon(qt.QMessageBox.Warning)
        text = (
            "Unable to find url to compute the axis of `%s`" % scan.path
            or "no path given"
        )
        text += ", please select them from the `axis input` tab"
        msg.setText(text)
        msg.exec_()

    def _updateSettingsVals(self):
        self._rpSetting = self._axis_params.to_dict()
        self._rpSetting["gui"] = {
            "mode_is_lock": self.isModeLocked(),
            "value_is_lock": self.isValueLock(),
        }

    def _skip_exec(self, b):
        """util function used for unit test. If activate, skip the call to
        self.exec() in process"""
        self.__skip_exec = b

    @property
    def recons_params(self):
        return self._axis_params

    def _instanciateReconsParams(self):
        return QAxisRP()

    def _lock_axis_controls(self, lock):
        """

        :param bool lock: lock the axis controls to avoid modification of the
                          requested options, method... of the axis calculation
                          when this value is under calculation.
        """
        self._widget.setLocked(lock)

    def isValueLock(self):
        """
        Check if the cor value has been lock. If so we simply copy the cor
        value and move to the next scan
        """
        return self._widget.isValueLock()

    def isModeLocked(self):
        """
        Check if the mode has been lock or not. If lock then call the
        algorithm and does not wait for any user feedback
        """
        return self._widget.isModeLock()

    @Inputs.data_in
    def new_data_in(self, scan):
        if scan is None:
            return
        scan_ = copy.copy(scan)
        if not (
            settings.isOnLbsram(scan)
            and utils.isLowOnMemory(settings.get_lbsram_path())
        ):
            self._widget.setScan(scan=scan_)
        elif scan_.axis_params is None:
            scan_.axis_params = QAxisRP()
        self.process(scan=scan_)

    def process(self, scan):
        if scan is None:
            return
        self.__scan = scan
        self._axis_params.frame_width = scan.dim_1
        if (
            settings.isOnLbsram(scan)
            and utils.isLowOnMemory(settings.get_lbsram_path()) is True
        ):
            self._updatePosition(scan=scan)
            self.scan_ready(scan=scan)
        elif self.__skip_exec:
            self._n_skip += 1
            if self.isValueLock():
                scan._axis_params.set_value_ref_tomwer(self._axis_params.value)
                cor = scan._axis_params.value_ref_tomwer
                if isinstance(scan, HDF5TomoScan):
                    entry = scan.entry
                else:
                    entry = "entry"
                with scan.acquire_process_file_lock():
                    AxisProcess._register_process(
                        process_file=scan.process_file,
                        entry=entry,
                        process=AxisProcess,
                        results={"center_of_rotation": cor if cor is not None else "-"},
                        configuration=self._axis_params.to_dict(),
                        process_index=scan.pop_process_index(),
                        overwrite=True,
                    )
            else:
                processing_class = AxisProcess(axis_params=self._axis_params)
                for patch in self._patches:
                    mode, function = patch
                    processing_class.RADIO_CALCULATIONS_METHODS[mode] = function
                processing_class.process(scan=self.__scan)
            self._updatePosition(scan=self.__scan)
            if self.isModeLocked() or self.isValueLock():
                self.scan_ready(scan=scan)

        elif self.isModeLocked() or self.isValueLock():
            self.__lastAxisProcessParamsCache = (
                self._axis_params.to_dict(),
                str(self.__scan),
            )
            callback = functools.partial(self._updatePosition, scan)
            self._processingStack.add(
                scan=scan, configuration=self._axis_params.to_dict(), callback=callback
            )
        else:
            callback = functools.partial(self._updatePosition, self.__scan)
            self._processingStack.add(
                scan=self.__scan,
                callback=callback,
                configuration=self._axis_params.to_dict(),
            )
            self.activateWindow()
            self.raise_()
            self.show()

    def _updatePosition(self, scan):
        if scan.axis_params is not None:
            self._widget.setPosition(frm=None, value=scan.axis_params.value_ref_tomwer)

    @Inputs.data_recompute_axis
    def reprocess(self, scan):
        """Recompute the axis for scan"""
        # for now The behavior for reprocessing is the sama as for processing
        self.process(scan=scan.instance)

    def close(self):
        self._processingStack.stop()
        self._processingStack.wait_computation_finished()
        super(AxisOW, self).close()

    def patch_calc_method(self, mode, function):
        self._patches.append((mode, function))

    def keyPressEvent(self, event):
        """The event has to be filtered since we have some children
         that can be edited using the 'enter' key as defining the cor manually
        (see #481)). As we are in a dialog this automatically trigger
        'accepted'. See https://forum.qt.io/topic/5080/preventing-enter-key-from-triggering-ok-in-qbuttonbox-in-particular-qlineedit-qbuttonbox/5
        """
        if event.key() != qt.Qt.Key_Enter:
            super().keyPressEvent(event)
