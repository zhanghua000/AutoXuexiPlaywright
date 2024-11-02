"""Main window."""
# pyright: reportAny=false

from typing import ClassVar as _ClassVar
from typing import final as _final
from typing import override as _override
from logging import getLogger as _getLogger
from pathlib import Path as _Path
from datetime import timedelta as _timedelta
from PySide6.QtGui import QPixmap as _QPixmap
from PySide6.QtGui import QShowEvent as _QShowEvent
from PySide6.QtGui import QCloseEvent as _QCloseEvent
from PySide6.QtCore import Qt as _Qt
from PySide6.QtCore import Slot as _Slot
from PySide6.QtCore import Signal as _QSignal
from PySide6.QtCore import QThread as _QThread
from PySide6.QtCore import QSettings as _QSettings
from PySide6.QtWidgets import QFrame as _QFrame
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QVBoxLayout as _QVBoxLayout
from PySide6.QtWidgets import QApplication as _QApplication
from PySide6.QtWidgets import QSystemTrayIcon as _QSystemTrayIcon
from autoxuexiplaywright.event import Score as _Score
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.storage import get_config_path as _getConfigPath
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.processor import __name__ as _loggerName
from autoxuexiplaywright.ui.qt.job import JobObject as _JobObject
from autoxuexiplaywright.ui.qt.utils import (
    getBundledOrLooseResourceContent as _getBundledOrLooseResourceContent,
)
from autoxuexiplaywright.ui.qt.qhandler import QHandler as _QHandler
from autoxuexiplaywright.ui.qt.titlewidget import TitleWidget as _TitleWidget
from autoxuexiplaywright.ui.qt.settingwindow import SettingWindow as _SettingWindow
from autoxuexiplaywright.ui.qt.operationwidget import (
    OperationWidget as _OperationWidget,
)
from autoxuexiplaywright.ui.qt.logdisplaywidget import (
    LogDisplayWidget as _LogDisplayWidget,
)
from autoxuexiplaywright.ui.qt.qtranslucentbackgroundframelesswidget import (
    QTranslicentBackgroundFramelessWidget as _QTranslicentBackgroundFramelessWidget,
)


