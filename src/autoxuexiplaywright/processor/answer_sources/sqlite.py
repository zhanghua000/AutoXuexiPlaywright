"""Get answer from sqlite database."""

# pyright: reportAny=false

from base64 import b64decode as _base64_decode
from semver import Version as _Version
from typing import final as _final
from typing import override as _override
from logging import getLogger as _get_logger
from pathlib import Path as _Path
from sqlite3 import connect as _sqlite3_connect
from sqlite3 import threadsafety as _threadsafety
from collections.abc import AsyncIterator as _AsyncIterator
from autoxuexiplaywright import APPAUTHOR as _APPAUTHOR
from autoxuexiplaywright import __version__ as _version
from autoxuexiplaywright.sdk import RecordSupportedAnswerSource as _AnswerSource
from autoxuexiplaywright.sdk import module_entrance as _module
from autoxuexiplaywright.storage import get_data_path as _data_path
from autoxuexiplaywright.localize import gettext as __


@_module(_Version.parse(_version))
@_final
class SqliteAnswerSource(_AnswerSource):
    """Get answer from sqlite database."""

    _DB_PATH = _data_path(_Path("data.db"))
    _ANSWER_CONNECTOR = "#"
    _THREAD_SAFETY_SERIALIZED = 3

    @_override
    def __init__(self):
        super().__init__()
        self._CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS SqliteAnswerSource (
                'ID'         INTEGER PRIMARY KEY  AUTOINCREMENT,
                'QUESTION'   TEXT                 NOT NULL,
                'ANSWER'     TEXT                 NOT NULL
            );
        """

        self._GET_ANSWER = """
            SELECT ANSWER FROM SqliteAnswerSource WHERE QUESTION = ?;
        """

        self._RECORD_ANSWER = """
            INSERT INTO SqliteAnswerSource (QUESTION, ANSWER) VALUES (?, ?);
        """

        self._LEGACY_TABLE_COUNT = """
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='answer';
        """

        self._LEGACY_TABLE_CONTENT = """
            SELECT QUESTION, ANSWER FROM answer;
        """

        self._LEGACY_TABLE_DROP = """
            DROP TABLE answer;
        """

        self.__conn = _sqlite3_connect(
            self._DB_PATH,
            check_same_thread=_threadsafety != self._THREAD_SAFETY_SERIALIZED,
        )
        _ = self.__conn.execute(self._CREATE_TABLE)
        self.__conn.commit()
        self.__migration()

    @property
    @_override
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @_override
    def author(self) -> str:
        return _APPAUTHOR

    @_override
    async def get_answer(self, title: str) -> _AsyncIterator[str]:
        logger = _get_logger(__name__)
        logger.debug(__("Querying answer for %(title)s..."), {"title": title})
        answer_raw = self.__conn.execute(
            self._GET_ANSWER,
            [title],
        ).fetchone()
        logger.debug(__("Got raw answer %(raw)s in database."), {"raw": answer_raw})
        if isinstance(answer_raw, str):
            for answer in answer_raw.split(self._ANSWER_CONNECTOR):
                yield answer

    @_override
    async def record(self, title: str, answers: list[str]):
        if len(answers) > 0:
            _ = self.__conn.execute(
                self._RECORD_ANSWER,
                [title, self._ANSWER_CONNECTOR.join(answers)],
            )
            self.__conn.commit()

    def __del__(self):
        """Triggered before instance is destoryed."""
        self.__conn.commit()
        self.__conn.close()

    def __migration(self):
        if self.__conn.execute(self._LEGACY_TABLE_COUNT).fetchone()[0] == 1:
            logger = _get_logger(__name__)
            logger.info(__("Migrating from legacy database..."))
            try:
                for q, a in self.__conn.execute(self._LEGACY_TABLE_CONTENT).fetchall():
                    decoded_q = _base64_decode(q).decode()
                    decoded_a = _base64_decode(a).decode()
                    _ = self.__conn.execute(
                        self._RECORD_ANSWER,
                        [decoded_q, decoded_a],
                    )

            except Exception as e:
                logger.error(
                    __("Failed to migrate from legacy database because %(e)s."),
                    {"e": e},
                )
                self.__conn.rollback()
            else:
                logger.info(
                    __(
                        "Migration completed. We will remove 'answer' table in %(path)s.",  # noqa: E501
                    ),
                    {"path": self._DB_PATH},
                )
                _ = self.__conn.execute(self._LEGACY_TABLE_DROP)
                self.__conn.commit()
