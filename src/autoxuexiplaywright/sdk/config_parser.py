"""Parse config file at path."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from pathlib import Path as _Path
from autoxuexiplaywright.module import Module as _Module


type ConfigJsonType = dict[str, ConfigJsonType | int | str | None]


class ConfigParser(_Module, metaclass=_ABCMeta):
    """Parse config file at path."""

    @_abstract
    def is_support(self, path: _Path) -> bool:
        """If path is supported by the parser."""
        raise NotImplementedError

    @_abstract
    def get_config(self, path: _Path) -> ConfigJsonType:
        """Parse config in path."""
        raise NotImplementedError
