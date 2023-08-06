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
__date__ = "05/04/2019"


import shutil
import tempfile
import unittest
import numpy
import os
import fabio
import h5py
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.test.utils import UtilsTest
from tomwer.core.utils.scanutils import MockEDF, MockHDF5
from ..reconstruction.axis.axis import AxisProcess
from ..reconstruction.axis.axis import compute_near
from ..reconstruction.axis.axis import compute_scan_near
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.process.reconstruction.axis.params import AxisRP
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.baseprocess import BaseProcess
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from silx.io.url import DataUrl


class _AxisDataset:
    def __init__(self, name):
        self.name = name


class TestAxisIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    @staticmethod
    def _random_calc(scan):
        return numpy.random.random()

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.scan = MockEDF.mockScan(scanID=self.scan_folder,
                                     nRadio=10,
                                     nRecons=1,
                                     nPagRecons=4,
                                     dim=10)
        self.recons_params = AxisRP()
        self.axis_process = AxisProcess(self.recons_params)

        # set the axis url to be used
        projections = self.scan.projections
        urls = list(projections.values())
        self.scan.axis_params = AxisRP()
        self.scan.axis_params.axis_url_1 = urls[0]
        self.scan.axis_params.axis_url_2 = urls[1]

        # patch the axis process
        self.axis_process.RADIO_CALCULATIONS_METHODS[AxisMode.centered] = TestAxisIO._random_calc


    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        # for input_type in (dict, TomoBase):
        for input_type in (TomwerScanBase,):
            for _input in AxisProcess.inputs:
                for return_dict in (True, False):
                    with self.subTest(handler=_input.handler,
                                      return_dict=return_dict,
                                      input_type=input_type):
                        input_obj = self.scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        self.axis_process._set_return_dict(return_dict)
                        out = getattr(self.axis_process, _input.handler)(input_obj)
                        if return_dict:
                            self.assertTrue(isinstance(out, dict))
                        else:
                            self.assertTrue(isinstance(out, TomwerScanBase))


