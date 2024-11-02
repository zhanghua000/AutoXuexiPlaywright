"""Operations to emulate reading news."""

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
from autoxuexiplaywright.processor.tasks.utils import clean_string as _clean


_logger = _get_logger(__name__)


@_module(_Version.parse(_version))
@_final
class NewsTask(_ReadTask):
    """Operations to emulate reading news."""

    _NEWS_TITLE_SPAN = 'section[data-data-id="zhaiyao-title"] span.moreUrl'
    _NEWS_LIST = 'section[data-data-id="textListGrid"] div.grid-cell'
    _NEWS_TITLE_TEXT = "div.text-wrap>span.text"

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
        return ["我要选读文章"]

    @_override
    async def _handle(self, page: _Page, task_name: str) -> bool:
        _ = await page.goto(self._MAIN_PAGE)
        await page.wait_for_load_state()

        title_span = page.locator(self._NEWS_TITLE_SPAN).first
        await title_span.wait_for()
        await _expect(title_span).to_be_visible()

        async with page.context.expect_page() as e:
            await title_span.click()
        new_page = await e.value

        news_list = new_page.locator(self._NEWS_LIST)
        found_news = False
        while not found_news:
            await news_list.last.wait_for()
            await _expect(news_list.last).to_be_attached()
            for i in range(await news_list.count()):
                news = news_list.nth(i)
                title_element = news.locator(self._NEWS_TITLE_TEXT)
                title = _clean(await title_element.inner_text())
                if title not in self._read_titles:
                    found_news = True
                    _logger.info(__("Processing news %(title)s"), {"title": title})
                    async with new_page.context.expect_page() as e:
                        await title_element.click()
                    news_page = await e.value
                    if await self._read(news_page):
                        self._read_titles.append(title)
                    await news_page.close()
                    break
            if found_news:
                return True
            _logger.warning(
                __("No unread news found on this page, trying next page..."),
            )
            if not await self._go_to_next_page(new_page):
                _logger.error(__("No news can be read."))
                break
        await new_page.close()
        return found_news
