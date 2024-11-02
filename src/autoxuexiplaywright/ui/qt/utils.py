"""Utils for autoxuexiplaywright.ui.qt package."""

from pathlib import Path as _Path
from PySide6.QtCore import QFile as _QFile
from autoxuexiplaywright.storage import (
    get_overlayed_resource_content as _getLooseResourceContent,
)


def getBundledOrLooseResourceContent(
    absoluteFileName: str,
) -> bytes | None:
    """Get resource in loose resources or qt resource bundle.

    Args:
        absoluteFileName (str): The absolute path to the resource.

    Returns:
        bytes | None: The content of the resource, None if not found.
    """
    loosePrefix = "ui"
    if not absoluteFileName.startswith("/"):
        absoluteFileName = "/" + absoluteFileName
    looseResource = _getLooseResourceContent(_Path(loosePrefix + absoluteFileName))
    if looseResource is not None:
        return looseResource

    bundledResource = _QFile(":" + absoluteFileName)
    if bundledResource.open(_QFile.OpenModeFlag.ReadOnly):
        data = bundledResource.readAll().data()
        if isinstance(data, bytes):
            return data

    return None