@unittest.skip('Axis algorithm are pending at the moment')
class TestAxisComputation(unittest.TestCase):
    """Test functions used for computing the center of rotation"""
    def setUp(self):
        unittest.TestCase.setUp(self)
        # create a folder with an unfinished acquisition
        self.tmp_folder = tempfile.mkdtemp()

    def tearDown(self):
        # create a folder with an unfinished acquisition
        if os.path.exists(self.tmp_folder):
            shutil.rmtree(path=self.tmp_folder)
        unittest.TestCase.tearDown(self)

    def test_compute_near(self):
        """Test results of the near algorithm"""
        dataset1 = _AxisDataset('00021_PURfoam2_0N_500angles')
        dataset1.radio_1 = '00021_PURfoam2_0N_500angles3000.edf'
        dataset1.radio_2 = '00021_PURfoam2_0N_500angles3002.edf'
        dataset1.near_positions = (0.0, 1.1)
        dataset1.window_sizes = (2, 5, 10)
        dataset1.fine_steps = (0.1, )
        dataset1.look_at_stdmax = (False, )

        for dataset in (dataset1, ):
            for near_position in dataset.near_positions:
                for window_size in dataset.window_sizes:
                    for fine_step in dataset.fine_steps:
                        for look_at_stdmax in dataset.look_at_stdmax:
                            self.subTest("near cor calculation",
                                         radios=(dataset.radio_1, dataset.radio_2),
                                         near_position=near_position,
                                         look_at_stdmax=look_at_stdmax,
                                         fine_step=fine_step,
                                         window_size=window_size)

                            scan_dir = os.path.join(
                                UtilsTest.getDatasets(name='axis'),
                                dataset.name)
                            file1 = os.path.join(scan_dir, dataset.radio_1)
                            file2 = os.path.join(scan_dir, dataset.radio_2)

                            with fabio.open(file1) as _f:
                                radio1 = _f.data
                            with fabio.open(file2) as _f:
                                radio2 = _f.data
                            radio1, radio2 = self.apply_home_made_normalization(
                                radio1=radio1,
                                radio2=radio2,
                                scan_dir=scan_dir,
                                use_log=False)

                            res = compute_near(radio_1=radio1,
                                               radio_2=radio2,
                                               near_pos=near_position,
                                               window_size=window_size,
                                               fine_step_x=fine_step,
                                               look_at_stdmax=look_at_stdmax)
                            self.assertTrue(
                                numpy.isclose(res, self.th_res_near(name=dataset.name,
                                                                    near_pos=near_position,
                                                                    window_size=window_size,
                                                                    fine_step=fine_step,
                                                                    look_at_stdmax=look_at_stdmax))
                            )

    def test_img_scale(self):
        """Test the algorithm within the scale_img2_to_img1 option"""
        dataset = _AxisDataset('A2_550N_20k_')
        dataset.radio_1 = 'A2_550N_20k_2499.edf'
        dataset.radio_2 = 'A2_550N_20k_2501.edf'

        scan_dir = os.path.join(UtilsTest.getDatasets(name='axis'), dataset.name)
        scan = EDFTomoScan(scan_dir)
        scan.axis_params = AxisRP()
        scan.axis_params.axis_url_1 = DataUrl(file_path=os.path.join(scan.path, dataset.radio_1),
                                              scheme='fabio', data_slice=(0,))
        scan.axis_params.axis_url_2 = DataUrl(file_path=os.path.join(scan.path, dataset.radio_2),
                                              scheme='fabio', data_slice=(0,))
        scan.axis_params.calculation_input_type = AxisCalculationInput.emission
        scan.axis_params.scale_im2_to_im1 = True

        self.assertTrue(numpy.isclose(compute_scan_global(scan=scan), 256.0))

        scan.axis_params.mode = AxisMode.near
        scan.axis_params.fine_step_x = 0.1
        scan.axis_params.near_wx = 5
        scan.axis_params.look_at_std_max = False
        scan.axis_params.near_position = 255.5
        self.assertTrue(numpy.isclose(compute_scan_near(scan=scan), 257.8))

    def th_res_near(self, name, near_pos, window_size, fine_step, look_at_stdmax):
        if name == '00021_PURfoam2_0N_500angles':
            if near_pos == 0 and fine_step == 0.1 and look_at_stdmax:
                if window_size == 5:
                    return 2.65
                elif window_size == 10:
                    return -4.35
                elif window_size == 2:
                    return 0.65
            elif near_pos == 0 and fine_step == 0.1 and not look_at_stdmax:
                if window_size == 5:
                    return 0.3
                elif window_size == 10:
                    return -3.2
                elif window_size == 2:
                    return 0.3
            elif near_pos == 1.1 and fine_step == 0.1 and look_at_stdmax:
                if window_size == 5:
                    return 2.65
                elif window_size == 10:
                    return -3.95
                elif window_size == 2:
                    return 2.2
            elif near_pos == 1.1 and fine_step == 0.1 and not look_at_stdmax:
                if window_size == 5:
                    return 0.3
                elif window_size == 10:
                    return -3.2
                elif window_size == 2:
                    return 0.3

    def apply_home_made_normalization(self, radio1, radio2, scan_dir, use_log):
        refMat = numpy.zeros_like(radio1)
        darkMat = numpy.zeros_like(radio1)
        reflist = DarkRefs.getRefHSTFiles(scan_dir, prefix='ref')
        darklist = DarkRefs.getDarkHSTFiles(scan_dir,
                                            prefix='dark')

        for reffile in reflist:
            fd = fabio.open(reffile)
            refMat = refMat + fd.data
            fd.close()

        refMat = refMat / len(reflist)

        for darkfile in darklist:
            fd = fabio.open(darkfile)
            darkMat = darkMat + fd.data
            fd.close()

        darkMat = darkMat / len(darklist)
        refMat -= darkMat
        refMat[refMat < 1] = 1.

        radio1 = (radio1 - darkMat) / refMat
        radio2 = (radio2 - darkMat) / refMat

        if use_log is True:
            radio1 = -numpy.log(radio1)
            radio2 = -numpy.log(radio2)

        radio1[numpy.isnan(radio1)] = 0.0001
        radio2[numpy.isnan(radio2)] = 0.0001
        return radio1, radio2

    def th_res(self, name, use_log):
        if name == '00021_PURfoam2_0N_500angles':
            if use_log is True:
                return 9.040816326530603
            else:
                return -319.84375


