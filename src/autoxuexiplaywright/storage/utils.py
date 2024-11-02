"""Utils for autoxuexiplaywright.storage package."""

from pathlib import Path as _Path
from platformdirs import PlatformDirs as _PlatformDirs
from collections.abc import Iterator as _Iterator
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


def filter_overlayed_paths(pattern: str) -> _Iterator[_Path]:
    """Filter path matches pattern in overlayed style.

    Args:
        pattern (str): The pattern to filter path.

    Yields:
        Path: The path that matches pattern given.
    """
    pdirs = _PlatformDirs(
        appauthor=_APPAUTHOR,
        appname=_APPNAME,
    )
    recorded: list[_Path] = []
    for data_dir in pdirs.iter_data_paths():
        for path in data_dir.glob(pattern):
            if path not in recorded:
                yield data_dir / path
                recorded.append(path)
