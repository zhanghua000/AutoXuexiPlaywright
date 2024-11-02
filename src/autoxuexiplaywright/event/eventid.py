"""Event ID."""

from enum import Enum as _Enum


class EventID(_Enum):
    """The IDs of the events."""

    FINISHED = 1
    STATUS_UPDATED = 2
    QR_UPDATED = 3
    SCORE_UPDATED = 4
