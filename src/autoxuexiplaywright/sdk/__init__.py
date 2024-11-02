"""Classes and functions allowed to be extended by modules."""

from autoxuexiplaywright.module import module_entrance as module_entrance
from autoxuexiplaywright.sdk.task import Task as Task
from autoxuexiplaywright.sdk.reader import Reader as Reader
from autoxuexiplaywright.sdk.answer_source import AnswerSource as AnswerSource
from autoxuexiplaywright.sdk.config_parser import ConfigParser as ConfigParser
from autoxuexiplaywright.sdk.config_parser import ConfigJsonType as ConfigJsonType
from autoxuexiplaywright.sdk.captcha_handler import CaptchaHandler as CaptchaHandler
from autoxuexiplaywright.sdk.record_supported_answer_source import (
    RecordSupportedAnswerSource as RecordSupportedAnswerSource,
)
