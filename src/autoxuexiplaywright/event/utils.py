"""Utils for autoxuexiplaywright.event package."""

from typing import Any as _Any
from typing import Callable as _Callable
from typing import overload as _overload
from autoxuexiplaywright.event.event import Event as _Event
from autoxuexiplaywright.event.eventid import EventID as _EventID


_events: dict[_EventID, _Event[_Any]] = {}


def register_event[T](
    event_id: _EventID,
) -> _Callable[[type[_Event[T]]], type[_Event[T]]]:
    """Register the event.

    Example:
        ```python
        @register_event(EventID.UNKNOWN)
        class MyEvent(Event[int]):
            pass
        ```
    """

    def wrapper(event_type: type[_Event[T]]) -> type[_Event[T]]:
        if event_id not in _events:
            _events[event_id] = event_type(event_id)
        return event_type

    return wrapper


@_overload
def find_event_by_id(event_id: _EventID) -> _Event[_Any]:
    pass


@_overload
def find_event_by_id[T](
    event_id: _EventID,
    event_type: type[_Event[T]],
) -> _Event[T] | None:
    pass


def find_event_by_id[T](
    event_id: _EventID,
    event_type: type[_Event[T]] | None = None,
) -> _Event[T] | _Event[_Any] | None:
    """Find the event by ID and type given.

    Arguments:
        event_id (EventID): The ID of the event.
        event_type: (type[Event[T]] | None): The type of the event, defaults to None.

    Returns:
        Event[T] | None: The event if found and event_type is set. None if not found.
        Event[Any] | None: The event if found but no event_type is set.
        None if not found.
    """
    event = _events.get(event_id)
    if event_type is None:
        return event
    if isinstance(event, event_type):
        return event
    return None
