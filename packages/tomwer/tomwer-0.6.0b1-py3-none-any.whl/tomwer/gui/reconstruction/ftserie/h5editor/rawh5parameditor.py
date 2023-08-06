# /*##########################################################################
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
__date__ = "08/02/2017"


from collections import OrderedDict

from silx.gui import qt

from tomwer.core.octaveh5editor import OctaveH5Editor
from tomwer.core.process.reconstruction.ftseries.params import fastsetupdefineglobals
import logging

logger = logging.getLogger(__name__)


class RawH5ParamEditor(OctaveH5Editor, qt.QTabWidget):
    """
    This is a simple interface allowing the user to change values of an
    h5 file

    :param QObject parent: the parent widget
    :param str h5File: the path of h5File to load on the editor
    :param float readedOctaveVersion: the version which as write the h5File
    """

    sigH5StructSettedToDefault = qt.Signal(list)
    """signal emitted when some structure are not found in the h5 file and
    set to default
    """

    def __init__(self, parent, h5File):
        OctaveH5Editor.__init__(self)
        qt.QWidget.__init__(self, parent)

        self.__initPalette = self.palette()
        self._loadH5File(h5File)
        self.defaultStructs = fastsetupdefineglobals.getAllDefaultStructures()

    def _loadH5File(self, h5File):
        """Main function to build the GUI"""
        self.h5File = h5File
        if self.h5File is None:
            return

        reader = fastsetupdefineglobals.FastSetupAll()
        reader.readAll(self.h5File, 3.8)
        self.loadReconsParams(reader.structures)

    def getInitialPalette(self):
        return self.__initPalette

    def getPalette(self, highlight=False):
        p = self.getInitialPalette()
        brush = qt.QBrush()
        p.setBrush(self.backgroundRole(), brush)

        if highlight:
            p.setColor(qt.QPalette.WindowText, qt.Qt.red)
            p.setColor(qt.QPalette.Text, qt.Qt.red)
            p.setColor(qt.QPalette.Window, qt.Qt.red)
        else:
            p.setColor(qt.QPalette.WindowText, qt.Qt.black)
            p.setColor(qt.QPalette.Text, qt.Qt.black)
            p.setColor(qt.QPalette.Window, qt.Qt.black)
        return p

    def getDefaultStruct(self, structID):
        if structID not in self.defaultStructs:
            raise ValueError("%s structure has no default value" % structID)
        else:
            return self.defaultStructs[structID]

    # implementation of OctaveH5Editor function
    def getStructs(self):
        """Return a list of all the structures with their values"""
        res = {}
        for struct in self.structs:
            fields = {}
            for field in self.structs[struct]:
                self.structs[struct][field].text()
                fields[field] = self.structs[struct][field].text()
            res[struct] = fields

        return res

    def loadReconsParams(self, structures):
        structureIDs = ["FT", "PYHSTEXE", "FTAXIS", "PAGANIN", "BEAMGEO", "DKRF"]
        self.structs = {}
        settedToDefault = []
        for structID in structureIDs:
            highlightStruct = False
            highlightedVariables = []
            try:
                struct = structures[structID]
                FSDG = fastsetupdefineglobals.FastSetupAll()
                for variable in FSDG.defaultValues[structID]:
                    if variable not in struct:
                        highlightedVariables.append(variable)
                        struct[variable] = FSDG.defaultValues[structID][variable]
                        logger.info("%s variable in %s is missing" % (variable, struct))
            except (ValueError):
                highlightStruct = True
                struct = self.getDefaultStruct(structID)
                settedToDefault.append(structID)
                warn = (
                    "%s structure not found in the given file, values setted to default"
                    % struct
                )
                logger.info(warn)

            self.structs[structID] = self._addStruct(
                OrderedDict(sorted(struct.items(), key=lambda t: t[0])),
                structID,
                highlight=highlightStruct,
                highlightedVariables=highlightedVariables,
            )

        # for now we are only displaying a message box if some structure are
        # setted to default values. Should this evolve ? If so a signal is emitted
        # and can be used back
        if len(settedToDefault) > 0:
            self.sigH5StructSettedToDefault.emit(settedToDefault)
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            text = (
                "The following structure haven't been found in %s, you might check if setted values are corrects"
                % self.h5File
            )
            for s in settedToDefault:
                text += "\n    - %s" % s
            msg.setText(text)
            msg.exec_()

    def _addStruct(self, struct, structID, highlight, highlightedVariables):
        """Add the given structure to the GUI"""
        newStruct = qt.QWidget()
        newStruct.setLayout(qt.QGridLayout())
        newStruct.setPalette(self.getPalette(highlight))
        self.addTab(newStruct, structID)
        dicoFieldToQLE = {}
        for i, field in enumerate(struct):
            dicoFieldToQLE[field] = self._addField(
                field, struct[field], newStruct, i, field in highlightedVariables
            )

        return OrderedDict(sorted(dicoFieldToQLE.items(), key=lambda t: t[0]))

    def _addField(self, field, value, parent, index, highlighted=False):
        """Add the field to the widget

        :param str field: the ID of the new field to defined
        :param value: the value of the field
        :param parent: the Qt parent
        :param index: the index of the field
        :return: the line edit for the field
        """
        titleItem = qt.QLabel(field)
        titleItem.setPalette(self.getPalette(highlighted))
        parent.layout().addWidget(titleItem, index, 0)
        lineEdit = qt.QLineEdit(parent=parent, text=str(value))
        parent.layout().addWidget(lineEdit, index, 1)
        return lineEdit
