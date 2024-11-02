"""Objects to process various tasks on website."""

from os import environ as _environ
from re import search as _search
from shutil import rmtree as _rmdir
from logging import getLogger as _get_logger
from pathlib import Path as _Path
from datetime import datetime as _datetime
from collections.abc import AsyncGenerator as _AsyncGenerator
from playwright.async_api import Page as _Page
from playwright.async_api import Locator as _Locator
from playwright.async_api import expect as _expect
from playwright.async_api import async_playwright as _playwright
from autoxuexiplaywright.event import Score as _Score
from autoxuexiplaywright.event import EventID as _EventID
from autoxuexiplaywright.event import FinishedEvent as _FinishedEvent
from autoxuexiplaywright.event import ScoreUpdatedEvent as _ScoreUpdatedEvent
from autoxuexiplaywright.event import find_event_by_id as _find_event
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.storage import get_cache_path as _cache
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.processor.tasks.news import NewsTask as NewsTask
from autoxuexiplaywright.processor.tasks.login import LoginTask as LoginTask
from autoxuexiplaywright.processor.tasks.utils import iter_task as iter_task
from autoxuexiplaywright.processor.tasks.utils import first_task as first_task
from autoxuexiplaywright.processor.tasks.video import VideoTask as VideoTask
from autoxuexiplaywright.processor.tasks.daily_test import (
    DailyTestTask as DailyTestTask,
)
from autoxuexiplaywright.processor.answer_sources.sqlite import (
    SqliteAnswerSource as SqliteAnswerSource,
)
from autoxuexiplaywright.processor.captcha_handlers.drag import (
    DragCaptchaHandler as DragCaptchaHandler,
)
from autoxuexiplaywright.processor.readers.simple_reader import (
    SimpleReader as SimpleReader,
)


_legacy_pki_dir = _Path.home() / ".pki"
_mozilla_dir = _Path.home() / ".mozilla"
_remove_pki = not _legacy_pki_dir.is_dir()
_remove_mozilla = not _mozilla_dir.is_dir()


async def _login(page: _Page):
    login = first_task("登录")
    await login.do(page, "登录")


async def _get_scores(points: _Locator) -> _Score:
    logger = _get_logger(__name__)
    await points.last.wait_for()
    await _expect(points.nth(0)).to_be_visible()
    await _expect(points.nth(1)).to_be_visible()
    try:
        total = int(await points.nth(0).inner_text())
        current = int(await points.nth(1).inner_text())
    except ValueError:
        logger.error(__("Failed to parse score value."))
        total = 0
        current = 0
    return _Score(current, total)


async def _iter_tasks_from_status_page(
    page: _Page,
    skipped: list[str],
) -> _AsyncGenerator[str]:
    status_page_url = "https://pc.xuexi.cn/points/my-points.html"
    points_selector = "span.my-points-points"
    cards_selector = "div.my-points-card"
    card_title_selector = "p.my-points-card-title"
    card_button_selector = "div.big"

    all_finished = False
    while True:
        _ = await page.goto(status_page_url)
        await page.wait_for_load_state()
        points = page.locator(points_selector)
        score_event = _find_event(_EventID.SCORE_UPDATED, _ScoreUpdatedEvent)
        if score_event is not None:
            await score_event.trigger(await _get_scores(points))

        if all_finished:
            break

        cards = page.locator(cards_selector)
        await cards.last.wait_for()
        all_finished = True
        for i in range(await cards.count()):
            card = cards.nth(i)
            task_title = (await card.locator(card_title_selector).inner_text()).strip()
            task_button = card.locator(card_button_selector)
            button_style = await task_button.get_attribute("style") or ""
            match_result = _search(r"cursor:(.+?);", button_style)
            task_finished = (
                match_result is not None and match_result[1].strip() == "not-allowed"
            )
            if not task_finished and (task_title not in skipped):
                all_finished = False
                yield task_title


async def launch_processor(config: _Config):
    """Launch the processor."""
    logger = _get_logger(__name__)
    start_time = _datetime.now()
    logger.info(__("Starting processing..."))

    if config.debug:
        _environ["PWDEBUG"] = "1"

    async with _playwright() as p:
        context = await p[config.browser_id].launch_persistent_context(
            _cache(_Path("browser-data")) / config.browser_id,
            channel=config.browser_channel,
            executable_path=config.executable_path,
            # Mute Chromium
            args=["--mute-audio"],
            proxy=config.proxy,
            # Mute firefox
            firefox_user_prefs={"media.volume_scale": "0.0"},
        )
        try:
            await _login(await context.new_page())
            async for task_title in _iter_tasks_from_status_page(
                await context.new_page(),
                config.skipped,
            ):
                task = first_task(task_title)
                logger.debug(
                    __("Processing %(title)s with %(name)s..."),
                    {"title": task_title, "name": task.name},
                )
                pages_to_remove: list[_Page] = []

                # Simply pass pages_to_remove.append is not acceptable by playwright.
                def on_new_page(page: _Page):
                    pages_to_remove.append(page)  # noqa: B023

                context.on("page", on_new_page)
                await task.do(await context.new_page(), task_title)
                context.remove_listener("page", on_new_page)
                for page in pages_to_remove:
                    if not page.is_closed():
                        await page.close()
        except Exception as e:
            logger.error(__("Failed to finish tasks because %(e)s"), {"e": e})

    if _remove_pki and _legacy_pki_dir.is_dir():
        logger.debug(
            __("Removing temp dir %(path)s outside cache."),
            {"path": _legacy_pki_dir},
        )
        _rmdir(_legacy_pki_dir)
    if _remove_mozilla and _mozilla_dir.is_dir():
        logger.debug(
            __("Removing temp dir %(path)s outside cache."),
            {"path": _mozilla_dir},
        )
        _rmdir(_mozilla_dir)
    logger.info(__("Processing completed."))
    finished_event = _find_event(_EventID.FINISHED, _FinishedEvent)
    if finished_event is not None:
        await finished_event.trigger(
            round((_datetime.now() - start_time).total_seconds()),
        )
