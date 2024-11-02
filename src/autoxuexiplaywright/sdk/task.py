"""Handling tasks on page."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from enum import Enum as _Enum
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from playwright.async_api import Page as _Page
from autoxuexiplaywright.event import EventID as _EventID
from autoxuexiplaywright.event import StatusUpdatedEvent as _StatusUpdatedEvent
from autoxuexiplaywright.event import find_event_by_id as _find_event
from autoxuexiplaywright.module import Module as _Module
from autoxuexiplaywright.localize import gettext as __


_logger = _get_logger(__name__)


class _TaskStatus(_Enum):
    UNKNOWN = 0
    READY = 1
    SUCCESS = 2
    FAILED = 3
    SKIPPED = 4


class Task(_Module, metaclass=_ABCMeta):
    """Handling tasks on page."""

    _RETRY_TIMES = 3
    _CHECK_ELEMENT_TIMEOUT_SECS = 300
    _LOADING_SELECTOR = "div.ant-spin-spinning"

    @_override
    def __init__(self):
        super().__init__()
        self.__status = _TaskStatus.UNKNOWN

    @property
    @_final
    def status(self) -> _TaskStatus:
        """The status of the task."""
        return self.__status

    @property
    @_abstract
    def requires(self) -> "list[Task]":
        """Other task(s) required by the task."""
        return []

    @property
    @_abstract
    def handles(self) -> list[str]:
        """What task names can be handled by this task."""
        return []

    @_final
    async def __pre_handle(self, page: _Page, task_name: str) -> bool:
        requires_not_fiinished = any(
            task.__status != _TaskStatus.SUCCESS for task in self.requires
        )
        if task_name not in self.handles or requires_not_fiinished:
            return False
        page.set_default_timeout(self._CHECK_ELEMENT_TIMEOUT_SECS * 1000)

        event = _find_event(_EventID.STATUS_UPDATED, _StatusUpdatedEvent)
        if event is not None:
            await event.trigger(task_name)
        self.__status = _TaskStatus.READY
        return True

    @_abstract
    async def _handle(self, page: _Page, task_name: str) -> bool:
        raise NotImplementedError

    @_final
    async def __post_handle(self, page: _Page):
        if not page.is_closed():
            await page.close()
        if self.__status == _TaskStatus.READY:
            self.__status = _TaskStatus.SUCCESS

    @_final
    async def do(self, page: _Page, task_name: str):
        """Do the task on page.

        Args:
            page (Page): The page to operate.
            task_name (str): The name of the task.
        """
        if not await self.__pre_handle(page, task_name):
            _logger.debug(__("__pre_handle() returns False."))
            self.__status = _TaskStatus.FAILED
            return
        try:
            if not await self._handle(page, task_name):
                _logger.debug(__("_handle() returns False."))
                self.__status = _TaskStatus.FAILED
                return
        except Exception as e:
            _logger.error(__("Failed to handle task because %(e)s"), {"e": e})
            self.__status = _TaskStatus.FAILED
            return
        await self.__post_handle(page)
