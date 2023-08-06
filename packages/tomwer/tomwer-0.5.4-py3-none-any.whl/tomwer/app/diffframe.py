#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
import argparse
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.gui.visualization.diffviewer import DiffFrameViewer
import signal

logging.basicConfig()
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer nabu [scan_path]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    import os

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path", help="Data file to show (h5 file, edf files, spec files)"
    )
    parser.add_argument(
        "--entry", default=None, help="An entry should be specify for hdf5 files"
    )
    options = parser.parse_args(argv[1:])

    app = qt.QApplication.instance() or qt.QApplication([])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    if options.entry is None:
        scan = ScanFactory.create_scan_object(options.scan_path)
    else:
        scan = HDF5TomoScan(scan=options.scan_path, entry=options.entry)
    if scan is None:
        raise ValueError(
            "Given scan path is not recognized as a path" "containing a scan"
        )
    widget = DiffFrameViewer(parent=None)
    widget.setScan(scan)
    # for the application we run for the reconstruction to be finished
    # to give back hand to the user
    widget.setWindowTitle("Frame diff")
    widget.setWindowIcon(icons.getQIcon("tomwer"))
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
