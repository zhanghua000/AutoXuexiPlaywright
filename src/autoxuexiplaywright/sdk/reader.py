"""Operations to emulate reading on page."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from typing import final as _final
from playwright.async_api import Page as _Page
from autoxuexiplaywright.module import Module as _Module


class Reader(_Module, metaclass=_ABCMeta):
    """Operations to emulate reading on page."""

    _PAGE_PARAGRAPHS = "div.render-detail-content>p,div.videoSet-article-summary>p"

    _VIDEO_PLAYER = "div.gr-video-player"
    _VIDEO_SUBTITLE = "div.videoSet-article-sub-title"
    _PLAY_BTN = "div.prism-play-btn"
    _REPLAY_BTN = "span.replay-btn"

    @_abstract
    async def read(
        self,
        page: _Page,
        read_seconds: int,
        min_sleep_seconds: float,
        max_sleep_seconds: float,
    ) -> bool:
        """Emulate reading page.

        Args:
            page(Page): The page to operate.
            read_seconds(int): How many seconds to read.
            min_sleep_seconds(float): The minimal seconds to sleep.
            max_sleep_seconds(float): The maximal seconds to sleep.

        Returns:
            bool: If read successfully.
        """
        raise NotImplementedError

    @_final
    async def play_video(self, page: _Page):
        """Play the video on the page."""
        player = page.locator(self._VIDEO_PLAYER)
        if await player.count() > 0:
            await player.wait_for()
            play = player.locator(self._PLAY_BTN)
            replay = player.locator(self._REPLAY_BTN)
            if await replay.count() == 0:
                await player.hover()
                if "playing" not in (await play.get_attribute("class") or ""):
                    await play.click()
