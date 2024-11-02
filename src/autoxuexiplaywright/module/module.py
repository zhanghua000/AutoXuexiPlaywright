"""Class definition for a module."""

from abc import ABC as _ABC
from abc import abstractmethod as _abstract
from typing import final as _final
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR


class Module(_ABC):
    """A loadable module."""

    def __init__(self):
        """Initialize the module without any argument."""
        self.initialized: bool = True

    @property
    def priority(self) -> int:
        """The priority of module.

        Lower value means used first.

        Defaults to 0.
        """
        return 0

    @property
    @_abstract
    def name(self) -> str:
        """The name of module."""

    @property
    @_abstract
    def author(self) -> str:
        """The author of module."""

    @property
    @_final
    def official(self) -> bool:
        """If the module is from AutoXuexiPlaywright organization."""
        return self.author == _APPAUTHOR
