"""Scan data folders and load modules."""

from logging import getLogger as _get_logger
from importlib.metadata import entry_points
from autoxuexiplaywright.localize import gettext as __


ENTRYPOINT_GROUP, _, _ = __name__.rpartition(".")


def load_modules():
    """Load modules from module_folder."""
    logger = _get_logger(__name__)

    for entrypoint in entry_points(group=ENTRYPOINT_GROUP):
        logger.debug(__("Loading module %(name)s"), {"name": entrypoint.name})
        try:
            entrypoint.load()
        except Exception as e:
            logger.error(__("Load module failed because %(e)s"), {"e": e})
