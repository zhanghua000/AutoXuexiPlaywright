"""Job that run in QThread."""
# pyright: reportAny=false

from typing import final as _final


try:
    from uvloop import run as _runAsync
except ImportError:
    from asyncio import run as _runAsync
from PySide6.QtCore import Slot as _Slot
from PySide6.QtCore import Signal as _Signal
from PySide6.QtCore import QObject as _QObject
from autoxuexiplaywright.event import Score as _Score
from autoxuexiplaywright.event import EventID as _EventID
from autoxuexiplaywright.event import FinishedEvent as _FinishedEvent
from autoxuexiplaywright.event import QrUpdatedEvent as _QrUpdatedEvent
from autoxuexiplaywright.event import ScoreUpdatedEvent as _ScoreUpdatedEvent
from autoxuexiplaywright.event import StatusUpdatedEvent as _StatusUpdatedEvent
from autoxuexiplaywright.event import find_event_by_id as _findEventById
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.processor import launch_processor as _launchProcessor


@_final
class JobObject(_QObject):
    """Job that run in QThread."""

    finished = _Signal(int)
    qrUpdated = _Signal(bytes)
    statusUpdated = _Signal(str)
    scoreUpdated = _Signal(_Score)

    def __init__(self, config: _Config):
        """Initialize JobObject with parameters given.

        Args:
            config (Config): The runtime config of processor.
        """
        super().__init__()
        self._config = config

        finishedEvent = _findEventById(_EventID.FINISHED, _FinishedEvent)
        if finishedEvent is not None:
            _ = finishedEvent.add_callback(self.finished.emit)

        qrUpdatedEvent = _findEventById(_EventID.QR_UPDATED, _QrUpdatedEvent)
        if qrUpdatedEvent is not None:
            _ = qrUpdatedEvent.add_callback(self.qrUpdated.emit)

        statusUpdatedEvent = _findEventById(
            _EventID.STATUS_UPDATED,
            _StatusUpdatedEvent,
        )
        if statusUpdatedEvent is not None:
            _ = statusUpdatedEvent.add_callback(self.statusUpdated.emit)

        scoreUpdatedEvent = _findEventById(_EventID.SCORE_UPDATED, _ScoreUpdatedEvent)
        if scoreUpdatedEvent is not None:
            _ = scoreUpdatedEvent.add_callback(self.scoreUpdated.emit)

    @_Slot(result=None)
    def run(self):
        """Launch the processor.

        Remarks:
            This should be invoked in a QThread.
        """
        _runAsync(_launchProcessor(self._config))
