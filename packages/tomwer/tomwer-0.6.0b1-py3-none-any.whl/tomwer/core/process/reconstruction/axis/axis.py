# coding: utf-8
###########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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

"""contain the AxisProcess
"""

__authors__ = ["C.Nemoz", "H.Payno"]
__license__ = "MIT"
__date__ = "19/03/2019"

from .params import AxisRP
from .mode import AxisMode
from .projectiontype import ProjectionType
from .anglemode import CorAngleMode
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from silx.image import tomography
import logging
from tomwer.core.utils import logconfig
import numpy
from typing import Union
from tomwer.utils import docstring
from tomwer.core.utils import image
import tomwer.version
from tomwer.core.scan.scanbase import _TomwerBaseDock
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from nabu.preproc.alignment import CenterOfRotation
from nabu.preproc.alignment import CenterOfRotationAdaptiveSearch
from nabu.preproc.alignment import CenterOfRotationGrowingWindow
from nabu.preproc.alignment import CenterOfRotationSlidingWindow
from silx.io.url import DataUrl
from tomoscan.io import HDF5File

_logger = logging.getLogger(__name__)

# vertically, work on a window having only a percentage of the frame.
pc_height = 10.0 / 100.0
# horizontally. Global method supposes the COR is more or less in center
# % of the detector:

pc_width = 50.0 / 100.0


def compute_cor_nabu_growing_window(
    radio_1: numpy.ndarray,
    radio_2: numpy.ndarray,
    side: str,
    padding_mode,
    horz_fft_width=False,
):
    """
    Call nabu.preproc.alignement.CenterOfRotationGrowingWindow.find_shift

    :param radio_1:
    :param radio_2:
    :param padding_mode: padding mode
    :param str side: side of the cor
    :param horz_fft_width:
    :param half_acq_cor_guess: The approximate position of the rotation axis
                               from the image center. Optional. When given a
                               special algorithm is used which can work also
                               in half-tomo conditions.

    :return:
    """
    nabu_class = CenterOfRotationGrowingWindow(horz_fft_width=horz_fft_width)
    return nabu_class.find_shift(
        img_1=radio_1,
        img_2=numpy.fliplr(radio_2),
        side=side,
        roi_yxhw=None,
        padding_mode=padding_mode,
        median_filt_shape=None,
    )


def compute_scan_cor_nabu_growing_window(scan):
    """
    Call to nabu.preproc.alignment.CenterOfRotation from the scan axis_params
    value.

    :param `.TomoBase` scan: scan to process
    :return: Union[float, None]

    """
    assert scan.axis_params is not None
    radio_1, radio_2 = AxisProcess.get_inputs(scan=scan)
    if radio_1 is None or radio_2 is None:
        raise NoAxisUrl("Unable to find projections for nabu axis calculation")

    _logger.info(
        "compute scan axis from nabu CenterOfRotationGrowingWindow with padding "
        "mode {} and side {}".format(
            scan.axis_params.padding_mode, scan.axis_params.side
        )
    )

    return compute_cor_nabu_growing_window(
        radio_1=radio_1.copy(),
        radio_2=radio_2.copy(),
        side=scan.axis_params.side,
        padding_mode=scan.axis_params.padding_mode,
    )


def compute_cor_nabu_sliding_window(
    radio_1: numpy.ndarray,
    radio_2: numpy.ndarray,
    side: str,
    padding_mode,
    horz_fft_width=False,
):
    """
    Call nabu.preproc.alignement.CenterOfRotationSlidingWindow.find_shift

    :param radio_1:
    :param radio_2:
    :param padding_mode:
    :param str side: side of the cor
    :param horz_fft_width:
    :param half_acq_cor_guess: The approximate position of the rotation axis
                               from the image center. Optional. When given a
                               special algorithm is used which can work also
                               in half-tomo conditions.

    :return:
    """
    nabu_class = CenterOfRotationSlidingWindow(horz_fft_width=horz_fft_width)
    return nabu_class.find_shift(
        img_1=radio_1,
        img_2=numpy.fliplr(radio_2),
        side=side,
        roi_yxhw=None,
        padding_mode=padding_mode,
        median_filt_shape=None,
    )


