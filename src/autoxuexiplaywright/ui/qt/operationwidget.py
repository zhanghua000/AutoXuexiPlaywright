"""Widget to start processor or edit setting."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from PySide6.QtWidgets import QPushButton as _QPushButton
from autoxuexiplaywright.localize import gettext as __


@_final
class OperationWidget(_QWidget):
    """Widget to start processor or edit setting."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._startButton = _QPushButton(__("Start"), self)
        self._setUpStartButton()
        self.layout().addWidget(self._startButton)

        self._settingButton = _QPushButton(__("Settings"), self)
        self._setUpSettingButton()
        self.layout().addWidget(self._settingButton)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._startButton.setObjectName(objectName + "-start")
        self._settingButton.setObjectName(objectName + "-setting")

    def _setUpStartButton(self):
        pass

    def _setUpSettingButton(self):
        pass

    def startButton(self) -> _QPushButton:
        """The button to start processor."""
        return self._startButton

    def settingButton(self) -> _QPushButton:
        """The button to open settings dialog."""
        return self._settingButton

    def resetStartButton(self):
        """Reset start button to default."""
        self._startButton.setEnabled(True)
        self._startButton.setText(__("Start"))
