"""Widget contains a label and a lineedit."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QLineEdit as _QLineEdit
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout


@_final
class QLabelWithLineEdit(_QWidget):
    """Widget contains a label and a lineedit."""

    @_override
    def __init__(self, parent: _QWidget | None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._titleWidget = _QLabel(self)
        self._setUpTitleWidget()
        self.layout().addWidget(self._titleWidget)

        self._lineEditWidget = _QLineEdit(self)
        self._setUpLineEditWidget()
        self.layout().addWidget(self._lineEditWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._titleWidget.setObjectName(objectName + "-title")
        self._lineEditWidget.setObjectName(objectName + "-line-edit")

    def _setUpTitleWidget(self):
        pass

    def _setUpLineEditWidget(self):
        pass

    def titleWidget(self) -> _QLabel:
        """The label widget in the widget."""
        return self._titleWidget

    def lineEditWidget(self) -> _QLineEdit:
        """The lineedit widget in the widget."""
        return self._lineEditWidget
