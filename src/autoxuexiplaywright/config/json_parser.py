"""Parse config in json format."""

import json
from semver import Version as _SemVer
from typing import override as _override
from pathlib import Path as _Path
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _appversion
from autoxuexiplaywright.sdk import ConfigParser as _ConfigParser
from autoxuexiplaywright.sdk import ConfigJsonType as _ConfigJsonType
from autoxuexiplaywright.sdk import module_entrance as _module


@_module(_SemVer.parse(_appversion))
class JsonConfigParser(_ConfigParser):
    """Parser to parse config in json format."""

    @property
    @_override
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @_override
    def author(self) -> str:
        return _APPAUTHOR

    @_override
    def is_support(self, path: _Path) -> bool:
        return path.name.endswith(".json")

    @_override
    def get_config(self, path: _Path) -> _ConfigJsonType:
        return json.loads(path.read_text())  # pyright: ignore[reportAny]
