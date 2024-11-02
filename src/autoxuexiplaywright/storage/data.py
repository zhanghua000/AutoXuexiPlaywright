"""Functions to access data content."""

from pathlib import Path as _Path
from platformdirs import user_data_path as _data_path
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


def get_data_path(path: _Path) -> _Path:
    """Get path under data directory."""
    data = _data_path(_APPNAME, _APPAUTHOR)
    if path.is_absolute():
        path = path.relative_to("/")
    return data / path
