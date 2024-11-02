"""Functions to access cache content."""

from pathlib import Path as _Path
from platformdirs import user_cache_path as _cache_path
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


def get_cache_path(path: _Path) -> _Path:
    """Get path under cache directory."""
    cache = _cache_path(_APPNAME, _APPAUTHOR)
    if path.is_absolute():
        path = path.relative_to("/")
    return cache / path
