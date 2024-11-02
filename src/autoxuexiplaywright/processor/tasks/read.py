"""Basic operations to emulate reading."""

from abc import ABCMeta as _ABCMeta
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from playwright.async_api import Page as _Page
from autoxuexiplaywright.sdk import Task as _Task
from autoxuexiplaywright.sdk import Reader as _Reader
from autoxuexiplaywright.module import iter_module_type as _iter_modules
from autoxuexiplaywright.localize import gettext as __


_logger = _get_logger(__name__)


class ReadTask(_Task, metaclass=_ABCMeta):
    """Basic operations to emulate reading."""

    _MAIN_PAGE = "https://www.xuexi.cn/"
    _READ_TIME_SECS = 60
    _READ_SLEEPS_MIN_SECS = 2.0
    _READ_SLEEPS_MAX_SECS = 5.0
    _NEXT_PAGE = 'div.btn:has-text(">>")'

    @_final
    @_override
    def __init__(self):
        super().__init__()
        self._read_titles: list[str] = []

    @_final
    async def _read(self, page: _Page) -> bool:
        for reader in _iter_modules(_Reader):
            try:
                if await reader.read(
                    page,
                    self._READ_TIME_SECS,
                    self._READ_SLEEPS_MIN_SECS,
                    self._READ_SLEEPS_MAX_SECS,
                ):
                    return True
            except Exception as e:
                _logger.error(__("Failed to read content because %(e)s"), {"e": e})
        return False

    @_final
    async def _go_to_next_page(self, page: _Page) -> bool:
        next_button = page.locator(self._NEXT_PAGE)
        if await next_button.count() == 0:
            return False
        await next_button.click()
        await page.locator(self._LOADING_SELECTOR).wait_for(state="hidden")
        return True
