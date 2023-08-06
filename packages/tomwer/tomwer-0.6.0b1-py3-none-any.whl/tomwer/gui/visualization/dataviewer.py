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
__date__ = "21/07/2020"

import silx
from silx.gui import qt
from silx.utils.enum import Enum as _Enum

try:
    from silx.gui.utils.signal import SignalProxy
except ImportError:
    from tomwer.third_party.silxsignal import SignalProxy
import weakref
import logging

if silx._version.MAJOR == 0 and silx._version.MINOR < 14:
    from tomwer.third_party.ImageStack import UrlLoader, ImageStack as _ImageStack
else:
    from silx.gui.plot.ImageStack import UrlLoader, ImageStack as _ImageStack
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.ftseriesutils import get_vol_file_shape
from silx.io.url import DataUrl
from silx.io.utils import get_data
from tomwer.core.utils.char import BETA_CHAR, DELTA_CHAR

try:
    from PIL import Image
except ImportError:
    has_PIL = False
else:
    has_PIL = True

import numpy
import numpy.lib.npyio
import time
import os
from tomoscan.io import HDF5File

_logger = logging.getLogger(__name__)


class DataViewer(qt.QMainWindow):
    """
    Widget used to browse through data and reconstructed slices
    """

    sigConfigChanged = qt.Signal()
    """Signal emitted when the settings (display mode, options...) changed. """

    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._scan = None

        # viewer
        self._viewer = ImageStack(parent=self)
        # set an UrlLoader managing .npy and .vol
        self._viewer.setUrlLoaderClass(_TomwerUrlLoader)
        self._viewer.getPlotWidget().setKeepDataAspectRatio(True)
        self.setCentralWidget(self._viewer)

        # signal / slot
        # add a signal proxy on the QSlider
        self._viewer._slider.sigCurrentUrlIndexChanged.disconnect(
            self._viewer.setCurrentUrlIndex
        )
        self._proxySig = SignalProxy(
            self._viewer._slider.sigCurrentUrlIndexChanged,
            delay=0.3,
            slot=self._urlIndexDelayed,
        )

        # display control
        self._controls = DisplayControl(parent=self)
        self._controlsDW = qt.QDockWidget(self)
        self._controlsDW.setWidget(self._controls)
        self._controlsDW.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.TopDockWidgetArea, self._controlsDW)

        # connect signal / slot
        self._controls.sigDisplayModeChanged.connect(self._updateDisplay)
        self._controls.sigDisplayModeChanged.connect(self._reportSettingsUpdate)

    def getCurrentUrl(self):
        return self._viewer.getCurrentUrl()

    def cleanBeforeQuit(self):
        self._viewer._plot.updateThread.stop()

    def close(self):
        self._viewer.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._viewer.close()
        self._viewer = None
        qt.QMainWindow.close(self)

    def _urlIndexDelayed(self, *args, **kwargs):
        self._viewer.setCurrentUrlIndex(args[0][0])

    def getScan(self):
        if self._scan:
            return self._scan()

    def setScan(self, scan):
        if scan is not None:
            self._scan = weakref.ref(scan)
        else:
            self._scan = None
        # update scan name
        self._controls.setScanName(str(scan))
        self._updateDisplay()

    def getDisplayMode(self):
        return self._controls.getDisplayMode()

    def setDisplayMode(self, mode):
        self._controls.setDisplayMode(mode)

    def getRadioOption(self):
        return self._controls.getRadioOption()

    def setRadioOption(self, opt):
        self._controls.setRadioOption(opt)

    def getSliceOption(self):
        return self._controls.getSliceOption()

    def setSliceOption(self, opt):
        self._controls.setSliceOption(opt)

    def _updateDisplay(self):
        """Update display of the viewer"""
        self._viewer.setSliceReconsParamsVisible(
            self.getDisplayMode() is _DisplayMode.SLICES
        )
        if self._scan is None or self._scan() is None:
            self._viewer.reset()
        else:
            assert isinstance(self._scan(), TomwerScanBase)
            if self.getDisplayMode() is _DisplayMode.RADIOS:
                # update the normalization function from the viewer if needed
                if self.getRadioOption() is _RadioMode.NORMALIZED:
                    url_to_index = {
                        v.path(): k for k, v in self._scan().projections.items()
                    }
                    self._viewer.setNormalizationFct(
                        self._scan().flat_field_correction, url_indexes=url_to_index
                    )
                else:
                    self._viewer.setNormalizationFct(None)

                values = self._scan().projections
                if len(values) > 0:
                    values = [
                        value
                        for key, value in sorted(
                            values.items(), key=lambda item: item[0]
                        )
                    ]
                    self._viewer.setUrls(values)
                else:
                    self._viewer.reset()
            elif self.getDisplayMode() is _DisplayMode.SLICES:
                self._viewer.setNormalizationFct(None)
                if self.getSliceOption() is _SliceMode.LATEST:
                    slices = self._scan().latest_reconstructions
                else:
                    slices = self._scan().get_reconstructions_urls()
                if len(slices) > 0:
                    self._viewer.setUrls(slices)
                else:
                    self._viewer.reset()
            else:
                raise ValueError("DisplayMode should be RADIOS or SLICES")

    def _reportSettingsUpdate(self):
        self.sigConfigChanged.emit()

    def clear(self):
        self._viewer.reset()


