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
__date__ = "24/01/2017"

import logging
import os
import shutil
import tempfile
import time
import unittest

from silx.gui import qt
from orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW import (
    DarkRefAndCopyOW,
)
from tomwer.core.process.reconstruction.darkref.params import Method as DkrfMethod
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui.reconstruction.ftserie import FtserieWidget
from tomwer.gui.qtapplicationmanager import QApplicationManager
from tomwer.gui.reconstruction.darkref.darkrefcopywidget import DarkRefAndCopyWidget
from tomwer.synctools.ftseries import QReconsParams
from tomwer.test.utils import UtilsTest
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.utils.scanutils import MockHDF5, MockEDF
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.process.reconstruction.darkref.settings import (
    DARKHST_PREFIX,
    REFHST_PREFIX,
)

_qapp = QApplicationManager()

logging.disable(logging.INFO)


class TestEDFDarkRefWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._recons_params = QReconsParams()
        self.widget = DarkRefAndCopyOW(
            parent=None, reconsparams=self._recons_params.dkrf
        )

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        TestCaseQt.tearDown(self)

    def testSyncRead(self):
        """Make sure any modification on the self._reconsParams is
        applied on the GUI"""
        rp = self._recons_params
        self.assertTrue(rp.dkrf["REFSRMV"] is False)
        self.assertFalse(
            self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        )
        rp.dkrf["REFSRMV"] = True
        self.assertTrue(
            self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        )

        pattern = self.widget.widget.mainWidget.tabExpert._refLE.text()
        newText = "popo.*"
        assert pattern != newText
        rp.dkrf["RFFILE"] = newText
        self.assertTrue(
            self.widget.widget.mainWidget.tabExpert._refLE.text() == newText
        )

    def testSyncWrite(self):
        """Test that if we edit through the :class:`DarkRefWidget` then the
        modification are fall back into the self._reconsParams"""
        rp = self._recons_params

        # test patterns
        pattern = self.widget.widget.mainWidget.tabExpert._refLE.text()
        newText = "popo.*"
        assert pattern != newText
        self.widget.widget.mainWidget.tabExpert._refLE.setText(newText)
        self.widget.widget.mainWidget.tabExpert._refLE.editingFinished.emit()
        qt.QApplication.instance().processEvents()
        self.assertTrue(rp.dkrf["RFFILE"] == newText)
        self.widget.widget.mainWidget.tabExpert._darkLE.setText(newText)
        self.widget.widget.mainWidget.tabExpert._darkLE.editingFinished.emit()
        qt.QApplication.instance().processEvents()
        self.assertTrue(rp.dkrf["DKFILE"] == newText)

        # test calc mode
        self.widget.widget.mainWidget.tabGeneral._darkWCB.setMode(DkrfMethod.none)
        self.widget.widget.mainWidget.tabGeneral._refWCB.setMode(DkrfMethod.median)
        self.assertTrue(rp.dkrf["DARKCAL"] == DkrfMethod.none)
        self.assertTrue(rp.dkrf["REFSCAL"] == DkrfMethod.median)

        # test options
        cuRm = self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        self.widget.widget.mainWidget.tabGeneral._rmOptionCB.setChecked(not cuRm)
        self.assertTrue(rp.dkrf["REFSRMV"] == (not cuRm))
        self.assertTrue(rp.dkrf["DARKRMV"] == (not cuRm))

        cuSkip = self.widget.widget.mainWidget.tabGeneral._skipOptionCB.isChecked()
        self.widget.widget.mainWidget.tabGeneral._skipOptionCB.setChecked(not cuSkip)
        # warning : here value of skip and overwrite are of course inverse
        self.assertTrue(rp.dkrf["DARKOVE"] == cuSkip)
        self.assertTrue(rp.dkrf["REFSOVE"] == cuSkip)

    def testBehaviorWithFtserie(self):
        """
        Make sure modification on ftserie 'Dark and flat field' tab are
        correctly take into account in this case they are working on the same
        QReconsParams object
        """
        ftserie = FtserieWidget(recons_params=self._recons_params)

        cuRm = ftserie.getReconsParamSetEditor()._dkRefWidget._qcbRmRef.isChecked()
        cuSkip = ftserie.getReconsParamSetEditor()._dkRefWidget._qcbSkipRef.isChecked()
        calcDK = ftserie.getReconsParamSetEditor()._dkRefWidget._qcbDKMode.getMode()
        calcRef = ftserie.getReconsParamSetEditor()._dkRefWidget._qcbRefMode.getMode()
        patternRef = (
            ftserie.getReconsParamSetEditor()._dkRefWidget._qleRefsPattern.text()
        )
        patternDK = ftserie.getReconsParamSetEditor()._dkRefWidget._qleDKPattern.text()

        # make sure initial status are the same between ftserie and darkref
        dkrfOWMainWidget = self.widget.widget.mainWidget
        self.assertTrue(dkrfOWMainWidget.tabGeneral._rmOptionCB.isChecked() == cuRm)
        self.assertTrue(dkrfOWMainWidget.tabGeneral._skipOptionCB.isChecked() == cuSkip)
        self.assertTrue(dkrfOWMainWidget.tabGeneral._darkWCB.getMode() == calcDK)
        self.assertTrue(dkrfOWMainWidget.tabGeneral._refWCB.getMode() == calcRef)
        self.assertTrue(dkrfOWMainWidget.tabExpert._refLE.text() == patternRef)
        self.assertTrue(dkrfOWMainWidget.tabExpert._darkLE.text() == patternDK)

        # change parameters
        ftserie.getReconsParamSetEditor()._dkRefWidget._qcbRmRef.setChecked(not cuRm)
        ftserie.getReconsParamSetEditor()._dkRefWidget._qcbSkipRef.setChecked(
            not cuSkip
        )
        ftserie.getReconsParamSetEditor()._dkRefWidget._qcbDKMode.setMode("none")
        ftserie.getReconsParamSetEditor()._dkRefWidget._qcbRefMode.setMode("average")
        text_ref_pattern = "toto.*"
        text_dk_pattern = "[maestro]?."
        ftserie.getReconsParamSetEditor()._dkRefWidget._qleDKPattern.setText(
            text_dk_pattern
        )
        ftserie.getReconsParamSetEditor()._dkRefWidget._qleDKPattern.editingFinished.emit()
        qt.QApplication.instance().processEvents()
        ftserie.getReconsParamSetEditor()._dkRefWidget._qleRefsPattern.setText(
            text_ref_pattern
        )
        ftserie.getReconsParamSetEditor()._dkRefWidget._qleRefsPattern.editingFinished.emit()
        qt.QApplication.instance().processEvents()

        # check modification are well take into account
        self.assertTrue(
            dkrfOWMainWidget.tabGeneral._rmOptionCB.isChecked() == (not cuRm)
        )
        self.assertTrue(self._recons_params.dkrf["DARKRMV"] == (not cuRm))
        self.assertTrue(
            dkrfOWMainWidget.tabGeneral._skipOptionCB.isChecked() == (not cuSkip)
        )
        self.assertTrue(self._recons_params.dkrf["DARKOVE"] == cuSkip)
        self.assertTrue(
            dkrfOWMainWidget.tabGeneral._darkWCB.getMode() == DkrfMethod.none
        )
        self.assertTrue(self._recons_params.dkrf["DARKCAL"] == DkrfMethod.none)
        self.assertTrue(
            dkrfOWMainWidget.tabGeneral._refWCB.getMode() == DkrfMethod.average
        )
        self.assertTrue(self._recons_params.dkrf["REFSCAL"] == DkrfMethod.average)
        self.assertTrue(self._recons_params.dkrf["DKFILE"] == text_dk_pattern)
        self.assertTrue(self._recons_params.dkrf["RFFILE"] == text_ref_pattern)
        self.assertTrue(dkrfOWMainWidget.tabExpert._refLE.text() == text_ref_pattern)
        self.assertTrue(dkrfOWMainWidget.tabExpert._darkLE.text() == text_dk_pattern)


