"""Functions to access state content."""

from pathlib import Path as _Path
from platformdirs import user_state_path as _state_path
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


def get_state_path(path: _Path) -> _Path:
    """Get path under state directory."""
    state = _state_path(_APPNAME, _APPAUTHOR)
    if path.is_absolute():
        path = path.relative_to("/")
    return state / path
