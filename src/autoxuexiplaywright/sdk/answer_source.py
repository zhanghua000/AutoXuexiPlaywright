"""Get answer by question title."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from collections.abc import AsyncIterator as _AsyncIterator
from autoxuexiplaywright.module import Module as _Module


class AnswerSource(_Module, metaclass=_ABCMeta):
    """Get answer by question title."""

    @_abstract
    def get_answer(self, title: str) -> _AsyncIterator[str]:
        """Get the answers from question title."""
        raise NotImplementedError