@unittest.skipIf(
    UtilsTest.getInternalTestDir("testslicesNemoz6x") is None, "No extra datatset"
)
class TestID16TestCase(TestCaseQt):
    """
    class testing the process of the dark ref widget in the case of ID16
    """

    def setUp(self):
        TestCaseQt.setUp(self)
        datasetDir = UtilsTest.getInternalTestDir("testslicesNemoz6x")
        self._tmpDir = tempfile.mkdtemp()
        self.datasets = []
        for subFolder in (
            "testslicesNemoz61_1_",
            "testslicesNemoz62_1_",
            "testslicesNemoz63_1_",
            "testslicesNemoz64_1_",
            "testslicesNemoz65_1_",
        ):
            shutil.copytree(
                os.path.join(datasetDir, subFolder),
                os.path.join(self._tmpDir, subFolder),
            )
            self.datasets.append(os.path.join(self._tmpDir, subFolder))

        self.recons_params = QReconsParams()
        self.recons_params.dkrf.remove_dark = True
        self.recons_params.dkrf.remove_ref = True
        self.widget = DarkRefAndCopyWidget(
            parent=None, reconsparams=self.recons_params.dkrf
        )
        self.widget.setForceSync(True)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._tmpDir)
        TestCaseQt.tearDown(self)

    def test(self):
        """make sure the behavior of dark ref is correct for id16b pipeline:
        datasets is composed of :

        - testslicesNemoz61_1_: contains original dark and ref. DarkRef should
           process those to generate median ref and dark
        - testslicesNemoz62_1_, testslicesNemoz63_1_, testslicesNemoz64_1_:
           contains no ref or dark orignals or median.
           should copy the one normalized from testslicesNemoz61_1_
        testslicesNemoz65_1_: contains dark median. Should copy ref from
            testslicesNemoz61_1_
        """
        # check behavior for testslicesNemoz61_1_.
        files = os.listdir(self.datasets[0])
        assert "darkend0000.edf" in files
        assert "ref0000_0000.edf" in files
        assert "ref0000_0050.edf" in files
        assert "ref0001_0000.edf" in files
        assert "ref0001_0050.edf" in files
        assert "refHST0000.edf" not in files
        assert "refHST0050.edf" not in files
        assert "dark.edf" not in files

        scan = ScanFactory.create_scan_object(scan_path=self.datasets[0])
        self.widget.process(scan)
        for t in range(8):
            qt.QApplication.instance().processEvents()
            time.sleep(0.5)

        files = os.listdir(scan.path)
        self.assertTrue("dark.edf" in files)
        self.assertTrue("darkend0000.edf" not in files)
        self.assertTrue("ref0000_0000.edf" not in files)
        self.assertTrue("ref0000_0050.edf" not in files)
        self.assertTrue("ref0001_0000.edf" not in files)
        self.assertTrue("ref0001_0050.edf" not in files)
        self.assertTrue("refHST0000.edf" in files)
        self.assertTrue("refHST0050.edf" in files)
        self.assertTrue(self.widget._darkRef.has_flat_stored())

        # check behavior for testslicesNemoz62_1_, testslicesNemoz63_1_,
        # testslicesNemoz64_1_.
        for dataset in self.datasets[1:4]:
            files = os.listdir(dataset)
            assert "darkend0000.edf" not in files
            assert "ref0000_0000.edf" not in files
            assert "ref0000_0050.edf" not in files
            assert "ref0001_0000.edf" not in files
            assert "ref0001_0050.edf" not in files
            assert "refHST0000.edf" not in files
            assert "refHST0050.edf" not in files
            assert "dark.edf" not in files
            scan = ScanFactory.create_scan_object(scan_path=dataset)
            self.widget.process(scan)
            for t in range(8):
                qt.QApplication.instance().processEvents()
                time.sleep(0.5)

            files = os.listdir(dataset)
            self.assertTrue("darkend0000.edf" not in files)
            self.assertTrue("ref0000_0000.edf" not in files)
            self.assertTrue("ref0000_0050.edf" not in files)
            self.assertTrue("ref0001_0000.edf" not in files)
            self.assertTrue("ref0001_0050.edf" not in files)
            self.assertTrue("refHST0000.edf" in files)
            self.assertTrue("refHST0050.edf" in files)
            self.assertTrue("dark.edf" in files)

        # check behavior for testslicesNemoz65_1_
        dataset = self.datasets[-1]
        files = os.listdir(dataset)
        assert "darkend0000.edf" not in files
        assert "ref0000_0000.edf" not in files
        assert "ref0000_0050.edf" in files
        assert "ref0001_0000.edf" not in files
        assert "ref0001_0050.edf" in files
        assert "refHST0000.edf" not in files
        assert "refHST0050.edf" not in files
        assert "dark0000.edf" not in files
        scan = ScanFactory.create_scan_object(scan_path=dataset)
        self.widget.process(scan)
        for t in range(8):
            qt.QApplication.instance().processEvents()
            time.sleep(0.5)

        files = os.listdir(dataset)
        self.assertTrue("darkend0000.edf" not in files)
        self.assertTrue("ref0000_0000.edf" not in files)
        self.assertTrue("ref0000_0050.edf" not in files)
        self.assertTrue("ref0001_0000.edf" not in files)
        self.assertTrue("ref0001_0050.edf" not in files)
        self.assertTrue("refHST0000.edf" in files)
        self.assertTrue("refHST0050.edf" in files)
        self.assertTrue("dark.edf" in files)