def compute_scan_cor_nabu_sliding_window(scan):
    """
    Call to nabu.preproc.alignment.CenterOfRotation from the scan axis_params
    value.

    :param `.TomoBase` scan: scan to process
    :return: Union[float, None]

    """
    assert scan.axis_params is not None
    radio_1, radio_2 = AxisProcess.get_inputs(scan=scan)
    if radio_1 is None or radio_2 is None:
        raise NoAxisUrl("Unable to find projections for nabu axis calculation")

    _logger.info(
        "compute scan axis from nabu CenterOfRotationSlidingWindow with padding "
        "mode {} and side {}".format(
            scan.axis_params.padding_mode, scan.axis_params.side
        )
    )

    return compute_cor_nabu_sliding_window(
        radio_1=radio_1.copy(),
        radio_2=radio_2.copy(),
        side=scan.axis_params.side,
        padding_mode=scan.axis_params.padding_mode,
    )


def compute_cor_nabu_centered(
    radio_1: numpy.ndarray,
    radio_2: numpy.ndarray,
    padding_mode,
    horz_fft_width=False,
):
    """
    Call nabu.preproc.alignement.CenterOfRotation.find_shift

    :param radio_1:
    :param radio_2:
    :param padding_mode:
    :param horz_fft_width:
    :param half_acq_cor_guess: The approximate position of the rotation axis
                               from the image center. Optional. When given a
                               special algorithm is used which can work also
                               in half-tomo conditions.

    :return:
    """
    nabu_class = CenterOfRotation(horz_fft_width=horz_fft_width)
    return nabu_class.find_shift(
        img_1=radio_1,
        img_2=numpy.fliplr(radio_2),
        roi_yxhw=None,
        padding_mode=padding_mode,
        median_filt_shape=None,
    )


def compute_scan_cor_nabu_centered(scan):
    """
    Call to nabu.preproc.alignment.CenterOfRotation from the scan axis_params
    value.

    :param `.TomoBase` scan: scan to process
    :return: Union[float, None]

    """
    assert scan.axis_params is not None
    radio_1, radio_2 = AxisProcess.get_inputs(scan=scan)
    if radio_1 is None or radio_2 is None:
        raise NoAxisUrl("Unable to find projections for nabu axis calculation")

    _logger.info(
        "compute scan axis from nabu CenterOfRotation with padding "
        "mode %s" % scan.axis_params.padding_mode
    )

    return compute_cor_nabu_centered(
        radio_1=radio_1.copy(),
        radio_2=radio_2.copy(),
        padding_mode=scan.axis_params.padding_mode,
    )


def compute_cor_nabu_global(
    radio_1: numpy.ndarray,
    radio_2: numpy.ndarray,
    padding_mode,
    horz_fft_width=False,
):
    """
    Call nabu.preproc.alignement.CenterOfRotation.find_shift

    :param radio_1:
    :param radio_2:
    :param padding_mode:
    :param horz_fft_width:
    :return:
    """
    nabu_class = CenterOfRotationAdaptiveSearch(horz_fft_width=horz_fft_width)
    return nabu_class.find_shift(
        img_1=radio_1,
        img_2=numpy.fliplr(radio_2),
        roi_yxhw=None,
        padding_mode=padding_mode,
        median_filt_shape=None,
    )


def compute_scan_cor_nabu_global(scan):
    """
    Call to nabu.preproc.alignment.CenterOfRotation from the scan axis_params
    value.

    :param `.TomoBase` scan: scan to process
    :return: Union[float, None]

    """
    assert scan.axis_params is not None
    radio_1, radio_2 = AxisProcess.get_inputs(scan=scan)
    if radio_1 is None or radio_2 is None:
        raise NoAxisUrl("Unable to find projections for nabu axis calculation")

    _logger.info(
        "compute scan axis from nabu CenterOfRotation with padding "
        "mode %s" % scan.axis_params.padding_mode
    )

    return compute_cor_nabu_global(
        radio_1=radio_1.copy(),
        radio_2=radio_2.copy(),
        padding_mode=scan.axis_params.padding_mode,
    )


def get_stdmax_column(x: numpy.ndarray) -> float:
    """

    :param x:
    :return: column index of the maximal standard deviation
    """
    kernel_size = 5
    l = len(x)
    r = range(l - kernel_size)
    y = numpy.empty(l - kernel_size)
    for i in r:
        s = numpy.std(x[i : i + kernel_size])
        y[i] = s

    return y.argmax()


