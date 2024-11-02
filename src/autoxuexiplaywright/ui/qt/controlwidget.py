"""Widget to control window."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtGui import Qt as _Qt
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from PySide6.QtWidgets import QPushButton as _QPushButton
from autoxuexiplaywright.localize import gettext as __


@_final
class ControlWidget(_QWidget):
    """Widget to control window."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))
        self.layout().setAlignment(_Qt.AlignmentFlag.AlignRight)

        self._onTopToggleButton = _QPushButton(self)
        self._setUpOnTopCheck()
        self.layout().addWidget(self._onTopToggleButton)

        self._minimizeButton = _QPushButton(self)
        self._setUpMinimizeButton()
        self.layout().addWidget(self._minimizeButton)

        self._closeButton = _QPushButton(self)
        self._setUpCloseButton()
        self.layout().addWidget(self._closeButton)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._closeButton.setObjectName(objectName + "-close")
        self._minimizeButton.setObjectName(objectName + "-minimize")
        self._onTopToggleButton.setObjectName(objectName + "-ontop")

    def _setUpCloseButton(self):
        self._closeButton.setToolTip(__("Close"))
        _ = self._closeButton.setProperty("control-buttons", True)

    def _setUpMinimizeButton(self):
        self._minimizeButton.setToolTip(__("Show minimized"))
        _ = self._minimizeButton.setProperty("control-buttons", True)

    def _setUpOnTopCheck(self):
        self._onTopToggleButton.setToolTip(__("Toggle staying on top"))
        _ = self._onTopToggleButton.setProperty("control-buttons", True)

    def closeButton(self) -> _QPushButton:
        """The close button of the widget."""
        return self._closeButton

    def minimizeButton(self) -> _QPushButton:
        """The minimize buton of the widget."""
        return self._minimizeButton

    def onTopToggleButton(self) -> _QPushButton:
        """The ontop-toggle button of widget."""
        return self._onTopToggleButton
