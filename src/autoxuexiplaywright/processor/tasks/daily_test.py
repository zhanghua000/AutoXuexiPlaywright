"""Operations to finish daily test."""

from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from playwright.async_api import Page as _Page
from autoxuexiplaywright.sdk import Task as _Task
from autoxuexiplaywright.sdk import module_entrance as _module
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.processor.tasks.test import TestTask as _TestTask
from autoxuexiplaywright.processor.tasks.utils import first_task as _first_task


@_module(_Version.parse(_version))
@_final
class DailyTestTask(_TestTask):
    """Operations to finish daily test."""

    _DAILY_TEST_PAGE = "https://pc.xuexi.cn/points/exam-practice.html"
    __requires = None

    @property
    @_override
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @_override
    def author(self) -> str:
        return _APPAUTHOR

    @property
    @_override
    def requires(self) -> list[_Task]:
        if self.__requires is None:
            self.__requires = [_first_task("登录")]
        return self.__requires

    @property
    @_override
    def handles(self) -> list[str]:
        return ["每日答题"]

    @_override
    async def _handle(self, page: _Page, task_name: str) -> bool:
        _ = await page.goto(self._DAILY_TEST_PAGE)
        logger = _get_logger(__name__)
        logger.info(__("Processing daily test..."))
        return await self._test(page)
