"""Event triggered when score is updated."""

from typing import NamedTuple as _NamedTuple
from autoxuexiplaywright.event.event import Event as _Event
from autoxuexiplaywright.event.utils import register_event as _event
from autoxuexiplaywright.event.eventid import EventID as _EventID


class Score(_NamedTuple):
    """The score information."""

    current: int
    total: int


@_event(_EventID.SCORE_UPDATED)
class ScoreUpdatedEvent(_Event[Score]):
    """Event triggered when score is updated.

    Type params:
        Score: The updated score.
    """

    pass
