"""Widget to save or discard settings."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from PySide6.QtWidgets import QPushButton as _QPushButton
from autoxuexiplaywright.localize import gettext as __


@_final
class SettingOperationWidget(_QWidget):
    """Widget to save or discard settings."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))
        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

        self._saveButton = _QPushButton(self)
        self._setUpSaveButton()
        self.layout().addWidget(self._saveButton)

        self._cancelButton = _QPushButton(self)
        self._setUpCancelButton()
        self.layout().addWidget(self._cancelButton)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._saveButton.setObjectName(objectName + "-save")
        self._cancelButton.setObjectName(objectName + "-cancel")

    def _setUpSaveButton(self):
        self._saveButton.setText(__("Save"))

    def _setUpCancelButton(self):
        self._cancelButton.setText(__("Cancel"))

    def saveButton(self) -> _QPushButton:
        """The button to save settings."""
        return self._saveButton

    def cancelButton(self) -> _QPushButton:
        """The button to discard settings."""
        return self._cancelButton
