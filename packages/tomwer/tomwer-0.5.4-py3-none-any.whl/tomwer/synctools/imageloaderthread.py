#/*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
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
__date__ = "02/06/2017"

from silx.gui import qt
import numpy
import numpy.lib.npyio
import os
from silx.io.utils import get_data as silx_get_data
from tomwer.core.utils import ftseriesutils
import tomwer.resources
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageLoaderThread(qt.QThread):
    """Thread used to load an image"""
    IMG_NOT_FOUND = numpy.load(
            tomwer.resources._resource_filename('%s.%s' % ('imageNotFound', 'npy'),
                                                default_directory=os.path.join(
                                                        'gui', 'icons'))
    )


    def __init__(self, url):
        """

        :param index: index of the image on the stackplot
        :param filePath: filePath is the file to load on stackplot reference.
                         It can be an .edf file or a .vol file. If this is a
                         vol file then the name is given with the slice z index
                         to be loaded.
        """
        super(qt.QThread, self).__init__()
        self.data = None
        self.url = url

    def getData(self):
        if hasattr(self, 'data'):
            return self.data
        else:
            return None

    def run(self):
        if os.path.exists(self.url.file_path()) and os.path.isfile(self.url.file_path()):
            if (self.url.file_path().lower().endswith('.vol.info') or
                    self.url.file_path().lower().endswith('.vol')):
                self.data = self._loadVol()
            elif self.url.scheme() == 'numpy':
                data = numpy.load(self.url.file_path())
                if isinstance(data, numpy.lib.npyio.NpzFile):
                    self.data = data['result']
                self.data = data
            elif self.url.scheme() == 'tomwer':
                self.data = numpy.array(Image.open(self.url.file_path()))
                if self.url.data_slice() is not None:
                    self.data = self.data[self.url.data_slice()]
            else:
                try:
                    self.data = silx_get_data(self.url)
                except Exception as e:
                    logger.error(e)
                    logger.warning(
                        'file %s not longer exists or is empty' % self.url)
                    self.data = None
        else:
            logger.warning('file %s not longer exists or is empty' % self.url)
            self.data = self.IMG_NOT_FOUND

    def _loadVol(self):
        if self.url.file_path().lower().endswith('.vol.info'):
            infoFile = self.url.file_path()
            rawFile = self.url.file_path().replace('.vol.info', '.vol')
        else:
            assert self.url.file_path().lower().endswith('.vol')
            rawFile = self.url.file_path()
            infoFile = self.url.file_path().replace('.vol', '.vol.info')

        if not os.path.exists(rawFile):
            data = None
            mess = "Can't find raw data file %s associated with %s" % (rawFile, infoFile)
            logger.warning(mess)
        elif not os.path.exists(infoFile):
            mess = "Can't find info file %s associated with %s" % (infoFile, rawFile)
            logger.warning(mess)
            data = None
        else:
            shape = ftseriesutils.get_vol_file_shape(infoFile)
            if None in shape:
                logger.warning(
                    'Fail to retrieve data shape for %s.' % infoFile)
                data = None
            else:
                try:
                    numpy.zeros(shape)
                except MemoryError:
                    data = None
                    logger.warning('Raw file %s is to large for being '
                                   'readed %s' % rawFile)
                else:
                    data = numpy.fromfile(rawFile, dtype=numpy.float32,
                                          count=-1, sep='')
                    try:
                        data = data.reshape(shape)
                    except ValueError:
                        logger.warning('unable to fix shape for raw file %s. '
                                       'Look for information in %s'
                                       '' % (rawFile, infoFile))
                        try:
                            sqr = int(numpy.sqrt(len(data)))
                            shape = (1, sqr, sqr)
                            data = data.reshape(shape)
                        except ValueError:
                            logger.info('deduction of shape size for %s failed'
                                        % rawFile)
                            data = None
                        else:
                            logger.warning('try deducing shape size for %s '
                                           'might be an incorrect '
                                           'interpretation' % rawFile)
        if self.url.data_slice() is None:
            return data
        else:
            return data[self.url.data_slice()]
