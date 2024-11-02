"""Widget contains complex items in settings."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QHBoxLayout as _QHBoxLayout
from autoxuexiplaywright.ui.qt.qlabelwithplaintextedit import (
    QLabelWithPlainTextEdit as _QLabelWithPlainTextEdit,
)
from autoxuexiplaywright.ui.qt.settingconfigproxywidget import (
    SettingConfigProxyWidget as _SettingConfigProxyWidget,
)


@_final
class SettingConfigComplexItemContainer(_QWidget):
    """Widget that contains complex items in settings."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QHBoxLayout(self))

        self._proxySetter = _SettingConfigProxyWidget(self)
        self._setUpProxySetter()
        self.layout().addWidget(self._proxySetter)

        self._skippedItemsSetter = _QLabelWithPlainTextEdit(self)
        self._setUpSkippedItemsSelector()
        self.layout().addWidget(self._skippedItemsSetter)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._proxySetter.setObjectName(objectName + "-proxy")
        self._skippedItemsSetter.setObjectName(objectName + "-skipped")

    def _setUpProxySetter(self):
        pass

    def _setUpSkippedItemsSelector(self):
        pass

    def proxySetter(self) -> _SettingConfigProxyWidget:
        """The proxy setter widget in the widget."""
        return self._proxySetter

    def skippedItemsSetter(self) -> _QLabelWithPlainTextEdit:
        """The skipped items setter widget in the widget."""
        return self._skippedItemsSetter
