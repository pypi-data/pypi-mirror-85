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

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "01/12/2016"

import logging
import os
from collections import OrderedDict
from silx.gui import qt
from tomwer.core.process.control.scanlist import _ScanList
from tomwer.core.utils import logconfig
from tomwer.gui.qfolderdialog import QScanDialog
from nxtomomill import converter as nxtomomill_converter
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanfactory import ScanFactory

logger = logging.getLogger(__name__)


class _DataListDialog(qt.QWidget):
    """A simple list of dataset path.

    .. warning: the widget won't check for scan validity and will only
        emit the path to folders to the next widgets

    :param parent: the parent widget
    """

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        # add list
        self.datalist = self.createDataList()
        self.layout().addWidget(self.datalist)
        # add buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._addButton = qt.QPushButton("Add", parent=self)
        self._buttons.addButton(self._addButton, qt.QDialogButtonBox.ActionRole)
        self._rmButton = qt.QPushButton("Remove", parent=self)
        self._buttons.addButton(self._rmButton, qt.QDialogButtonBox.ActionRole)
        self._rmAllButton = qt.QPushButton("Remove all", parent=self)
        self._buttons.addButton(self._rmAllButton, qt.QDialogButtonBox.ActionRole)

        self._sendButton = qt.QPushButton("Send", parent=self)
        self._buttons.addButton(self._sendButton, qt.QDialogButtonBox.AcceptRole)
        self.layout().addWidget(self._buttons)

        # expose API
        self._sendList = self.datalist._sendList
        self.add = self.datalist.add
        self.remove = self.datalist.remove
        self.setScanIDs = self.datalist.setScanIDs
        self._scheme_title = self.datalist._scheme_title
        self.length = self.datalist.length
        self.selectAll = self.datalist.selectAll
        self.clear = self.datalist.clear

        # connect signal / slot
        self._addButton.clicked.connect(self._callbackAddPath)
        self._rmButton.clicked.connect(self._callbackRemoveFolder)
        self._rmAllButton.clicked.connect(self._callbackRemoveAllFolders)

    def n_scan(self):
        return len(self.datalist.items)

    def _callbackAddPath(self):
        """"""
        raise NotImplementedError("Base class")

    def _callbackRemoveFolder(self):
        """"""
        selectedItems = self.datalist.selectedItems()
        toRemove = []
        if selectedItems is not None and len(selectedItems) > 0:
            for item in selectedItems:
                toRemove.append(item.text())
        for scan in toRemove:
            self.remove(scan)

    def _callbackRemoveAllFolders(self):
        self.datalist.selectAll()
        self._callbackRemoveFolder()

    def createDataList(self):
        raise NotImplementedError("Base class")


class BlissHDF5DataListDialog(_DataListDialog):
    """Dialog used to load .h5 only (used when for nxtomomillOW when we need)
    to do a conversion from bliss.h5 to NXtomo"""

    def __init__(self, parent):
        _DataListDialog.__init__(self, parent)
        self._sendButton.setText("Send all")
        self._sendSelectedButton = qt.QPushButton("Send selected", self)
        self._buttons.addButton(
            self._sendSelectedButton, qt.QDialogButtonBox.AcceptRole
        )

    def createDataList(self):
        return BlissDataList(self)

    def _callbackAddPath(self):
        """"""
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(["HDF5 file *.h5 *.hdf5 *.nx *.nexus"])

        if not dialog.exec_():
            dialog.close()
            return

        filesSelected = dialog.selectedFiles()
        for file_ in filesSelected:
            self.add(file_)


class GenericDataListDialog(_DataListDialog):
    """Dialog used to load EDFScan or HEDF5 scans"""

    def createDataList(self):
        return GenericDataList(self)

    def _callbackAddPath(self):
        """"""
        dialog = QScanDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        files_or_folders = dialog.files_selected()
        for file_or_folder in files_or_folders:
            self.add(file_or_folder)


