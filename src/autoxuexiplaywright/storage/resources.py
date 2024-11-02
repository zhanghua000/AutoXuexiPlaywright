"""Functions to access resource content."""

from pathlib import Path as _Path
from platformdirs import PlatformDirs as _PlatformDirs
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __name__ as _resource_name
from importlib.resources import files as _resource_files
from importlib.resources import as_file as _resource_as_file


def get_overlayed_resource_path(path: _Path) -> _Path | None:
    """Get resource path in overlay style.

    Args:
        path(Path):: The relative path to resource.

    Returns:
        Path | None: The path to the resource, None if not found.

    Remarks:
        It means the resource is not in the filesystem directly if path is not exist.
    """
    resource_prefix = "resources"
    pdirs = _PlatformDirs(_APPAUTHOR, _APPNAME)
    if path.is_absolute():
        path = path.relative_to("/")
    for data_dir in pdirs.iter_data_paths():
        data = data_dir / resource_prefix / path
        if data.exists():
            return data

    resource = _resource_files(_resource_name).joinpath(str(resource_prefix / path))
    if resource.is_dir() or resource.is_file():
        with _resource_as_file(resource) as p:
            return p

    return None


def get_overlayed_resource_content(path: _Path) -> bytes | None:
    """Get resource content in overlay style.

    Args:
        path(Path): The relative path to resource file.

    Returns:
        bytes | None: The content of file, None if path is not a file.

    Remarks:
        Please ensure path is relative, or we will convert in force.
    """
    resource = get_overlayed_resource_path(path)
    return resource.read_bytes() if resource else None


def ensure_overlayed_resource_content(path: _Path) -> bytes:
    """Ensure resource content in overlay style.

    Remarks:
        This basically equals to get_overlayed_resource_content.
        But will raise a ValueError if resource is not exist.

    Raises:
        ValueError: If resource is not found.
    """
    content = get_overlayed_resource_content(path)
    if content is None:
        raise ValueError("Path {} is not a file.".format(path))
    return content
