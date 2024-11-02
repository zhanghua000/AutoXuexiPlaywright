"""Event triggered when processing is finished."""

from autoxuexiplaywright.event.event import Event as _Event
from autoxuexiplaywright.event.utils import register_event as _event
from autoxuexiplaywright.event.eventid import EventID as _EventID


@_event(_EventID.FINISHED)
class FinishedEvent(_Event[int]):
    """Event triggered when processing is finished.

    Type params:
        int: The seconds used to finish processing.
    """

    pass
