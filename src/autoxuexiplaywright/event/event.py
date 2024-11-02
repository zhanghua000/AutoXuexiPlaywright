"""Basic Event class."""

import logging
from typing import Any as _Any
from typing import Callable as _Callable
from typing import TypeGuard as _TypeGuard
from typing import final as _final
from typing import overload as _overload
from asyncio import Task as _Task
from asyncio import TaskGroup as _TaskGroup
from asyncio import to_thread as _to_thread
from inspect import iscoroutinefunction as _is_async_callback
from collections.abc import Coroutine as _Coroutine
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.event.eventid import EventID as _EventID


type SyncCallback[T] = _Callable[[T], None]
type AsyncCallback[T] = _Callable[[T], _Coroutine[_Any, _Any, None]]
type Callback[T] = AsyncCallback[T] | SyncCallback[T]


def _is_sync_callback[T](callback: Callback[T]) -> _TypeGuard[SyncCallback[T]]:
    return not _is_async_callback(callback)


class Event[T]:
    """Basic generic event class."""

    @_final
    def __init__(self, event_id: _EventID):
        """Initialize Event[T] instance with event id given."""
        self.__callbacks: list[Callback[T]] = []
        self.__event_id = event_id

    @_final
    @property
    def event_id(self) -> _EventID:
        """The id of the event."""
        return self.__event_id

    @_overload
    def add_callback(self, callback: SyncCallback[T]) -> bool:
        pass

    @_overload
    def add_callback(self, callback: AsyncCallback[T]) -> bool:
        pass

    @_final
    def add_callback(self, callback: Callback[T]) -> bool:
        """Register callback to be called when the event is triggered."""
        if callback not in self.__callbacks:
            self.__callbacks.append(callback)
            return True
        return False

    @_final
    async def trigger(self, arg: T):
        """Trigger the event."""
        logger = logging.getLogger(__name__)
        tasks: list[_Task[None]] = []
        async with _TaskGroup() as tg:
            for callback in self.__callbacks:
                try:
                    if _is_async_callback(callback):
                        coro = callback(arg)
                    elif _is_sync_callback(callback):
                        coro = _to_thread(callback, arg)
                    else:
                        # Should never be reached here.
                        coro = None
                except Exception as e:
                    logger.error(
                        __("Failed to invoke callback because %(e)s"),
                        {"e": e},
                    )
                else:
                    if coro is not None:
                        task = tg.create_task(coro)
                        tasks.append(task)
