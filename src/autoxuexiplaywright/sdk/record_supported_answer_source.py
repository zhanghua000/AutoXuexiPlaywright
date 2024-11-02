"""Record answer and provide it in the future."""

from abc import ABCMeta as _ABCMeta
from abc import abstractmethod as _abstract
from autoxuexiplaywright.sdk.answer_source import AnswerSource as _AnswerSource


class RecordSupportedAnswerSource(_AnswerSource, metaclass=_ABCMeta):
    """Record answer and provide it in the future."""

    @_abstract
    async def record(self, title: str, answers: list[str]) -> None:
        """Record the answer."""
        raise NotImplementedError
