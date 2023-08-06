# coding: utf-8
###########################################################################
# Copyright (C) 2016-2019 European Synchrotron Radiation Facility
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
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "03/05/2019"


from tomwer.core.process.reconstruction.axis import AxisProcess
from tomwer.core.process.reconstruction.axis.axis import NoAxisUrl
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.synctools.axis import QAxisRP
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils import isLowOnMemory
from ..processingstack import FIFO, ProcessingThread
from silx.gui import qt
import logging
import functools

_logger = logging.getLogger(__name__)


class AxisProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisProcess` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, axis_params):
        qt.QObject.__init__(self)
        FIFO.__init__(self)
        assert axis_params is not None
        self._axis_params = axis_params

    def _process(self, scan, configuration, callback=None):
        assert isinstance(scan, TomwerScanBase)
        if scan.axis_params is None:
            scan.axis_params = QAxisRP()
        self._scan_currently_computed = scan
        self._axis_params.frame_width = scan.dim_1
        mode = self._axis_params.mode
        if isOnLbsram(scan) and isLowOnMemory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip axis calculation", scan.path
            _logger.processSkipped(mess)
            scan.axis_params.set_value_ref_tomwer(None)
            if callback is not None:
                callback()
            self.scan_ready(scan=scan)
        elif not self._axis_params.use_sinogram and mode in (
            AxisMode.manual,
            AxisMode.read,
        ):
            scan._axis_params.set_value_ref_tomwer(self._axis_params.value_ref_tomwer)
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
            # If mode is read or manual the position_value is not computed and
            # we will keep the actual one (should have been defined previously)
            self._end_computation(scan=scan, callback=callback)

        elif (
            not self._axis_params.use_sinogram
            and not mode in AxisProcess.RADIO_CALCULATIONS_METHODS
        ):
            _logger.warning("no method defined to compute {}".format(mode))
            if callback is not None:
                callback()
            self._process_next()
        else:
            scan.axis_params.set_value_ref_tomwer("...")
            self._axis_params.set_value_ref_tomwer("...")
            assert self._axis_params.value_ref_tomwer == "..."
            self._scan_currently_computed = scan
            self._computationThread.init(scan=scan, axis_params=self._axis_params)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_computation(self, scan, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        assert isinstance(scan, TomwerScanBase)
        assert self._axis_params is not None
        # copy result computed on scan on the AxisProcess reconsparams
        self._axis_params.set_value_ref_tomwer(
            scan.axis_params.value_ref_tomwer
        )  # noqa
        self._axis_params.frame_width = scan.dim_1
        FIFO._end_computation(self, scan=scan, callback=callback)

    def _end_threaded_computation(self, callback=None):
        assert self._scan_currently_computed is not None
        self._axis_params.set_value_ref_tomwer(
            self._computationThread.center_of_rotation
        )
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self) -> qt.QThread:
        return _ProcessingThread()


class _ProcessingThread(ProcessingThread):
    """
    Thread use to execute the processing of the axis position
    """

    def __init__(self):
        ProcessingThread.__init__(self)
        self._scan = None
        self._axis_params = None
        """function pointer to know which function to call for the axis
        calculation"""
        self.__patch = {}
        """Used to patch some calculation method (for test purpose)"""

    def init(self, scan, axis_params):
        self._scan = scan
        self._axis_params = axis_params

    def run(self):
        self.sigComputationStarted.emit()
        axis = AxisProcess(axis_params=self._axis_params)
        axis = self.apply_patch(axis=axis)
        try:
            axis.process(self._scan)
        except NoAxisUrl as e:
            self.center_of_rotation = None
            _logger.error(str(e))
        except Exception as e:
            _logger.error(str(e))
            self.center_of_rotation = None
        else:
            self.center_of_rotation = self._scan.axis_params.value_ref_tomwer

    def patch_calc_method(self, mode, function):
        self.__patch[mode] = function

    def apply_patch(self, axis):
        for mode, patch_fct in self.__patch.items():
            if mode in AxisMode:
                axis.RADIO_CALCULATIONS_METHODS[mode] = patch_fct
        return axis
