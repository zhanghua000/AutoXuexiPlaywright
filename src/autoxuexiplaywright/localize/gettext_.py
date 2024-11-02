"""gettext which can load messages from resources instead static path."""

from io import BytesIO as _BytesIO
from locale import getlocale as _get_locale
from gettext import GNUTranslations as _Translator
from pathlib import Path as _Path
from autoxuexiplaywright.storage import get_overlayed_resource_content as _get_resource


def gettext(message: str) -> str:
    """Translate message."""
    return message


_domain = __name__.split(".")[0]
_lang = _get_locale()[0]
if _lang is not None:
    _translation = _Path("translations/{}/LC_MESSAGES/{}.mo".format(_lang, _domain))
    _mo = _get_resource(_translation)
    if _mo is not None:
        _translator = _Translator(_BytesIO(_mo))
        gettext = _translator.gettext