@_final
class _MainWindowContentWidget(_QFrame):
    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QVBoxLayout(self))

        self._titleWidget = _TitleWidget(self)
        self._setUpTitleWidget()
        self.layout().addWidget(self._titleWidget)

        self._logDisplayWidget = _LogDisplayWidget(self)
        self._setUpLogDisplayWidget()
        self.layout().addWidget(self._logDisplayWidget)

        self._operationWidget = _OperationWidget(self)
        self._setUpOperationWidget()
        self.layout().addWidget(self._operationWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)
        _ = self.setProperty("main", True)
        self.setObjectName(_QApplication.applicationName())

    def _setUpTitleWidget(self):
        pass

    def _setUpLogDisplayWidget(self):
        pass

    def _setUpOperationWidget(self):
        operationWidget = self._operationWidget
        _ = operationWidget.startButton().clicked.connect(self._startProcessor)
        operationWidget.startButton().setDefault(True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._titleWidget.setObjectName(objectName + "-title")
        self._logDisplayWidget.setObjectName(objectName + "-log")
        self._operationWidget.setObjectName(objectName + "-operations")

    @_Slot(result=None)
    def _startProcessor(self):
        startButton = self._operationWidget.startButton()
        startButton.setEnabled(False)
        startButton.setText(__("Procesing..."))

    def titleWidget(self) -> _TitleWidget:
        """Widget as the title bar."""
        return self._titleWidget

    def logDisplayWidget(self) -> _LogDisplayWidget:
        """Widget to display processor outputs."""
        return self._logDisplayWidget

    def operationWidget(self) -> _OperationWidget:
        """Widget to start processor or edit processor settings."""
        return self._operationWidget


@_final
class MainWindow(_QTranslicentBackgroundFramelessWidget[_MainWindowContentWidget]):
    """Main window."""

    __logForwardSignal: _ClassVar[_QSignal] = _QSignal(str)

    @_override
    def __init__(self, config: _Config, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setWindowFlag(_Qt.WindowType.Window)

        content = _MainWindowContentWidget()
        self.setContentWidget(content)
        self.setPseudoCaptionWidget(content.titleWidget())
        _ = self.__logForwardSignal.connect(
            content.logDisplayWidget().logPlainTextWidget().appendPlainText,
        )
        control = content.titleWidget().controlWidget()
        _ = control.closeButton().clicked.connect(self.close)
        _ = control.minimizeButton().clicked.connect(self.showMinimized)
        _ = control.onTopToggleButton().clicked.connect(
            self.__onOnTopToggleButtonClicked,
        )

        self.__loggerHandler = _QHandler(self.__logForwardSignal)
        self.__setUpLoggerHandler()

        self.__trayIcon = _QSystemTrayIcon(self)
        self.__setUpTrayIcon()

        self.__settingWindow = _SettingWindow(content)
        self.__settingWindow.setProcessorConfig(config)
        _ = (
            content.operationWidget()
            .settingButton()
            .clicked.connect(
                self.__settingWindow.show,
            )
        )
        _ = content.objectNameChanged.connect(self.__onContentObjectNameChanged)
        self.__setUpSettingWindow()

        self.__jobObject = _JobObject(config)
        self.__setUpJobObject()

        self.__jobThread = _QThread(self)
        _ = (
            content.operationWidget()
            .startButton()
            .clicked.connect(
                self.__jobThread.start,
            )
        )
        self.__setUpJobThread()

        userConfigPath = _getConfigPath(
            _Path(_QApplication.applicationDisplayName() + ".ini"),
        )
        self.__uiSettings = _QSettings(
            str(userConfigPath),
            _QSettings.Format.IniFormat,
            self,
        )
        self.__setUpUiSettings()
        self.__onStatusUpdated(__("Ready"))

    @_Slot(result=None)
    def __onOnTopToggleButtonClicked(self):
        self.setWindowFlag(
            _Qt.WindowType.WindowStaysOnTopHint,
            _Qt.WindowType.WindowStaysOnTopHint not in self.windowFlags(),
        )
        self.show()

    def __setUpLoggerHandler(self):
        logger = _getLogger(_loggerName)
        if len(logger.handlers) > 0:
            formatter = logger.handlers[0].formatter
            level = logger.level
        else:
            rootLogger = _getLogger(__name__.split(".")[0])
            formatter = rootLogger.handlers[0].formatter
            level = rootLogger.level
        self.__loggerHandler.setFormatter(formatter)
        self.__loggerHandler.setLevel(level)
        logger.addHandler(self.__loggerHandler)

    @_Slot(_QSystemTrayIcon.ActivationReason, result=None)
    def __onTrayIconActivated(self, reason: _QSystemTrayIcon.ActivationReason):
        match reason:
            case _QSystemTrayIcon.ActivationReason.Trigger:
                self.setHidden(not self.isHidden())
            case _:
                pass

    def __setUpTrayIcon(self):
        self.__trayIcon.setToolTip(_QApplication.applicationDisplayName())
        _ = self.__trayIcon.activated.connect(self.__onTrayIconActivated)
        _ = self.windowIconChanged.connect(self.__trayIcon.setIcon)

    @_Slot(str, result=None)
    def __onContentObjectNameChanged(self, objectName: str):
        content = self.__settingWindow.contentWidget(True)
        content.setObjectName(objectName + "-settings")

    def __setUpSettingWindow(self):
        content = self.contentWidget(True)
        _ = content.objectNameChanged.connect(self.__onContentObjectNameChanged)
        self.__onContentObjectNameChanged(content.objectName())

    @_Slot(int, result=None)
    def __onJobFinished(self, usedSeconds: int):
        notifySeconds = 5

        self.__jobThread.quit()
        self.__trayIcon.showMessage(
            __("Process completed."),
            __("Used time: %(delta)s") % {"delta": _timedelta(seconds=usedSeconds)},
            _QSystemTrayIcon.MessageIcon.Information,
            notifySeconds * 1000,
        )

        content = self.contentWidget(True)
        content.operationWidget().resetStartButton()
        self.__onStatusUpdated(__("Ready"))

    @_Slot(str, result=None)
    def __onStatusUpdated(self, status: str):
        content = self.contentWidget(True)
        content.logDisplayWidget().setToolTip(
            __("Current status: %(status)s") % {"status": status},
        )

    @_Slot(_Score, result=None)
    def __onScoreUpdated(self, score: _Score):
        content = self.contentWidget(True)
        content.titleWidget().scoreText().setText(
            __("Current: %(current)d\nTotal: %(total)d")
            % {"current": score.current, "total": score.total},
        )

    @_Slot(bytes, result=None)
    def __onQrUpdated(self, qrContent: bytes):
        pixmap = _QPixmap()
        content = self.contentWidget(True)
        logDisplayWidget = content.logDisplayWidget()
        if pixmap.loadFromData(qrContent):
            logDisplayWidget.qrDisplayWidget().setPixmap(pixmap)
            logDisplayWidget.setCurrentWidget(logDisplayWidget.qrDisplayWidget())
        else:
            logDisplayWidget.setCurrentWidget(logDisplayWidget.logPlainTextWidget())

    def __setUpJobObject(self):
        _ = self.__jobObject.finished.connect(self.__onJobFinished)
        _ = self.__jobObject.qrUpdated.connect(self.__onQrUpdated)
        _ = self.__jobObject.statusUpdated.connect(self.__onStatusUpdated)
        _ = self.__jobObject.scoreUpdated.connect(self.__onScoreUpdated)

    def __setUpJobThread(self):
        _ = self.__jobThread.started.connect(self.__jobObject.run)
        _ = self.__jobObject.moveToThread(self.__jobThread)

    def __saveSettings(self):
        self.__uiSettings.setValue("UI/x", self.x())
        self.__uiSettings.setValue("UI/y", self.y())
        self.__uiSettings.setValue("UI/width", self.width())
        self.__uiSettings.setValue("UI/height", self.height())
        self.__uiSettings.setValue(
            "UI/ontop",
            _Qt.WindowType.WindowStaysOnTopHint in self.windowFlags(),
        )

    def __setUpUiSettings(self):
        defaultX = 0
        defaultY = 0
        defaultWidth = 1024
        defaultHeight = 768
        x = self.__uiSettings.value("UI/x", defaultX, int)
        y = self.__uiSettings.value("UI/y", defaultY, int)
        width = self.__uiSettings.value("UI/width", defaultWidth, int)
        height = self.__uiSettings.value("UI/height", defaultHeight, int)
        if (
            isinstance(x, int)
            and isinstance(y, int)
            and isinstance(width, int)
            and isinstance(height, int)
        ):
            self.setGeometry(x, y, width, height)
        onTop = self.__uiSettings.value("UI/ontop", False, bool)
        if isinstance(onTop, bool):
            self.setWindowFlag(_Qt.WindowType.WindowStaysOnTopHint, onTop)
        icon = _getBundledOrLooseResourceContent("/icon.png")
        iconPixmap = _QPixmap()
        if icon is not None and iconPixmap.loadFromData(icon):
            self.setWindowIcon(iconPixmap)
        customQssStr = _getBundledOrLooseResourceContent("/ui.qss")
        content = self.contentWidget(True)
        if customQssStr is not None:
            content.setStyleSheet(customQssStr.decode())

    @_override
    def closeEvent(self, event: _QCloseEvent) -> None:
        if self.__jobThread.isRunning():
            self.__jobThread.quit()
        self.__saveSettings()
        self.__trayIcon.hide()
        return super().closeEvent(event)

    @_override
    def showEvent(self, event: _QShowEvent) -> None:
        self.__trayIcon.show()
        return super().showEvent(event)

    def trayIcon(self) -> _QSystemTrayIcon:
        """Tray icon of the window."""
        return self.__trayIcon

    def loggerHandler(self) -> _QHandler:
        """Logger handler to obtain processor output."""
        return self.__loggerHandler
