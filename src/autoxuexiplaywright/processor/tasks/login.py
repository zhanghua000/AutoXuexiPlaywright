"""Operations to get qr and request login if needed."""

from base64 import b64decode as _base64_decode
from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from playwright.async_api import Page as _Page
from playwright.async_api import Locator as _Locator
from playwright.async_api import TimeoutError as _TimeoutError
from playwright.async_api import expect as _expect
from autoxuexiplaywright.sdk import Task as _Task
from autoxuexiplaywright.sdk import module_entrance as _module
from autoxuexiplaywright.event import EventID as _EventID
from autoxuexiplaywright.event import QrUpdatedEvent as _QrUpdatedEvent
from autoxuexiplaywright.event import find_event_by_id as _get_event
from autoxuexiplaywright.localize import gettext as __


_logger = _get_logger(__name__)


@_module(_Version.parse(_version))
@_final
class LoginTask(_Task):
    """Operations to get qr and request login if needed."""

    _LOGIN_PAGE = "https://pc.xuexi.cn/points/login.html"
    _LOGIN_CHECK_SELECTOR = "div.point-manage"
    _QGLOGIN_SELECTOR = "div#qglogin"
    _LOGIN_IFRAME_SELECTOR = "iframe"
    _LOGIN_IFRAME_IMAGE_SELECTOR = "div#app img"
    _LOGIN_QR_REFRESH_SELECTOR = "div#app div.login_qrcode_refresh"
    _LOGIN_QR_REFRESH_CLICKABLE_SELECTOR = "span"
    _QR_REFRESH_SECS = 300

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
        return []

    @property
    @_override
    def handles(self) -> list[str]:
        return ["登录"]

    @_override
    async def _handle(self, page: _Page, task_name: str) -> bool:
        _ = await page.goto(self._LOGIN_PAGE)
        await page.wait_for_load_state()
        await page.bring_to_front()

        login_check = page.locator(self._LOGIN_CHECK_SELECTOR).first
        if await login_check.is_visible():
            _logger.info(__("Login with cookie successfully."))
            return True

        _logger.info(__("Trying to login with QR code."))
        qglogin = page.locator(self._QGLOGIN_SELECTOR).first
        await _expect(qglogin).to_be_visible()
        frame = qglogin.frame_locator(self._LOGIN_IFRAME_SELECTOR).first
        image = frame.locator(self._LOGIN_IFRAME_IMAGE_SELECTOR).first
        refresh = frame.locator(self._LOGIN_QR_REFRESH_SELECTOR).first
        refresh_clickable = refresh.locator(
            self._LOGIN_QR_REFRESH_CLICKABLE_SELECTOR,
        ).first

        for failed_times in range(self._RETRY_TIMES):
            if await refresh.is_visible():
                await refresh_clickable.click()
            await image.wait_for()
            content = await self._get_qr_bytes(image)
            _logger.info(__("Require scanning QR code with mobile app."))
            event = _get_event(_EventID.QR_UPDATED, _QrUpdatedEvent)
            if event is not None:
                await event.trigger(content)
            try:
                await login_check.wait_for(timeout=self._QR_REFRESH_SECS * 1000)
            except _TimeoutError as e:
                if failed_times >= self._RETRY_TIMES - 1:
                    raise e
            else:
                # Send an invalid QR content to close it.
                if event is not None:
                    await event.trigger(bytes())
                return True

        return False

    async def _get_qr_bytes(self, locator: _Locator) -> bytes:
        src = await locator.get_attribute("src") or ","
        src_type, src_data = src.split(",")
        if src_type.endswith("base64"):
            return _base64_decode(src_data)
        raise NotImplementedError("Unknown src_type {}".format(src_type))
