"""Functions to launch TUI."""

try:
    from uvloop import run as _run_async
except ImportError:
    from asyncio import run as _run_async
from logging import getLogger as _get_logger
from pathlib import Path as _Path
from autoxuexiplaywright.event import EventID as _EventID
from autoxuexiplaywright.event import FinishedEvent as _FinishedEvent
from autoxuexiplaywright.event import QrUpdatedEvent as _QrUpdatedEvent
from autoxuexiplaywright.event import find_event_by_id as _find_event
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.storage import get_cache_path as _cache_path
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.processor import launch_processor as _launch_processor


_qr_file = _cache_path(_Path("qr.png"))


def _on_qr_updated(content: bytes):
    _ = _qr_file.write_bytes(content)
    logger = _get_logger(__name__)
    logger.info(
        __("Please scan QR code at %(path)s to login."),
        {"path": _qr_file},
    )


def _remove_qr_image(_: int):
    _qr_file.unlink(missing_ok=True)


def launch(config: _Config):
    """Launch the TUI."""
    qr_updated_event = _find_event(_EventID.QR_UPDATED, _QrUpdatedEvent)
    if qr_updated_event is not None:
        _ = qr_updated_event.add_callback(_on_qr_updated)

    if not config.debug:
        finished_event = _find_event(_EventID.FINISHED, _FinishedEvent)
        if finished_event is not None:
            _ = finished_event.add_callback(_remove_qr_image)

    coro = _launch_processor(config)
    _run_async(coro)
