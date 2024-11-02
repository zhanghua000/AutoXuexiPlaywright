"""Config in typed struct."""

from typing import Literal as _Literal
from dataclasses import field as _data_field
from dataclasses import dataclass as _dataclass
from playwright.async_api import ProxySettings as ProxySettings


type BrowserType = _Literal["firefox", "chromium", "webkit"]
type ChannelType = (
    _Literal[
        "msedge",
        "msedge-beta",
        "msedge-dev",
        "chrome",
        "chrome-beta",
        "chrome-dev",
        "chromium",
        "chromium-beta",
        "chromium-dev",
    ]
    | None
)


@_dataclass
class Config:
    """Runtime config in typed struct."""

    browser_id: BrowserType = "firefox"
    browser_channel: ChannelType = None
    debug: bool = False
    executable_path: str | None = None
    gui: bool = True
    proxy: ProxySettings | None = None
    skipped: list[str] = _data_field(default_factory=list)
