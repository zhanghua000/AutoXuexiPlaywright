"""Operations to emulate watching video."""

from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from playwright.async_api import Page as _Page
from playwright.async_api import expect as _expect
from autoxuexiplaywright.sdk import Task as _Task
from autoxuexiplaywright.sdk import module_entrance as _module
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.processor.tasks.read import ReadTask as _ReadTask
from autoxuexiplaywright.processor.tasks.utils import first_task as _first_task
from autoxuexiplaywright.processor.tasks.utils import clean_string as _clean_string


_logger = _get_logger(__name__)


@_module(_Version.parse(_version))
@_final
class VideoTask(_ReadTask):
    """Operations to emulate watching video."""

    _VIDEO_ENTRANCE = 'div[data-data-id="tv-station-header"]>div.right>span.moreText'
    _VIDEO_LIBRARY = "div.more-wrap p.text"
    _VIDEO_TEXT_WRAPPER = "div.textWrapper"

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
        return ["视听学习", "视听学习时长", "我要视听学习"]

    @_override
    async def _handle(self, page: _Page, task_name: str) -> bool:
        _ = await page.goto(self._MAIN_PAGE)
        await page.wait_for_load_state()

        async with page.context.expect_page() as e:
            await page.locator(self._VIDEO_ENTRANCE).click()
        entrance_page = await e.value

        async with entrance_page.context.expect_page() as e:
            await entrance_page.locator(self._VIDEO_LIBRARY).click()
        library_page = await e.value

        text_wrappers = library_page.locator(self._VIDEO_TEXT_WRAPPER)

        found_video = False
        while not found_video:
            await text_wrappers.last.wait_for()
            await _expect(text_wrappers.last).to_be_attached()
            for i in range(await text_wrappers.count()):
                text_wrapper = text_wrappers.nth(i)
                text = _clean_string(await text_wrapper.inner_text())
                if text not in self._read_titles:
                    found_video = True
                    _logger.info(__("Processing video %(title)s"), {"title": text})
                    async with library_page.context.expect_page() as e:
                        await text_wrapper.click()
                    video_page = await e.value
                    if await self._read(video_page):
                        self._read_titles.append(text)
                    await video_page.close()
                    break
            if found_video:
                return True
            _logger.warning(
                __("No unread video on this page, trying next page..."),
            )
            if not await self._go_to_next_page(library_page):
                _logger.error(__("No video can be read."))
                break
        await library_page.close()
        await entrance_page.close()
        return found_video
