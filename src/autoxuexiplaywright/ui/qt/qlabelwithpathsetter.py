"""Widget contains a label and a path setter."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from PySide6.QtWidgets import QPushButton as _QPushButton


@_final
class QLabelWithPathSetter(_QWidget):
    """Widget contains a label and a path setter."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._titleWidget = _QLabel(self)
        self._setUpTitleWidget()
        self.layout().addWidget(self._titleWidget)

        self._pathDisplayWidget = _QLabel(self)
        self._setUpPathDisplayWidget()
        self.layout().addWidget(self._pathDisplayWidget)

        self._browseButton = _QPushButton(self)
        self._setUpBrowseButton()
        self.layout().addWidget(self._browseButton)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._titleWidget.setObjectName(objectName + "-title")
        self._pathDisplayWidget.setObjectName(objectName + "-path")
        self._browseButton.setObjectName(objectName + "-browse")

    def _setUpTitleWidget(self):
        pass

    def _setUpPathDisplayWidget(self):
        pass

    def _setUpBrowseButton(self):
        pass

    def titleWidget(self) -> _QLabel:
        """The label widget in the widget."""
        return self._titleWidget

    def pathDisplayWidget(self) -> _QLabel:
        """The path displayer widget of the path setter in the widget."""
        return self._pathDisplayWidget

    def browseButton(self) -> _QPushButton:
        """The browser button of the path setter in the widget."""
        return self._browseButton