class TestDarkRefCopyWithEDFAndHDF5(TestCaseQt):
    """Test the DarkRefCopy orange widget behaviour"""

    def setUp(self) -> None:
        TestCaseQt.setUp(self)
        self._folder = tempfile.mkdtemp()

        # define scans to be treated
        hdf5_mock_with_refs = MockHDF5(
            scan_path=os.path.join(self._folder, "h5_with_refs"),
            n_proj=10,
            n_ini_proj=10,
            dim=20,
            create_ini_ref=True,
            create_ini_dark=True,
            create_final_ref=False,
        )
        self.hdf5_acquisition_with_refs = hdf5_mock_with_refs.scan

        hdf5_mock_without_refs = MockHDF5(
            scan_path=os.path.join(self._folder, "h5_without_refs"),
            n_proj=10,
            n_ini_proj=10,
            dim=20,
            create_ini_ref=False,
            create_ini_dark=False,
        )
        self.hdf5_acquisition_without_refs = hdf5_mock_without_refs.scan

        hdf5_mock_without_refs_incoherent_dim = MockHDF5(
            scan_path=os.path.join(self._folder, "h5_without_refs_different_dim"),
            n_proj=10,
            n_ini_proj=10,
            dim=21,
            create_ini_ref=False,
            create_ini_dark=False,
        )
        self.hdf5_acquisition_without_refs_incoherent_dim = (
            hdf5_mock_without_refs_incoherent_dim.scan
        )

        edf_mock_without_ref = MockEDF(
            scan_path=os.path.join(self._folder, "edf_without_refs"), dim=20, n_radio=20
        )
        self.edf_acquisition_without_ref = EDFTomoScan(
            scan=edf_mock_without_ref.scan_path
        )

        # processes set up
        self._recons_params = QReconsParams()
        self.widget = DarkRefAndCopyOW(
            parent=None, reconsparams=self._recons_params.dkrf
        )
        self.widget.setForceSync(True)
        self.widget.show()

    def tearDown(self) -> None:
        time.sleep(0.5)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._folder)
        TestCaseQt.tearDown(self)

    def testCopyInactive(self):
        self.widget.setCopyActive(False)

        self.widget.process(self.hdf5_acquisition_with_refs)
        self.assertTrue(os.path.exists(self.hdf5_acquisition_with_refs.process_file))

        # make sure dark has been processed for the one with ref
        self.assertEqual(
            len(
                DarkRefs.get_flats_frm_process_file(
                    self.hdf5_acquisition_with_refs.process_file
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                DarkRefs.get_darks_frm_process_file(
                    self.hdf5_acquisition_with_refs.process_file
                )
            ),
            1,
        )
        # make sure no dark or flats exists for the hdf5 without refs
        for scan in (
            self.hdf5_acquisition_without_refs_incoherent_dim,
            self.hdf5_acquisition_without_refs,
        ):
            self.widget.process(scan)
            self.assertFalse(os.path.exists(scan.process_file))

        # make sure no dark or flats exists for the edf one
        self.widget.process(self.edf_acquisition_without_ref)

    def testCopyActive(self):
        self.widget.setCopyActive(True)
        self.widget.setModeAuto(True)

        self.widget.process(self.hdf5_acquisition_with_refs)
        self.assertTrue(os.path.exists(self.hdf5_acquisition_with_refs.process_file))
        # 1. make sure dark has been processed for the one with ref
        self.assertEqual(
            len(
                DarkRefs.get_flats_frm_process_file(
                    self.hdf5_acquisition_with_refs.process_file
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                DarkRefs.get_darks_frm_process_file(
                    self.hdf5_acquisition_with_refs.process_file
                )
            ),
            1,
        )
        self.assertTrue(self.widget.hasDarkStored())
        self.assertTrue(self.widget.hasFlatStored())

        # 2. make sure copy has been processed for the the 'compatible hdf5'
        self.widget.process(self.hdf5_acquisition_without_refs)
        self.assertTrue(os.path.exists(self.hdf5_acquisition_without_refs.process_file))
        self.assertEqual(
            len(
                DarkRefs.get_flats_frm_process_file(
                    self.hdf5_acquisition_without_refs.process_file
                )
            ),
            2,
        )
        self.assertEqual(
            len(
                DarkRefs.get_darks_frm_process_file(
                    self.hdf5_acquisition_without_refs.process_file
                )
            ),
            1,
        )

        # 3. make sure copy has been processed for the the 'compatible edf'
        self.widget.process(self.edf_acquisition_without_ref)
        self.assertEqual(
            len(
                DarkRefs.getRefHSTFiles(
                    self.edf_acquisition_without_ref.path, prefix=REFHST_PREFIX
                )
            ),
            2,
        )
        self.assertEqual(
            len(
                DarkRefs.getDarkHSTFiles(
                    self.edf_acquisition_without_ref.path, prefix=DARKHST_PREFIX
                )
            ),
            1,
        )

        # 4. make sure process but no copy made if incompatible size
        self.widget.process(self.hdf5_acquisition_without_refs_incoherent_dim)
        self.assertFalse(
            os.path.exists(
                self.hdf5_acquisition_without_refs_incoherent_dim.process_file
            )
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestEDFDarkRefWidget, TestID16TestCase, TestDarkRefCopyWithEDFAndHDF5):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
