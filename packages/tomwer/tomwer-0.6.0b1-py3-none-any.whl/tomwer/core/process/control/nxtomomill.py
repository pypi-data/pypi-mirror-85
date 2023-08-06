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
__date__ = "30/07/2020"


from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from nxtomomill import converter as nxtomomill_converter
from tomwer.core.scan.scanbase import TomwerScanBase
import os
import logging

_logger = logging.getLogger(__name__)


class NxTomomillProcess(SingleProcess):
    """
    Process to convert from a bliss dataset to a nexus compliant dataset
    """

    inputs = [
        _input_desc(name="data", type=BlissScan, handler="process", doc="scan path")
    ]

    outputs = [_output_desc(name="data", type=TomwerScanBase, doc="scan path")]

    @staticmethod
    def deduce_output_file_path(master_file_name, entry):
        file_dir = os.path.dirname(master_file_name)
        file_name = os.path.basename(master_file_name)
        if "." in file_name:
            file_name = "".join(file_name.split(".")[:-1])

        entry_for_file_name = entry.lstrip("/")
        entry_for_file_name = entry_for_file_name.replace("/", "_")
        entry_for_file_name = entry_for_file_name.replace(".", "_")
        entry_for_file_name = entry_for_file_name.replace(":", "_")
        output_file_name = "_".join(
            (os.path.splitext(file_name)[0], entry_for_file_name + ".nx")
        )
        return os.path.join(file_dir, output_file_name)

    def process(self, scan=None):
        if scan is None:
            return
        _logger.processStarted("Start translate {} to NXTomo".format(str(scan)))
        if isinstance(scan, dict):
            scan = BlissScan.from_dict(scan)

        assert isinstance(scan, BlissScan)
        output_file_path = self.deduce_output_file_path(
            master_file_name=scan.master_file, entry=scan.entry
        )
        _logger.info(" ".join(("write", str(scan), "to", output_file_path)))
        try:
            conv = nxtomomill_converter.h5_to_nx(
                input_file_path=scan.master_file,
                output_file=output_file_path,
                entries=(scan.entry,),
                single_file=True,
                ask_before_overwrite=False,
                file_extension=".nx",
            )
        except Exception as e:
            _logger.processFailed(
                "Fail to convert from bliss file: %s to NXTomo."
                "Conversion error is: %s" % (scan.master_file, e)
            )
            return None
        else:
            if len(conv) != 1:
                _logger.processFailed(
                    "Something went wrong during file conversion. Unable to "
                    "process the file."
                )
                return None
            else:
                conv_file, conv_entry = conv[0]
                scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
                _logger.processSucceed(
                    "{} has been translated to {}"
                    "".format(str(scan), str(scan_converted))
                )
                return scan_converted

    def set_properties(self, properties):
        # for now the NXProcess cannot be tune
        pass
