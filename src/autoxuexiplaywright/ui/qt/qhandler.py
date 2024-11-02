"""Log handler that forward log to Qt signal."""

from typing import final as _final
from typing import override as _override
from logging import Handler as _LogHandler
from logging import LogRecord as _LogRecord
from PySide6.QtCore import SignalInstance as _QSignal


@_final
class QHandler(_LogHandler):
    """Log handler that forward log to Qt signal."""

    @_override
    def __init__(self, signal: _QSignal):
        super().__init__()
        self._signal = signal

    @_override
    def emit(self, record: _LogRecord):
        self._signal.emit(self.format(record))
