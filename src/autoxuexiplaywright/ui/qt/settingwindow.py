"""Widget to allow editing processor settings."""
# pyright: reportAny=false

import json
from typing import final as _final
from typing import override as _override
from dataclasses import asdict as _asDict
from PySide6.QtGui import Qt as _Qt
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QFrame as _QFrame
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QFileDialog as _QFileDialog
from PySide6.QtWidgets import QVBoxLayout as _QVBoxLayout
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.ui.qt.settingconfigwidget import (
    SettingConfigWidget as _SettingConfigWidget,
)
from autoxuexiplaywright.ui.qt.settingoperationwidget import (
    SettingOperationWidget as _SettingOperationWidget,
)
from autoxuexiplaywright.ui.qt.qtranslucentbackgroundframelesswidget import (
    QTranslicentBackgroundFramelessWidget as _QTranslicentBackgroundFramelessWidget,
)


@_final
class _SettingWindowContentWidget(_QFrame):
    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QVBoxLayout(self))

        self._titleWidget = _QLabel(__("Settings"), self)
        self._setUpTitleWidget()
        self.layout().addWidget(self._titleWidget)

        self._configWidget = _SettingConfigWidget(self)
        self._setUpConfigWidget()
        self.layout().addWidget(self._configWidget)

        self._operationWidget = _SettingOperationWidget(self)
        self._setUpOperationWidget()
        self.layout().addWidget(self._operationWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)
        _ = self.setProperty("main", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._titleWidget.setObjectName(objectName + "-title")
        self._configWidget.setObjectName(objectName + "-config")
        self._operationWidget.setObjectName(objectName + "-operations")

    def _setUpTitleWidget(self):
        self._titleWidget.setAlignment(_Qt.AlignmentFlag.AlignCenter)

    def _setUpConfigWidget(self):
        self._configWidget.applyProcessorConfig(_Config())

    def _setUpOperationWidget(self):
        _ = self._operationWidget.saveButton().clicked.connect(
            self._onSaveButtonClicked,
        )
        self._operationWidget.saveButton().setDefault(True)

    @_Slot(result=None)
    def _onSaveButtonClicked(self):
        configDict = _asDict(self._configWidget.toConfig())
        configJson = json.dumps(configDict, ensure_ascii=False, indent=4)
        _QFileDialog.saveFileContent(configJson.encode(), "config.json", self)

    def operationWidget(self) -> _SettingOperationWidget:
        """Widget to save or discard settings."""
        return self._operationWidget

    def configWidget(self) -> _SettingConfigWidget:
        """Widget contains settings contents."""
        return self._configWidget

    def titleWidget(self) -> _QLabel:
        """Title widget."""
        return self._titleWidget


@_final
class SettingWindow(
    _QTranslicentBackgroundFramelessWidget[_SettingWindowContentWidget],
):
    """Widget to allow editing processor settings."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setWindowFlag(_Qt.WindowType.Dialog)
        self.setWindowModality(_Qt.WindowModality.WindowModal)

        content = _SettingWindowContentWidget(parent)
        self.setContentWidget(content)
        self.setPseudoCaptionWidget(content.titleWidget())
        _ = content.operationWidget().cancelButton().clicked.connect(self.close)

    def setProcessorConfig(self, config: _Config):
        """Apply processor config and update widget."""
        content = self.contentWidget(True)
        content.configWidget().applyProcessorConfig(config)
