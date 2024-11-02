"""Widget to display processor log."""
# pyright: reportAny=false

from typing import final as _final
from typing import override as _override
from PySide6.QtCore import Qt as _Qt
from PySide6.QtCore import Slot as _Slot
from PySide6.QtWidgets import QLabel as _QLabel
from PySide6.QtWidgets import QWidget as _QWidget
from PySide6.QtWidgets import QPlainTextEdit as _QPlainTextEdit
from PySide6.QtWidgets import QStackedWidget as _QStackedWidget


@_final
class LogDisplayWidget(_QStackedWidget):
    """Widget to display processor log."""

    @_override
    def __init__(self, parent: _QWidget | None = None):
        super().__init__(parent)

        self.__logPlainTextWidget = _QPlainTextEdit(self)
        self.__setUpLogPlainTextWidget()
        self.__logPlainTextWidgetIndex = self.addWidget(self.__logPlainTextWidget)

        self.__qrDisplayWidget = _QLabel(self)
        self.__setUpQrDisplayWidget()
        self.__qrDisplayWidgetIndex = self.addWidget(self.__qrDisplayWidget)

        _ = self.objectNameChanged.connect(self._refreshObjectNames)
        _ = self.setProperty("container", True)

    @_Slot(str, result=None)
    def _refreshObjectNames(self, objectName: str):
        self.__logPlainTextWidget.setObjectName(objectName + "-text")
        self.__qrDisplayWidget.setObjectName(objectName + "-qr")

    def __setUpLogPlainTextWidget(self):
        self.__logPlainTextWidget.setReadOnly(True)

    def __setUpQrDisplayWidget(self):
        self.__qrDisplayWidget.setAlignment(_Qt.AlignmentFlag.AlignCenter)

    def logPlainTextWidget(self) -> _QPlainTextEdit:
        """The widget contains log output."""
        return self.__logPlainTextWidget

    def qrDisplayWidget(self) -> _QLabel:
        """The widget contains qr image."""
        return self.__qrDisplayWidget
