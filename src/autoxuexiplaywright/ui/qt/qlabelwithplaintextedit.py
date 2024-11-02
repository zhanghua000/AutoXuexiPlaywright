"""Widget contains a label and a plaintextedit."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QVBoxLayout as _QVBoxLayout
from PySide6.QtWidgets import QPlainTextEdit as _QPlainTextEdit


@_final
class QLabelWithPlainTextEdit(_QWidget):
    """Widget contains a label and a plaintextedit."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QVBoxLayout(self))

        self._titleWidget = _QLabel(self)
        self._setUpTitleWidget()
        self.layout().addWidget(self._titleWidget)

        self._textEditWidget = _QPlainTextEdit(self)
        self._setUpTextEditWidget()
        self.layout().addWidget(self._textEditWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._titleWidget.setObjectName(objectName + "-title")
        self._textEditWidget.setObjectName(objectName + "-text")

    def _setUpTitleWidget(self):
        pass

    def _setUpTextEditWidget(self):
        pass

    def titleWidget(self) -> _QLabel:
        """The label widget in the widget."""
        return self._titleWidget

    def textEditWidget(self) -> _QPlainTextEdit:
        """The plaintextedit widget in the widget."""
        return self._textEditWidget
