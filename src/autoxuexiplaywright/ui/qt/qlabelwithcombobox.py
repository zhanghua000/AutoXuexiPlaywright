"""Widget contains a label and a combobox."""
# pyright: reportAny=false

from typing import NamedTuple as _NamedTuple
from typing import final as _final
from typing import overload as _overload
from typing import override as _override
from PySide6.QtGui import QIcon as _QIcon
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QComboBox as _QComboBox
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout


class _UserDataWithIcon(_NamedTuple):
    icon: _QIcon
    data: object


@_final
class QLabelWithCombobox(_QWidget):
    """Widget contains a label and a combobox."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._labelWidget = _QLabel(self)
        self._setUpLabelWidget()
        self.layout().addWidget(self._labelWidget)

        self._selectorWidget = _QComboBox(self)
        self._setUpSelectorWidget()
        self.layout().addWidget(self._selectorWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._labelWidget.setObjectName(objectName + "-label")
        self._selectorWidget.setObjectName(objectName + "-selector")

    def _setUpLabelWidget(self):
        pass

    def _setUpSelectorWidget(self):
        pass

    def labelWidget(self) -> _QLabel:
        """The label widget in the widget."""
        return self._labelWidget

    def selectorWidget(self) -> _QComboBox:
        """The combobox widget in the widget."""
        return self._selectorWidget

    @_overload
    def setSelectorWidgetContents(
        self,
        *contents: str,
        **contentsWithData: _UserDataWithIcon,
    ) -> None:
        pass

    @_overload
    def setSelectorWidgetContents(
        self,
        *contents: str,
        **contentsWithData: object,
    ) -> None:
        pass

    def setSelectorWidgetContents(
        self,
        *contents: str,
        **contentsWithData: _UserDataWithIcon | object,
    ):
        """Set content of the combobox.

        Args:
            *contents (str): The content
            **contentsWithData (_UserDataWithIcon | object): The content with icon.
        """
        self._selectorWidget.clear()
        self._selectorWidget.addItems(contents)
        for key, value in contentsWithData.items():
            if isinstance(value, _UserDataWithIcon):
                icon, data = value
                self._selectorWidget.addItem(icon, key, data)
            else:
                self._selectorWidget.addItem(key, value)
