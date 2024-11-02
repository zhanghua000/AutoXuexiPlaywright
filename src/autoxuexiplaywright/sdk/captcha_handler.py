"""Solve captcha element on page."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from playwright.async_api import Locator as _Locator
from autoxuexiplaywright.module import Module as _Module


class CaptchaHandler(_Module, metaclass=_ABCMeta):
    """Solve captcha element on page."""

    @_abstract
    async def solve(self, locator: _Locator) -> bool:
        """Solve the captcha element.

        Args:
            locator(Locator): The locator to captcha element.

        Returns:
            bool: If support handling and solve successfully.
        """
        raise NotImplementedError
