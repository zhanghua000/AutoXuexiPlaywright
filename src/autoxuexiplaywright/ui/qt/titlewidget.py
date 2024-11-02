"""Title bar of the main window."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtGui import Qt as _Qt
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from PySide6.QtWidgets import QApplication as _QApplication
from autoxuexiplaywright.ui.qt.controlwidget import ControlWidget as _ControlWidget


@_final
class TitleWidget(_QWidget):
    """Title bar of the main window."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._scoreText = _QLabel(self)
        self._setUpScoreText()
        self.layout().addWidget(self._scoreText)

        self._titleText = _QLabel(self)
        self._setUpTitleText()
        self.layout().addWidget(self._titleText)

        self._controlWidget = _ControlWidget(self)
        self._setUpControlWidget()
        self.layout().addWidget(self._controlWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._scoreText.setObjectName(objectName + "-score")
        self._titleText.setObjectName(objectName + "-title")
        self._controlWidget.setObjectName(objectName + "-control")

    def _setUpScoreText(self):
        self._scoreText.setAlignment(_Qt.AlignmentFlag.AlignLeft)

    def _setUpTitleText(self):
        self._titleText.setText(_QApplication.applicationDisplayName())
        self._titleText.setAlignment(_Qt.AlignmentFlag.AlignCenter)

    def _setUpControlWidget(self):
        pass

    def scoreText(self) -> _QLabel:
        """Widget displays current score."""
        return self._scoreText

    def titleText(self) -> _QLabel:
        """Title widget."""
        return self._titleText

    def controlWidget(self) -> _ControlWidget:
        """Widget to control the main window."""
        return self._controlWidget
