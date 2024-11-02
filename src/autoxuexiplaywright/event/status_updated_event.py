"""Event triggered when a new task is being finished."""

from autoxuexiplaywright.event.event import Event as _Event
from autoxuexiplaywright.event.utils import register_event as _event
from autoxuexiplaywright.event.eventid import EventID as _EventID


@_event(_EventID.STATUS_UPDATED)
class StatusUpdatedEvent(_Event[str]):
    """Event triggered when a new task is being finished.

    Type params:
        str: The task name.
    """

    pass