def compute_frm_sinogram(scan, line, is_emission, subsampling):
    """
    Compute the center of rotation of the sinogram for the given
    :param scan:
    :param line:
    :param is_emission:
    :return: axis of rotation in [-image_width/2, image_width/2]
    """
    assert type(line) is int
    sinogram = scan.get_sinogram(line=line, subsampling=subsampling)
    if is_emission is True:
        sinogram = sinogram.max() - sinogram
    sinogram[sinogram == numpy.nan] = None
    sinogram[sinogram == numpy.inf] = None
    # make sure minimal value is 1
    sinogram = sinogram + abs(sinogram.min()) + 1
    sinogram = sinogram + 1

    _logger.info(
        "Compute axis from sinogram for %s. With line:%s,"
        "subsamppling: %s, is emission: %s"
        "" % (scan.path, line, subsampling, is_emission)
    )

    res = tomography.calc_center_centroid(sino=sinogram.T)
    # move it to tomwer ref [-image_width/2, image_width/2]
    return res - sinogram.shape[0] // 2


class NoAxisUrl(Exception):
    pass


class AxisProcess(SingleProcess):
    """
    Process used to compute the center of rotation of a scan

    :param axis_params: parameters to configure the axis process
    :type: AxisRP
    """

    inputs = [
        _input_desc(
            name="data", type=TomwerScanBase, handler="process", doc="scan path"
        ),
        _input_desc(
            name="change recons params",
            type=_TomwerBaseDock,
            handler="reprocess",
            doc="recompute axis",
        ),
    ]
    outputs = [_output_desc(name="data", type=TomwerScanBase, doc="scan path")]

    RADIO_CALCULATIONS_METHODS = {
        AxisMode.centered: compute_scan_cor_nabu_centered,
        AxisMode.global_: compute_scan_cor_nabu_global,
        AxisMode.sliding_window: compute_scan_cor_nabu_sliding_window,
        AxisMode.growing_window: compute_scan_cor_nabu_growing_window,
        # AxisMode.near: compute_scan_cor_near,
    }

    def __init__(self, axis_params=None):
        SingleProcess.__init__(self)
        self._mode_calculation_fct = {}
        """dict with function pointer to call for making the mode calculation.
        Function should have only one 'scan' parameter as input"""

        assert axis_params is None or isinstance(axis_params, AxisRP)
        self._axis_params = axis_params or AxisRP()
        """Axis reconstruction parameters to apply"""
        self._locked = False
        """Boolean used to lock reconstruction parameters edition"""
        self._recons_params_before_lock = None
        """Recons parameters register before locking the position"""

    @docstring(SingleProcess)
    def set_properties(self, properties):
        self.set_recons_params(recons_params=AxisRP.from_dict(properties["_rpSetting"]))

    def set_recons_params(self, recons_params):
        assert isinstance(recons_params, AxisRP)
        self._axis_params = recons_params

    def lock_position_value(self, lock=True):
        """
        lock the position currently computed or defined by the user.
        In this case we will lock the axis as defined 'fixed' with the current
        value

        :param bool lock: if true lock the currently existing position value
        """
        self._locked = lock
        if lock:
            self._recons_params_before_lock = self._axis_params.to_dict()
            if self._axis_params not in (AxisMode.manual, AxisMode.read):
                self._axis_params.mode = AxisMode.manual
        else:
            if self._recons_params_before_lock:
                self._axis_params.load_from_dict(
                    self._recons_params_before_lock
                )  # noqa

    def process(self, scan):
        """
        Compute the position value then get ready to the next. And call

        .. note:: this simply call `compute`.
                  But this is needed for the AxisProcessThreaded class
        """
        if scan is None:
            return

        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError("input type {} is not managed".format(scan))

        _logger.info("start axis calculation for %s" % scan.path)
        self._axis_params.frame_width = scan.dim_1
        cor = error = None
        try:
            scan_res = self.compute(scan=scan)
        except Exception as e:
            scan_res = None
            error = e
        else:
            if isinstance(scan_res, TomwerScanBase):
                cor = scan_res.axis_params.value_ref_tomwer
            elif scan_res is None:
                if scan.axis_params.value_ref_tomwer is not None:
                    cor = scan.axis_params.value_ref_tomwer
            elif isinstance(scan_res, float):
                cor = scan_res
            else:
                assert isinstance(scan_res, dict)
                b_dict = scan_res
                if TomwerScanBase._DICT_AXIS_KEYS in scan_res:
                    b_dict = scan_res["axis_recons_params"]
                cor = b_dict["POSITION_VALUE"]
        finally:
            if cor != "...":
                self._process_end(scan, cor=cor, error=error)
        return scan_res

    def reprocess(self, scan):
        """
        Reprocess the scan. For now simply call process

        :param scan:
        """
        return self.process(scan=scan)

    def _process_end(self, scan, cor, error=None):
        assert isinstance(scan, TomwerScanBase)
        if scan.process_file is not None:
            entry = "entry"
            if isinstance(scan, HDF5TomoScan):
                entry = scan.entry
            with scan.acquire_process_file_lock():
                self.register_process(
                    process_file=scan.process_file,
                    entry=entry,
                    results={"center_of_rotation": cor if cor is not None else "-"},
                    configuration=self._axis_params.to_dict(),
                    process_index=scan.pop_process_index(),
                    overwrite=True,
                )

        try:
            extra = {
                logconfig.DOC_TITLE: self._scheme_title,
                logconfig.SCAN_ID: scan.path,
            }
            if error is not None:
                info = " ".join(
                    (
                        "fail to compute axis position for scan",
                        str(scan.path),
                        "reason is ",
                        str(error),
                    )
                )
                _logger.processFailed(info, extra=extra)
            elif scan.axis_params.value_ref_tomwer is None:
                info = " ".join(
                    ("fail to compute axis position for scan", str(scan.path))
                )
                _logger.processFailed(info, extra=extra)
            else:
                info = "axis calculation defined for {}: {} (using {})" "".format(
                    str(scan.path),
                    str(scan.axis_params.value_ref_tomwer),
                    scan.axis_params.mode.value,
                )
                _logger.processSucceed(info, extra=extra)
        except Exception as e:
            _logger.error(e)

    @staticmethod
    def get_inputs_urls(scan):
        """Make sure we have valid projections to be used for axis calculation

        :param TomwerScanBase scan: scan to check
        :raise: NoAxisUrl if fails to found
        :return: the two projections to be used for axis calculation
        :rtype: tuple of AxisResource
        """
        if (
            scan.axis_params
            and scan.axis_params.axis_url_1
            and scan.axis_params.axis_url_1.url
        ):
            return scan.axis_params.axis_url_1, scan.axis_params.axis_url_2
        else:
            _radio_1, _radio_2 = scan.getRadiosForAxisCalc(
                mode=CorAngleMode.manual_selection
            )
        return _radio_1, _radio_2

    @staticmethod
    def get_inputs(scan):
        assert isinstance(scan, TomwerScanBase)
        radio_1, radio_2 = AxisProcess.get_inputs_urls(scan=scan)
        if radio_1 and radio_2:
            mess = " ".join(
                ("input radios are", radio_1.url.path(), "and", radio_2.url.path())
            )
            _logger.info(mess)
            log_ = scan.axis_params.projection_type is ProjectionType.transmission

            # if necessary normalize data
            if radio_1.normalized_data is None:
                radio_1.normalize_data(scan, log_=log_)
            if radio_2.normalized_data is None:
                radio_2.normalize_data(scan, log_=log_)

            if scan.axis_params.paganin_preproc:
                data_1 = radio_1.normalized_data_paganin
                data_2 = radio_2.normalized_data_paganin
            else:
                data_1 = radio_1.normalized_data
                data_2 = radio_2.normalized_data

            if scan.axis_params.scale_img2_to_img1:
                data_2 = image.scale_img2_to_img1(img_1=data_1, img_2=data_2)
            return data_1, data_2
        else:
            _logger.info("fail to find any inputs")
            return None, None

    def compute(self, scan, wait=True):
        """
        Compute the position value for the scan

        :param TomwerScanBase scan:
        :param bool wait: used for threaded process. True if we want to end the
                          computation before releasing hand.
        :return: scan as a TomoBase
        """
        assert scan is not None
        if isinstance(scan, dict):
            _logger.warning("convert scan from a dict")
            _scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            _scan = scan
        assert isinstance(_scan, TomwerScanBase)
        # if the scan has no tomo reconstruction parameters yet create them
        if _scan.axis_params is None:
            _scan.axis_params = AxisRP()

        # copy axis recons parameters. We skip the axis_url which are specific
        # to the scan
        _scan.axis_params.copy(self._axis_params, copy_axis_url=False)
        assert scan.axis_params is not None
        return self._process_computation(scan=_scan)

    def scan_ready(self, scan):
        _logger.info(scan, "processed")

    def _process_computation(self, scan):
        """

        :param TomwerScanBase scan: scan for which we want to compute the axis
                              position.
        :return: scan as a TomoBase or a dict if _return_dict activated
        """
        _logger.info("compute center of rotation for %s" % scan.path)
        try:
            position = self.compute_axis_position(scan)
        except NotImplementedError:
            scan.axis_params.set_value_ref_tomwer(None)
            raise NotImplementedError("Not implemented")
        except ValueError as e:
            scan_name = scan.path or "undef scan"
            scan.axis_params.set_value_ref_tomwer(None)
            raise Exception(
                "Fail to compute axis position for", scan_name, "reason is", e
            )
        else:
            scan.axis_params.set_value_ref_tomwer(position)
            self._axis_params.frame_width = scan.dim_1
            self._axis_params.set_value_ref_tomwer(position)
            scan_name = scan.path or "undef scan"
            if scan.axis_params.use_sinogram:
                method = "sinogram"
            else:
                method = scan.axis_params.mode.value
            mess = (
                "Compute axis position ({value}) with {method} for {scan_name}".format(
                    value=str(scan.axis_params.value_ref_tomwer),
                    method=method,
                    scan_name=scan_name,
                )
            )
            _logger.info(mess)
        if self._return_dict:
            return scan.to_dict()
        else:
            return scan

    def setMode(self, mode, value):
        if mode is AxisMode.manual:
            self._axis_params.cor_position = value
        else:
            raise NotImplementedError("mode not implemented yet")

    def define_calculation_mode(self, mode, fct_pointer):
        """Register the function to call of the given mode

        :param AxisMode mode: the mode to register
        :param fct_pointer: pointer to the function to call
        """
        self._mode_calculation_fct[id] = fct_pointer

    def compute_axis_position(self, scan):
        """

        :param scan: scan for which we compute the center of rotation
        :type: TomoScan
        :return: position of the rotation axis. Use the `.AxisMode` defined
                 by the `.ReconsParams` of the `.AxisProcess`
        :rtype: float or None (if fail to compute the axis position)
        """
        mode = self._axis_params.mode
        use_sinogram = self._axis_params.use_sinogram
        if use_sinogram:
            _logger.info("use sinogram")
            is_emission = self._axis_params.projection_type == ProjectionType.absorption
            subsampling = self._axis_params.sinogram_subsampling
            assert type(self._axis_params.sinogram_line) is int
            res = compute_frm_sinogram(
                scan=scan,
                line=self._axis_params.sinogram_line,
                is_emission=is_emission,
                subsampling=subsampling,
            )
        elif mode in (AxisMode.manual, AxisMode.read):
            # If mode is read or manual the position_value is not computed and
            # we will keep the actual one (should have been defined previously)
            res = self._axis_params.value_ref_tomwer
        elif mode in self.RADIO_CALCULATIONS_METHODS:
            _logger.info("use radios, mode is %s" % mode.value)
            res = self.RADIO_CALCULATIONS_METHODS[mode](scan)
        else:
            raise NotImplementedError("Method for", mode, "is not defined")
        return res

    @docstring(SingleProcess.program_name)
    @staticmethod
    def program_name():
        return "tomwer_axis"

    @docstring(SingleProcess.program_version)
    @staticmethod
    def program_version():
        return tomwer.version.version

    @docstring(SingleProcess.definition)
    @staticmethod
    def definition():
        return "Compute center of rotation"

    @staticmethod
    def get_cor_frm_process_file(
        process_file, entry, as_url=False
    ) -> Union[None, float]:
        """
        Read cor position from a tomwer_process file

        :param process_file:
        :param entry:
        :return:
        """
        if entry is None:
            with HDF5File(process_file, "r", swmr=True) as h5f:
                entries = AxisProcess._get_process_nodes(
                    root_node=h5f, process=AxisProcess
                )
                if len(entries) == 0:
                    _logger.info("unable to find a Axis process in %s" % process_file)
                    return None
                elif len(entries) > 1:
                    raise ValueError("several entry found, entry should be " "specify")
                else:
                    entry = list(entries.keys())[0]
                    _logger.info("take %s as default entry" % entry)

        with HDF5File(process_file, "r", swmr=True) as h5f:
            axis_nodes = AxisProcess._get_process_nodes(
                root_node=h5f[entry], process=AxisProcess
            )
            index_to_path = {}
            for key, index in axis_nodes.items():
                index_to_path[index] = key

            if len(axis_nodes) == 0:
                return None
            # take the last processed dark ref
            last_process_index = sorted(list(axis_nodes.values()))[-1]
            last_process_dark = index_to_path[last_process_index]
            if (len(index_to_path)) > 1:
                _logger.debug(
                    "several processing found for dark-ref,"
                    "take the last one: %s" % last_process_dark
                )

            res = None
            if "results" in h5f[last_process_dark].keys():
                results_node = h5f[last_process_dark]["results"]
                if "center_of_rotation" in results_node.keys():
                    if as_url:
                        res = DataUrl(
                            file_path=process_file,
                            data_path="/".join((results_node, "center_of_rotation")),
                            scheme="h5py",
                        )
                    else:
                        res = results_node["center_of_rotation"][()]
            return res