class _DisplayMode(_Enum):
    RADIOS = "radios"
    SLICES = "slices"


class _RadioMode(_Enum):
    NORMALIZED = "normalized"
    RAW = "raw"


class _SliceMode(_Enum):
    LATEST = "latest"
    ALL = "all"


class DisplayControl(qt.QWidget):
    """
    Widget sued to define what we want to display from the viewer
    """

    sigDisplayModeChanged = qt.Signal()
    """Signal emitted when the configuration of the display change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._lastConfig = None, None
        self.setLayout(qt.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # scan information
        scanLab = qt.QLabel("scan:", self)
        scanLab.setFixedWidth(40)
        scanLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(scanLab, 0, 0, 1, 1)
        self._scanQLE = qt.QLineEdit("", self)
        self._scanQLE.setReadOnly(True)
        self.layout().addWidget(self._scanQLE, 0, 1, 1, 3)

        # display information
        displayLab = qt.QLabel("display:", self)
        displayLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(displayLab, 1, 0, 1, 1)
        self._displayMode = qt.QComboBox(self)
        for mode in _DisplayMode:
            self._displayMode.addItem(mode.value)
        self.layout().addWidget(self._displayMode, 1, 1, 1, 1)

        # option information
        modeLab = qt.QLabel("mode:", self)
        modeLab.setFixedWidth(60)
        modeLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(modeLab, 1, 2, 1, 1)
        self._widget_options = qt.QWidget(self)
        self._widget_options.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._widget_options, 1, 3, 1, 1)

        self._radioMode = qt.QComboBox(self)
        for mode in _RadioMode:
            self._radioMode.addItem(mode.value)
        self._widget_options.layout().addWidget(self._radioMode)

        self._sliceMode = qt.QComboBox(self)
        for mode in _SliceMode:
            self._sliceMode.addItem(mode.value)
        self._widget_options.layout().addWidget(self._sliceMode)

        # set up
        # by default propose slices to avoid useless processing on radios
        idx = self._displayMode.findText(_DisplayMode.SLICES.value)
        self._displayMode.setCurrentIndex(idx)
        self._updateOptions()

        # connect signal and slot
        self._displayMode.currentTextChanged.connect(self._updateOptions)
        self._radioMode.currentTextChanged.connect(self._updateOptions)
        self._sliceMode.currentTextChanged.connect(self._updateOptions)

    def getDisplayMode(self) -> _DisplayMode:
        """

        :return: selected mode: display slices or radios
        """
        return _DisplayMode.from_value(self._displayMode.currentText())

    def setDisplayMode(self, mode):
        mode = _DisplayMode.from_value(mode)
        idx = self._displayMode.findText(mode.value)
        self._displayMode.setCurrentIndex(idx)

    def getRadioOption(self) -> _RadioMode:
        return _RadioMode.from_value(self._radioMode.currentText())

    def setRadioOption(self, opt):
        opt = _RadioMode.from_value(opt)
        idx = self._radioMode.findText(opt.value)
        self._radioMode.setCurrentIndex(idx)

    def getSliceOption(self) -> _SliceMode:
        return _SliceMode.from_value(self._sliceMode.currentText())

    def setSliceOption(self, opt):
        opt = _SliceMode.from_value(opt)
        idx = self._sliceMode.findText(opt.value)
        self._sliceMode.setCurrentIndex(idx)

    def _updateOptions(self, *args, **kwargs):
        mode = self.getDisplayMode()
        self._radioMode.setVisible(mode == _DisplayMode.RADIOS)
        self._sliceMode.setVisible(mode == _DisplayMode.SLICES)
        if mode is _DisplayMode.RADIOS:
            config = mode, self.getRadioOption()
        elif mode is _DisplayMode.SLICES:
            config = mode, self.getSliceOption()
        else:
            raise ValueError("mode should be RADIOS or SLICES")
        if config != self._lastConfig:
            self._lastConfig = config
            self.sigDisplayModeChanged.emit()

    def setScanName(self, scan_name: str):
        self._scanQLE.setText(scan_name)


class ImageStack(_ImageStack):
    def __init__(self, parent):
        self._normFct = None
        self._url_indexes = None
        super(ImageStack, self).__init__(parent)
        # hide axis to be display
        self._plot.getPlotWidget().setAxesDisplayed(False)

        # add dock widget for reconstruction parameters
        self._reconsInfoDockWidget = qt.QDockWidget(parent=self)
        self._reconsWidgetScrollArea = qt.QScrollArea(self)
        self._reconsWidget = _ReconstructionParameters(self)
        self._reconsWidgetScrollArea.setWidget(self._reconsWidget)
        self._reconsInfoDockWidget.setWidget(self._reconsWidgetScrollArea)
        self._reconsInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._reconsInfoDockWidget)

    def setSliceReconsParamsVisible(self, visible):
        self._reconsInfoDockWidget.setVisible(visible)

    def setNormalizationFct(self, fct, url_indexes=None):
        self._normFct = fct
        self._url_indexes = url_indexes

    def _urlLoaded(self) -> None:
        """

        :param url: result of DataUrl.path() function
        :return:
        """
        sender = self.sender()
        url = sender.url.path()
        if self._urlIndexes is not None and url in self._urlIndexes:
            data = sender.data
            if data is None:
                _logger.warning("no data found (is the url valid ?) " + url)
                return

            if data.ndim != 2:
                if data.ndim == 3 and data.shape[0] == 1:
                    data = data.reshape((data.shape[1], data.shape[2]))
                else:
                    _logger.warning("Image Stack only manage 2D data")
                    return
            if self._normFct is None:
                self._urlData[url] = data
            else:
                norm_data = self._normFct(data, index=self._urlIndexes[url])
                self._urlData[url] = norm_data

            if self.getCurrentUrl().path() == url:
                self._plot.setData(self._urlData[url])
                self._reconsWidget.setUrl(url)

            if sender in self._loadingThreads:
                self._loadingThreads.remove(sender)
            self.sigLoaded.emit(url)

    def setUrls(self, urls: list):
        _ImageStack.setUrls(self, urls)
        listWidget = self._urlsTable._urlsTable._listWidget
        items = []
        for i in range(listWidget.count()):
            # TODO: do this on the fly
            item = listWidget.item(i)
            try:
                url = DataUrl(path=item.text())
            except Exception:
                _logger.info(
                    "fail to deduce data of last modification for "
                    "{}".format(item.text())
                )
            else:
                if os.path.exists(url.file_path()):
                    lst_m = time.ctime(os.path.getmtime(url.file_path()))
                    item.setToolTip("last modification : {}".format(lst_m))
            items.append(listWidget.item(i))


class _ReconstructionParameters(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())
        # method
        self._methodQLE = qt.QLineEdit("", self)
        self.layout().addRow("method", self._methodQLE)
        # paganin
        self._paganinCB = qt.QCheckBox("", self)
        self._paganinCB.setEnabled(False)
        self.layout().addRow("pagagnin", self._paganinCB)
        # delta beta
        self._deltaBetaQLE = qt.QLineEdit("", self)
        self._deltaBetaQLE.setReadOnly(True)
        self.layout().addRow(" / ".join((DELTA_CHAR, BETA_CHAR)), self._deltaBetaQLE)
        # distance
        self._distanceQLE = qt.QLineEdit("", self)
        self._distanceQLE.setReadOnly(True)
        self.layout().addRow("distance (cm)", self._distanceQLE)
        # pixel size
        self._pixelSizeQLE = qt.QLineEdit("", self)
        self._pixelSizeQLE.setReadOnly(True)
        self.layout().addRow("pixel size (cm)", self._pixelSizeQLE)
        # cor
        self._corQLE = qt.QLineEdit("", self)
        self._corQLE.setReadOnly(True)
        self.layout().addRow("cor (absolute)", self._corQLE)
        # padding type
        self._paddingTypeQLE = qt.QLineEdit("", self)
        self._paddingTypeQLE.setReadOnly(True)
        self.layout().addRow("padding type", self._paddingTypeQLE)
        # half tomo
        self._halfTomoCB = qt.QCheckBox("", self)
        self._halfTomoCB.setEnabled(False)
        self.layout().addRow("half tomo", self._halfTomoCB)
        # fbp filter type
        self._fbpFilterQLE = qt.QLineEdit("", self)
        self._fbpFilterQLE.setReadOnly(True)
        self.layout().addRow("fbp filter", self._fbpFilterQLE)
        # log min clip
        self._minLogClipQLE = qt.QLineEdit("", self)
        self._minLogClipQLE.setReadOnly(True)
        self.layout().addRow("log min clip", self._minLogClipQLE)
        # log max clip
        self._maxLogClipQLE = qt.QLineEdit("", self)
        self._maxLogClipQLE.setReadOnly(True)
        self.layout().addRow("log max clip", self._maxLogClipQLE)
        # software version
        self._softwareVersionQLE = qt.QLabel("", self)
        self.layout().addRow("software version", self._softwareVersionQLE)

    def setUrl(self, url):
        if isinstance(url, DataUrl):
            pass
        elif isinstance(url, str):
            url = DataUrl(path=url)
        else:
            raise TypeError(
                "url should be a DataUrl or a str representing"
                "an url and not {}".format(type(url))
            )
        for func in (
            self._setMethod,
            self._setPaganin,
            self.setDeltaBeta,
            self._setDistance,
            self._setPixelSize,
            self._setCor,
            self._setPaddingType,
            self._setHalfTomo,
            self._setFBPFilter,
            self._setMinLogClip,
            self._setMaxLogClip,
            self._setSoftwareVersion,
        ):
            func(url)

    @staticmethod
    def _decode_nabu_str(input):
        if hasattr(input, "decode"):
            input = input.decode("UTF-8")
        return input

    def _setMethod(self, url):
        def get_method_value():
            _NABU_METHOD_URL = "../../configuration/nabu_config/reconstruction/method"
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                method_path = os.path.normpath("/".join((data_path, _NABU_METHOD_URL)))
                if method_path in h5s:
                    return h5s[method_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_method_value())
        self._methodQLE.setText(value if value is not None else "")

    def _setPaganin(self, url):
        def is_phase_defined():
            _NABU_PHASE_URL = "../../configuration/nabu_config/phase"
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                phase_path = os.path.normpath("/".join((data_path, _NABU_PHASE_URL)))
                return phase_path in h5s

        self._paganinCB.setChecked(is_phase_defined())

    def setDeltaBeta(self, url):
        def get_delta_beta_value():
            _NABU_DELTA_BETA_URL = "../../configuration/nabu_config/phase/delta_beta"
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                delta_beta_path = os.path.normpath(
                    "/".join((data_path, _NABU_DELTA_BETA_URL))
                )
                if delta_beta_path in h5s:
                    return h5s[delta_beta_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_delta_beta_value())
        self._deltaBetaQLE.setText(str(value) if value is not None else "")

    def _setDistance(self, url):
        def get_distance_value():
            _NABU_DISTANCE_URL = (
                "../../configuration/processing_options/phase/distance_cm"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                distance_path = os.path.normpath(
                    "/".join((data_path, _NABU_DISTANCE_URL))
                )
                if distance_path in h5s:
                    return h5s[distance_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_distance_value())
        if value is not None:
            value = "{:.2}".format(float(value))
        self._distanceQLE.setText(value if value is not None else "")

    def _setPixelSize(self, url):
        def get_pixel_size_value():
            _NABU_PIXEL_SIZE_URL = (
                "../../configuration/processing_options/reconstruction/pixel_size_cm"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                pixel_size_path = os.path.normpath(
                    "/".join((data_path, _NABU_PIXEL_SIZE_URL))
                )
                if pixel_size_path in h5s:
                    return h5s[pixel_size_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_pixel_size_value())
        if value is not None:
            value = "{:.8}".format(float(value))
        self._pixelSizeQLE.setText(value if value is not None else "")

    def _setCor(self, url):
        def get_cor_value():
            _NABU_COR_URL = "../../configuration/processing_options/reconstruction/rotation_axis_position"
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                pixel_size_path = os.path.normpath("/".join((data_path, _NABU_COR_URL)))
                if pixel_size_path in h5s:
                    return h5s[pixel_size_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_cor_value())
        if value is not None:
            value = "{:.4}".format(float(value))
        self._corQLE.setText(value if value is not None else "")

    def _setPaddingType(self, url):
        def get_padding_type_value():
            _NABU_PADDING_URL = (
                "../../configuration/processing_options/reconstruction/padding_type"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                padding_path = os.path.normpath(
                    "/".join((data_path, _NABU_PADDING_URL))
                )
                if padding_path in h5s:
                    return h5s[padding_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_padding_type_value())
        self._paddingTypeQLE.setText(str(value) if value is not None else "")

    def _setHalfTomo(self, url):
        def get_half_tomo_value():
            _NABU_HALF_TOMO_URL = (
                "../../configuration/processing_options/reconstruction/enable_halftomo"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                half_tomo_path = os.path.normpath(
                    "/".join((data_path, _NABU_HALF_TOMO_URL))
                )
                if half_tomo_path in h5s:
                    return h5s[half_tomo_path][()]
                else:
                    return False

        value = get_half_tomo_value()
        self._halfTomoCB.setChecked(value)

    def _setFBPFilter(self, url):
        def get_fbp_filter_value():
            _NABU_FBP_FILTER_URL = (
                "../../configuration/processing_options/reconstruction/fbp_filter_type"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                fbp_filter_path = os.path.normpath(
                    "/".join((data_path, _NABU_FBP_FILTER_URL))
                )
                if fbp_filter_path in h5s:
                    return h5s[fbp_filter_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_fbp_filter_value())
        self._fbpFilterQLE.setText(str(value) if value is not None else "")

    def _setMinLogClip(self, url):
        def get_log_min_clip_value():
            _NABU_LOG_MIN_CLIP_URL = (
                "../../configuration/processing_options/take_log/log_min_clip"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                log_min_path = os.path.normpath(
                    "/".join((data_path, _NABU_LOG_MIN_CLIP_URL))
                )
                if log_min_path in h5s:
                    return h5s[log_min_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_log_min_clip_value())
        self._minLogClipQLE.setText(str(value) if value is not None else "")

    def _setMaxLogClip(self, url):
        def get_log_max_clip_value():
            _NABU_LOG_MAX_CLIP_URL = (
                "../../configuration/processing_options/take_log/log_max_clip"
            )
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                log_max_path = os.path.normpath(
                    "/".join((data_path, _NABU_LOG_MAX_CLIP_URL))
                )
                if log_max_path in h5s:
                    return h5s[log_max_path][()]
                else:
                    return None

        value = self._decode_nabu_str(get_log_max_clip_value())
        self._maxLogClipQLE.setText(str(value) if value is not None else "")

    def _setSoftwareVersion(self, url):
        _NABU_VERSION_URL = "../../configuration/nabu_config/about/nabu_version"

        def get_nabu_software_verion():
            with HDF5File(url.file_path(), "r") as h5s:
                data_path = url.data_path()
                soft_version_path = os.path.normpath(
                    "/".join((data_path, _NABU_VERSION_URL))
                )
                if soft_version_path in h5s:
                    return h5s[soft_version_path][()]
                else:
                    return None

        software = software_version = ""
        nabu_version = self._decode_nabu_str(get_nabu_software_verion())
        if nabu_version is not None:
            software = "nabu"
            software_version = nabu_version
        self._softwareVersionQLE.setText("{} ({})".format(software, software_version))


class _TomwerUrlLoader(UrlLoader):
    """
    Thread use to load DataUrl
    """

    def __init__(self, parent, url):
        super(UrlLoader, self).__init__(parent=parent)
        assert isinstance(url, DataUrl)
        self.url = url
        self.data = None

    def run(self):
        if self.url.file_path().endswith(".vol"):
            self.data = self._load_vol()
        elif self.url.scheme() == "numpy":
            data = numpy.load(self.url.file_path())
            if isinstance(data, numpy.lib.npyio.NpzFile):
                data = data["result"]
            self.data = data
        elif self.url.scheme() == "tomwer":
            if has_PIL:
                self.data = numpy.array(Image.open(self.url.file_path()))
                if self.url.data_slice() is not None:
                    self.data = self.data[self.url.data_slice()]
            else:
                _logger.warning(
                    "need to install Pillow to read file " + self.url.file_path()
                )
                self.data = None
        else:
            try:
                self.data = get_data(self.url)
            except IOError:
                self.data = None
            except ValueError:
                self.data = None
                _logger.warning(
                    "Fail to open {}. Maybe the reconstruction failed.".format(
                        self.url.path()
                    )
                )

    def _load_vol(self):
        """
        load a .vol file
        """
        if self.url.file_path().lower().endswith(".vol.info"):
            info_file = self.url.file_path()
            raw_file = self.url.file_path().replace(".vol.info", ".vol")
        else:
            assert self.url.file_path().lower().endswith(".vol")
            raw_file = self.url.file_path()
            info_file = self.url.file_path().replace(".vol", ".vol.info")

        if not os.path.exists(raw_file):
            data = None
            mess = "Can't find raw data file %s associated with {}" "".format(
                raw_file, info_file
            )
            _logger.warning(mess)
        elif not os.path.exists(info_file):
            mess = "Can't find info file {} associated with {}" "".format(
                info_file, raw_file
            )
            _logger.warning(mess)
            data = None
        else:
            shape = get_vol_file_shape(info_file)
            if None in shape:
                _logger.warning("Fail to retrieve data shape for %s." % info_file)
                data = None
            else:
                try:
                    numpy.zeros(shape)
                except MemoryError:
                    data = None
                    _logger.warning(
                        "Raw file %s is too large for being " "read {}".format(raw_file)
                    )
                else:
                    data = numpy.fromfile(
                        raw_file, dtype=numpy.float32, count=-1, sep=""
                    )
                    try:
                        data = data.reshape(shape)
                    except ValueError:
                        _logger.warning(
                            "unable to fix shape for raw file {}. "
                            "Look for information in {}"
                            "".format(raw_file, info_file)
                        )
                        try:
                            sqr = int(numpy.sqrt(len(data)))
                            shape = (1, sqr, sqr)
                            data = data.reshape(shape)
                        except ValueError:
                            _logger.info(
                                "deduction of shape size for {} "
                                "failed".format(raw_file)
                            )
                            data = None
                        else:
                            _logger.warning(
                                "try deducing shape size for {}} "
                                "might be an incorrect "
                                "interpretation".format(raw_file)
                            )
        if self.url.data_slice() is None:
            return data
        else:
            return data[self.url.data_slice()]
