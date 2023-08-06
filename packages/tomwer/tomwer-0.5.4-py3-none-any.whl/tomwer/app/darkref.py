#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

from silx.gui import qt
from tomwer.gui import icons
from tomwer.gui.reconstruction.darkref.darkrefwidget import DarkRefWidget
from tomwer.synctools.ftseries import _QDKRFRP
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.hdf5scan import HDF5TomoScan

logging.basicConfig()
_logger = logging.getLogger(__name__)


class _DarkRefWidgetRunnable(DarkRefWidget):
    sigScanReady = qt.Signal(str)

    def __init__(self, scan, parent=None):
        self.__scan = scan
        self.__darkref_rp = _QDKRFRP()
        DarkRefWidget.__init__(self, parent=parent,
                               reconsparams=self.__darkref_rp)
        buttonExec = qt.QPushButton('execute', parent=self)
        buttonExec.setAutoDefault(True)
        # needed to be used as an application to return end only when the
        # processing thread is needed
        self._forceSync = True
        self.layout().addWidget(buttonExec)
        buttonExec.pressed.connect(self._process)
        self.setWindowIcon(icons.getQIcon('tomwer'))

    def _process(self):
        self.process(scan=self.__scan)


def getinputinfo():
    return "tomwer darkref [scanDir]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'scan_path',
        help='Data file to show (h5 file, edf files, spec files)')
    parser.add_argument('--entry',
        help='an entry can be specify in case of hdf5 the master file',
        default=None,
    )
    parser.add_argument(
        '--debug',
        dest="debug",
        action="store_true",
        default=False,
        help='Set logging system in debug mode')

    options = parser.parse_args(argv[1:])

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    if options.entry is None:
        scan = ScanFactory.create_scan_object(options.scan_path)
    else:
        scan = HDF5TomoScan(scan=options.scan_path, entry=options.entry)


    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catched
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()

    widget = _DarkRefWidgetRunnable(scan)
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
