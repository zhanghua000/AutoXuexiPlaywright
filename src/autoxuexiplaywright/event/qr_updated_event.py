"""Event triggered when QR content is updated."""

from autoxuexiplaywright.event.event import Event as _Event
from autoxuexiplaywright.event.utils import register_event as _event
from autoxuexiplaywright.event.eventid import EventID as _EventID


@_event(_EventID.QR_UPDATED)
class QrUpdatedEvent(_Event[bytes]):
    """Event triggered when QR content is updated.

    Type params:
        bytes: The content of QR code.
    """

    pass
