"""Functions to launch GUI."""

from pathlib import Path as _Path
from platform import system as _system
from PySide6.QtCore import QLocale as _QLocale
from PySide6.QtCore import QResource as _QResource
from PySide6.QtCore import QTranslator as _QTranslator
from PySide6.QtCore import QLibraryInfo as _QLibraryInfo
from PySide6.QtWidgets import QApplication as _QApplication
from autoxuexiplaywright import APPID as _APPID
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _appversion
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.storage import (
    get_overlayed_resource_content as _getLooseResourceContent,
)
from autoxuexiplaywright.ui.qt.window import MainWindow as _MainWindow


match _system():
    case "Windows":
        from sys import getwindowsversion as _windows_version

        if _windows_version()[:2] >= (6, 1):
            import ctypes

            # Win7 and later needs this to show icon correctly.
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(_APPID)
    case "Linux":
        # Linux Wayland needs this to show icon correctly
        _QApplication.setDesktopFileName(_APPID)
    case _:
        pass

_QApplication.setApplicationName(_APPNAME.lower())
_QApplication.setApplicationDisplayName(_APPNAME)
_QApplication.setApplicationVersion(_appversion)
_QApplication.setOrganizationName(_APPAUTHOR)
_QApplication.setOrganizationDomain("github.com")
# Supports Light/Dark mode without operating QStyleHints manually.
_ = _QApplication.setStyle("fusion")


def launch(config: _Config):
    """Launch the GUI."""
    app = _QApplication()
    path = _QLibraryInfo.location(_QLibraryInfo.LibraryPath.TranslationsPath)
    translator = _QTranslator(app)
    if translator.load(_QLocale.system(), "qtbase", "_", path):
        _ = app.installTranslator(translator)

    resourceContent = _getLooseResourceContent(_Path("ui.rcc"))
    if resourceContent is not None:
        _ = _QResource.registerResourceData(resourceContent)

    main = _MainWindow(config)
    main.show()

    _ = app.exec()
