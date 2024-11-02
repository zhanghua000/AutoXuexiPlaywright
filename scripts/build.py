"""Helpers to be used during build processes.

Remarks:
    You should not invoke this script directly.
"""

from shutil import copy2
from logging import INFO
from logging import StreamHandler
from logging import getLogger
from pathlib import Path


_logger = getLogger(__name__)
_logger.setLevel(INFO)
_logger.addHandler(StreamHandler())
for handler in _logger.handlers:
    handler.setLevel(_logger.level)


def copy_pattern(src: Path | str, dst: Path | str, pattern: str):
    """Copy files match pattern from src to dst.

    Args:
        src(Path | str): The source directory.
        dst(Path | str): The target directory.
        pattern(str): The pattern to filter files.
    """
    if not isinstance(src, Path):
        src = Path(src)
    if not isinstance(dst, Path):
        dst = Path(dst)

    for p in src.glob(pattern):
        if p.is_file():
            target = dst / p.relative_to(src)
            _logger.info("Copying %s to %s" % (p, target))
            target.parent.mkdir(parents=True, exist_ok=True)
            copy2(p, target, follow_symlinks=False)


def copy_mo():
    """Copy generated mo files."""
    copy_pattern(
        Path("resources/translations"),
        Path("src/autoxuexiplaywright/resources/translations"),
        "**/*.mo",
    )
