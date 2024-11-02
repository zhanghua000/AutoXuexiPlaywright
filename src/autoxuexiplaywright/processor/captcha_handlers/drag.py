"""Handle drag captcha."""

from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from playwright.async_api import Locator as _Locator
from autoxuexiplaywright.sdk import CaptchaHandler as _CaptchaHandler
from autoxuexiplaywright.sdk import module_entrance as _module


@_module(_Version.parse(_version))
@_final
class DragCaptchaHandler(_CaptchaHandler):
    """Handle drag captcha."""

    @property
    @_override
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @_override
    def author(self) -> str:
        return _APPAUTHOR

    @_override
    async def solve(self, locator: _Locator) -> bool:
        # TODO
        return False
