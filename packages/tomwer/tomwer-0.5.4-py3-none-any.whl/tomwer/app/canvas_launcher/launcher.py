import os
import sys

from silx.gui import qt
from Orange.canvas import config, __main__ as main
from Orange.misc import environ
from .splash import splash_screen, getIcon
import tomwer.version
from tomwer.gui import icons
from tomwer.core.log.logger import _formatter_message, _ColoredFormatter
from tomwer.web.config import grayport_port, grayport_host
import logging
try:
    import graypy

    has_graypy = True
except:
    has_graypy = False

_logger = logging.getLogger(__name__)


def version():
    return tomwer.version.version


class TomwerConfig(config.Config):
    ApplicationName = "tomwer"
    ApplicationVersion = version()

    @staticmethod
    def splash_screen():
        return splash_screen()

    @staticmethod
    def core_packages():
        return super(TomwerConfig, TomwerConfig).core_packages() + [
            "tomwer-add-on",
        ]

    @staticmethod
    def application_icon():
        return getIcon()


class TomwerSplashScreen(qt.QSplashScreen):
    def __init__(self, parent=None, pixmap=None, textRect=None,
                 textFormat=qt.Qt.PlainText, **kwargs):
        super(TomwerSplashScreen, self).__init__(pixmap=icons.getQPixmap('tomwer'))

    def showMessage(self, message, alignment=qt.Qt.AlignLeft, color=qt.Qt.black):
        version = 'tomwer version {}'.format(tomwer.version.version)
        super().showMessage(version, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.white)


class Launcher:
    """Proxy to orange-canvas"""
    def launch(self, argv):
        config.Config = TomwerConfig
        self.fix_application_dirs()
        self.replace_splash_screen()
        self.main(argv)

    def fix_application_dirs(self):
        def data_dir(versioned=True):
            """
            Return the platform dependent Orange data directory.

            This is ``data_dir_base()``/Orange/__VERSION__/ directory if versioned is
            `True` and ``data_dir_base()``/Orange/ otherwise.
            """
            base = environ.data_dir_base()
            if versioned:
                return os.path.join(base, "tomwer", version())
            else:
                return os.path.join(base, "tomwer")

        environ.data_dir = data_dir

        def cache_dir(*args):
            """
            Return the platform dependent Orange cache directory.
            """
            if sys.platform == "darwin":
                base = os.path.expanduser("~/Library/Caches")
            elif sys.platform == "win32":
                base = os.getenv("APPDATA", os.path.expanduser("~/AppData/Local"))
            elif os.name == "posix":
                base = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            else:
                base = os.path.expanduser("~/.cache")

            base = os.path.join(base, "tomwer", version())
            if sys.platform == "win32":
                # On Windows cache and data dir are the same.
                # Microsoft suggest using a Cache subdirectory
                return os.path.join(base, "Cache")
            else:
                return base

        environ.cache_dir = cache_dir

    def replace_splash_screen(self):
        main.SplashScreen = TomwerSplashScreen

    def add_graypy_handler(self, my_logger):

        if os.environ.get("ORANGE_WEB_LOG", "True") == "True":
            if hasattr(graypy, "GELFHandler"):
                constructor = graypy.GELFHandler
            elif hasattr(graypy, "GELFUDPHandler"):
                constructor = graypy.GELFUDPHandler
            else:
                _logger.warning("Fail to find the correct constructor from graypy")
                return

            try:
                self.graylogHandler = constructor(grayport_host, grayport_port)
            except:
                _logger.warning(
                    "Fail to create GELFHandler. Won't report log message"
                )
            else:
                my_logger.addHandler(self.graylogHandler)
                _logger.debug("- add graypy handler")
        else:
            info = "No log will be send to graylog."
            info += "ORANGE_WEB_LOG variable is setted to False"
            _logger.debug(info)

    def main(self, argv):
        from Orange.canvas.__main__ import main

        for logger_name in ("fabio", "tomoscan", "nxtomomill", "tomwer",
                            "nxtomomill.converter"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.WARNING)

        logger = logging.getLogger("nxtomomill.converter")
        logger.setLevel(logging.ERROR)

        # update tomwer logger
        FORMAT = (
            "%(asctime)s [%(levelname)-18s] %(message)s [$BOLD%(name)-20s$RESET]"
            "($BOLD%(filename)s$RESET:%(lineno)d)"
        )
        self.color_format = _formatter_message(
            FORMAT,
            use_color=os.environ.get("ORANGE_COLOR_STDOUT_LOG", "False") == "True",
        )

        color_formatter = _ColoredFormatter(self.color_format)

        tomwer_logger = logging.getLogger("tomwer")

        if has_graypy:
            self.add_graypy_handler(tomwer_logger)
        else:
            logger.info("graypy not install. No log will be send to graylog")

        main(argv)
