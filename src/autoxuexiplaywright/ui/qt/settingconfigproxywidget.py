"""Widget contains proxy configuration items."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QLineEdit as _QLineEdit
from PySide6.QtWidgets import QVBoxLayout as _QVBoxLayout
from autoxuexiplaywright.ui.qt.qlabelwithlineedit import (
    QLabelWithLineEdit as _QLabelWithLineEdit,
)


@_final
class SettingConfigProxyWidget(_QWidget):
    """Widget contains proxy configuration items."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)
        self.setLayout(_QVBoxLayout(self))

        self._serverWidget = _QLabelWithLineEdit(self)
        self._setUpServerWidget()
        self.layout().addWidget(self._serverWidget)

        self._bypassWidget = _QLabelWithLineEdit(self)
        self._setUpBypassWidget()
        self.layout().addWidget(self._bypassWidget)

        self._usernameWidget = _QLabelWithLineEdit(self)
        self._setUpUsernameWidget()
        self.layout().addWidget(self._usernameWidget)

        self._passwordWidget = _QLabelWithLineEdit(self)
        self._setUpPasswordWidget()
        self.layout().addWidget(self._passwordWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectName)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectName(self, objectName: str):
        self._serverWidget.setObjectName(objectName + "-server")
        self._bypassWidget.setObjectName(objectName + "-bypass")
        self._usernameWidget.setObjectName(objectName + "-username")
        self._passwordWidget.setObjectName(objectName + "-password")

    def _setUpServerWidget(self):
        pass

    def _setUpBypassWidget(self):
        pass

    def _setUpUsernameWidget(self):
        pass

    def _setUpPasswordWidget(self):
        self._passwordWidget.lineEditWidget().setEchoMode(
            _QLineEdit.EchoMode.PasswordEchoOnEdit,
        )

    def serverWidget(self) -> _QLabelWithLineEdit:
        """The widget to config proxy server."""
        return self._serverWidget

    def bypassWidget(self) -> _QLabelWithLineEdit:
        """The widget to config proxy bypass."""
        return self._bypassWidget

    def usernameWidget(self) -> _QLabelWithLineEdit:
        """The widget to config proxy username."""
        return self._usernameWidget

    def passwordWidget(self) -> _QLabelWithLineEdit:
        """The widget to config proxy password."""
        return self._passwordWidget
