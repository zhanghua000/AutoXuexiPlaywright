"""Random scroll on page to emulate reading."""

from time import time as _time
from random import randint as _randint
from random import uniform as _uniform
from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from playwright.async_api import Page as _Page
from playwright.async_api import Locator as _Locator
from playwright.async_api import TimeoutError as _TimeoutError
from autoxuexiplaywright.sdk import Reader as _Reader
from autoxuexiplaywright.sdk import module_entrance as _module
from autoxuexiplaywright.localize import gettext as __


_logger = _get_logger(__name__)


@_module(_Version.parse(_version))
@_final
class SimpleReader(_Reader):
    """Random scroll on page to emulate reading."""

    @property
    @_override
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @_override
    def author(self) -> str:
        return _APPAUTHOR

    @_override
    async def read(
        self,
        page: _Page,
        read_seconds: int,
        min_sleep_seconds: float,
        max_sleep_seconds: float,
    ) -> bool:
        first_read = True
        page.set_default_timeout(read_seconds * 1000)
        start = _time()
        while (_time() - start) < read_seconds:
            await page.wait_for_timeout(
                _uniform(
                    min_sleep_seconds,
                    max_sleep_seconds,
                )
                * 1000,
            )
            try:
                await self.play_video(page)
                video_subtitle = page.locator(self._VIDEO_SUBTITLE)
                page_paragraphs = page.locator(self._PAGE_PARAGRAPHS)
                await self.__scroll_elements(
                    video_subtitle.or_(page_paragraphs),
                    first_read,
                    min_sleep_seconds,
                    max_sleep_seconds,
                )
                first_read = False
            except _TimeoutError:
                pass
            except Exception as e:
                _logger.error(
                    __("Failed to read because %(e)s"),
                    {"e": e},
                )
                return False
        return True

    async def __scroll_elements(
        self,
        elements: _Locator,
        order: bool,
        min_sleep_seconds: float,
        max_sleep_seconds: float,
    ):
        count = await elements.count()
        if count > 0:
            for i in range(count):
                await elements.page.wait_for_timeout(
                    _uniform(
                        min_sleep_seconds,
                        max_sleep_seconds,
                    )
                    * 1000,
                )
                index = i if order else _randint(0, count - 1)
                await elements.nth(index).scroll_into_view_if_needed()
