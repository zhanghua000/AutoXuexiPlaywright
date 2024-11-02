"""Utils for autoxuexiplaywright.config package."""

import logging
from pathlib import Path as _Path
from autoxuexiplaywright.sdk import ConfigParser as _ConfigParser
from autoxuexiplaywright.sdk import ConfigJsonType as _ConfigJsonType
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.module.utils import iter_module_type as _filter_modules


def get_config(path: _Path) -> _ConfigJsonType | None:
    """Get config from path given."""
    logger = logging.getLogger(__name__)
    for parser in _filter_modules(_ConfigParser):
        if path.is_file() and parser.is_support(path):
            try:
                return parser.get_config(path)
            except Exception as e:
                logger.error(
                    __("Failed to parse config because %(e)s"),
                    {"e": e},
                )
    return None
