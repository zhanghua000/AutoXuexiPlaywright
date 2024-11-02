"""Widget contains a label and a checkbox."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QCheckBox as _QCheckBox
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout


@_final
class QLabelWithCheckbox(_QWidget):
    """Widget contains a label and a checkbox."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._labelWidget = _QLabel(self)
        self._setUpLabelWidget()
        self.layout().addWidget(self._labelWidget)

        self._checkerWidget = _QCheckBox(self)
        self._setUpCheckerWidget()
        self.layout().addWidget(self._checkerWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._labelWidget.setObjectName(objectName + "-label")
        self._checkerWidget.setObjectName(objectName + "-checker")

    def _setUpLabelWidget(self):
        pass

    def _setUpCheckerWidget(self):
        pass

    def labelWidget(self) -> _QLabel:
        """The label widget in the widget."""
        return self._labelWidget

    def checkerWidget(self) -> _QCheckBox:
        """The checkbox widget in the widget."""
        return self._checkerWidget
