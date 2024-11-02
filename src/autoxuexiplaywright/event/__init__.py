"""Events to be triggered during processing."""

from autoxuexiplaywright.event.event import Callback as Callback
from autoxuexiplaywright.event.event import SyncCallback as SyncCallback
from autoxuexiplaywright.event.event import AsyncCallback as AsyncCallback
from autoxuexiplaywright.event.utils import find_event_by_id as find_event_by_id
from autoxuexiplaywright.event.eventid import EventID as EventID
from autoxuexiplaywright.event.finished_event import FinishedEvent as FinishedEvent
from autoxuexiplaywright.event.qr_updated_event import QrUpdatedEvent as QrUpdatedEvent
from autoxuexiplaywright.event.score_updated_event import Score as Score
from autoxuexiplaywright.event.score_updated_event import (
    ScoreUpdatedEvent as ScoreUpdatedEvent,
)
from autoxuexiplaywright.event.status_updated_event import (
    StatusUpdatedEvent as StatusUpdatedEvent,
)
