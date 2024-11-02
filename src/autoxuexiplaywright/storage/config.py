"""Functions to access config content."""

from pathlib import Path as _Path
from platformdirs import user_config_path as _config_path
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


def get_config_path(path: _Path) -> _Path:
    """Get path under config directory."""
    config = _config_path(_APPNAME, _APPAUTHOR)
    if path.is_absolute():
        path = path.relative_to("/")
    return config / path