class TestAxis(unittest.TestCase):
    """Test the axis process"""
    def setUp(self):
        self.recons_params = AxisRP()
        self.axis_process = AxisProcess(axis_params=self.recons_params)
        self.recons_params.mode = 'accurate'

    # def test_no_axis_files(self):
    #     """Test that if no projections are found for computing axis the process
    #     will return None"""
    #     scan = ScanFactory.mock_scan()
    #     self.assertEqual(self.axis_process.process(scan=scan), None)

    def test_process_saved_edf(self):
        """Test that if process is called, the tomwer.h5 file is created
        and is correctly saving information regarding the center of position
        """
        self.tempdir = tempfile.mkdtemp()
        mock = MockEDF(scan_path=self.tempdir, n_radio=10, n_ini_radio=10)
        scan = EDFTomoScan(mock.scan_path)
        self.recons_params.mode = 'near'
        self.axis_process.process(scan=scan)
        self.assertTrue(os.path.exists(scan.process_file))

        with h5py.File(scan.process_file, 'r', swmr=True) as h5f:
            self.assertTrue('entry' in h5f)
            self.assertTrue('tomwer_process_0' in h5f['entry'])
            group_axis = h5f['entry']['tomwer_process_0']
            self.assertTrue('configuration' in group_axis)
            self.assertTrue('program' in group_axis)
            self.assertTrue('results' in group_axis)
            self.assertTrue('center_of_rotation' in group_axis['results'])
            axis_value = group_axis['results']['center_of_rotation'][()]

        processes = BaseProcess.get_processes_frm_type(process_file=scan.process_file,
                                                       process_type=AxisProcess,
                                                       entry='entry')
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].results['center_of_rotation'], axis_value)

        # make sure the process file can be loaded by an instance of AxisRP
        new_axis_params = AxisRP()
        new_axis_params.value = -10000
        new_axis_params.set_position_frm_par_file(file_path=scan.process_file,
                                                  entry=None)
        self.assertEqual(new_axis_params.value, scan.axis_params.value)

    def test_process_saved_hdf5(self):
        """Test that if process is called, the tomwer.h5 file is created
        and is correctly saving information regarding the center of position
        """
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockHDF5(scan_path=self.tempdir, n_proj=10, n_ini_proj=10,
                        scan_range=180, dim=dim)
        mock.add_alignment_radio(index=10, angle=90)
        mock.add_alignment_radio(index=10, angle=0)
        scan = mock.scan
        self.recons_params.mode = 'near'

        # check data url take
        self.axis_process.process(scan=scan)
        # make sure center of position has been computed
        self.assertTrue(os.path.exists(scan.process_file))

        with h5py.File(scan.process_file, 'r', swmr=True) as h5f:
            self.assertTrue('entry' in h5f)
            self.assertTrue('tomwer_process_0' in h5f['entry'])
            group_axis = h5f['entry']['tomwer_process_0']
            self.assertTrue('configuration' in group_axis)
            self.assertTrue('program' in group_axis)
            self.assertTrue('results' in group_axis)
            self.assertTrue('center_of_rotation' in group_axis['results'])
            axis_value = group_axis['results']['center_of_rotation'][()]

        self.assertTrue(-dim / 2 <= axis_value <= dim / 2)
        processes = BaseProcess.get_processes_frm_type(
            process_file=scan.process_file,
            process_type=AxisProcess)
        self.assertEqual(len(processes), 1)
        self.assertEqual(processes[0].results['center_of_rotation'],
                         axis_value)

        # make sure the process file can be loaded by an instance of AxisRP
        new_axis_params = AxisRP()
        new_axis_params.value = -10000
        new_axis_params.set_position_frm_par_file(
            file_path=scan.process_file)
        self.assertEqual(new_axis_params.value, scan.axis_params.value)


class TestAxisRP(unittest.TestCase):
    """Test the class used for AxisProcess configuration"""
    def setUp(self):
        self.axis_rp = AxisRP()
        self.tmp_folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_folder)

    def testSetPositionFromParFile(self):
        """Test that the position can be managed from a par file"""
        old_value = self.axis_rp.value

        with self.assertRaises(ValueError):
            self.axis_rp.set_position_frm_par_file('ghost_file.par', force=False)
        self.assertTrue(self.axis_rp.value == old_value)

        existing_empty_file = os.path.join(self.tmp_folder, 'par_file.par')
        with open(existing_empty_file, 'w') as _file:
            _file.write('toto')

        with self.assertRaises(KeyError):
            self.axis_rp.set_position_frm_par_file(existing_empty_file, force=False)
        self.assertTrue(self.axis_rp.value == old_value)

        valid_par_file = os.path.join(UtilsTest.getEDFDataset('scan_3_'), 'scan_3_slice.par')
        assert os.path.isfile(valid_par_file)
        self.axis_rp.set_position_frm_par_file(valid_par_file, force=False)
        self.assertTrue(self.axis_rp.value == 1024.742042)

        self.axis_rp.set_position_frm_par_file(existing_empty_file, force=True)
        self.assertTrue(self.axis_rp.value is None)

        self.axis_rp.set_position_frm_par_file('ghost_file.par', force=True)
        self.assertTrue(self.axis_rp.value is None)

        self.axis_rp.set_position_frm_par_file(valid_par_file, force=True)
        self.assertTrue(self.axis_rp.value == 1024.742042)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestAxisIO, TestAxisComputation, TestAxis, TestAxisRP):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