class _DataList(_ScanList, qt.QTableWidget):
    def __init__(self, parent):
        _ScanList.__init__(self)
        qt.QTableWidget.__init__(self, parent)
        self.setRowCount(0)
        self.setColumnCount(1)
        self.setSortingEnabled(True)
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), "setSectionResizeMode"):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.setAcceptDrops(True)
        self.items = OrderedDict()

    def remove_item(self, item):
        """Remove a given folder"""
        del self.items[item.text()]
        itemIndex = self.row(item)
        self.takeItem(itemIndex, 0)
        _ScanList.remove(self, item.text())
        self.removeRow(item.row())
        self.setRowCount(self.rowCount() - 1)
        self._update()

    def remove(self, scan):
        if scan is not None and scan in self.items:
            item = self.items[scan]
            itemIndex = self.row(item)
            self.takeItem(itemIndex, 0)
            _ScanList.remove(self, scan)
            del self.items[scan]
            self.removeRow(item.row())
            self.setRowCount(self.rowCount() - 1)
            self._update()

    def _update(self):
        list_scan = list(self.items.keys())
        self.clear()
        for scan in list_scan:
            self.add(scan)
        self.sortByColumn(0, self.horizontalHeader().sortIndicatorOrder())

    def add(self, d):
        """add the folder or path"""
        raise NotImplementedError("Base class")

    def _addScanIDItem(self, d):
        if "@" not in d and not os.path.isdir(d):
            warning = (
                "Skipping the observation of %s, directory not existing on the system"
                % d
            )
            logger.info(warning, extra={logconfig.DOC_TITLE: self._scheme_title})
        elif d in self.items:
            logger.debug("The path {} is already in the scan list".format(d))
        else:
            row = self.rowCount()
            self.setRowCount(row + 1)

            _item = qt.QTableWidgetItem()
            _item.setText(d)
            _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            self.setItem(row, 0, _item)

            self.items[d] = _item

    def setScanIDs(self, scanIDs):
        [self._addScanIDItem(item) for item in scanIDs]
        _ScanList.setScanIDs(self, scanIDs)

    def clear(self):
        """Remove all items on the list"""
        self.items = OrderedDict()
        _ScanList.clear(self)
        qt.QTableWidget.clear(self)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(["folder"])
        if hasattr(self.horizontalHeader(), "setSectionResizeMode"):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                self.add(str(url.path()))

    def supportedDropActions(self):
        """Inherited method to redefine supported drop actions."""
        return qt.Qt.CopyAction | qt.Qt.MoveAction

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
            event.setDropAction(qt.Qt.CopyAction)
        else:
            qt.QListWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.setDropAction(qt.Qt.CopyAction)
            event.accept()
        else:
            qt.QListWidget.dragMoveEvent(self, event)


class GenericDataList(_DataList):
    """Data list able to manage directories (EDF/HDF5?) or files (HDF5)"""

    def __init__(self, parent):
        _DataList.__init__(self, parent)
        self.setHorizontalHeaderLabels(["scan"])

    def add(self, path):
        """Add the path folder d in the scan list

        :param d: the path of the directory to add
        :type d: Union[str, TomoBase]
        """
        if isinstance(path, TomwerScanBase):
            scan_obj = _ScanList.add(self, path)
            self._addScanIDItem(str(scan_obj))
        elif os.path.isdir(path):
            scan_obj = _ScanList.add(self, path)
            if scan_obj:
                self._addScanIDItem(str(scan_obj.path))
        else:
            # try to add it as HDF5TomoScan
            try:
                scan_objs = ScanFactory.create_scan_objects(path)
            except Exception as e:
                logger.error(e)
            else:
                if scan_objs is None:
                    return
                for scan in scan_objs:
                    scan_obj = _ScanList.add(self, scan)
                    if scan_obj:
                        self._addScanIDItem(str(scan_obj))


class BlissDataList(_DataList):
    def __init__(self, parent):
        _DataList.__init__(self, parent)
        self.setHorizontalHeaderLabels(["entry@bliss_file.h5"])

    def add(self, path):
        """Add the path folder d in the scan list

        :param d: the path of the directory to add
        :type d: Union[str, TomoBase]
        """
        if "@" in path:
            entry, path = path.split("@")
            possible_entries = [entry]
        else:
            if not BlissScan.is_bliss_file(path):
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Warning)
                types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
                msg.setStandardButtons(types)

                if HDF5TomoScan.is_nexus_nxtomo_file(path):
                    text = (
                        "The input file `{}` seems to contain `NXTomo` entries. "
                        "and no valid `Bliss` valid entry. \n"
                        "This is probably not a Bliss file. Do you still want to "
                        "translate ?".format(path)
                    )
                else:
                    text = (
                        "The input file `{}` does not seems to contain any"
                        "valid `Bliss` entry. \n"
                        "This is probably not a Bliss file. Do you still want to "
                        "translate ?".format(path)
                    )
                msg.setText(text)
                if msg.exec_() != qt.QMessageBox.Ok:
                    return

            try:
                possible_entries = nxtomomill_converter.get_bliss_tomo_entries(
                    path, scan_titles=nxtomomill_converter.DEFAULT_SCAN_TITLES
                )
            except Exception as e:
                logger.error("Faild to find entries for {}".format(path))
                possible_entries = []

        for entry in possible_entries:
            scan = HDF5TomoScan(scan=path, entry=entry)
            scan_obj = _ScanList.add(self, scan)
            if scan_obj:
                self._addScanIDItem(str(scan_obj))


def main():
    app = qt.QApplication([])
    s = GenericDataListDialog()
    s.show()
    app.exec_()


if __name__ == "__main__":
    main()
