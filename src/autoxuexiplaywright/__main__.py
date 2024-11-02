"""Entrypoint for command autoxuexiplaywright."""

# pyright: reportAny=false

import logging
from pathlib import Path as _Path
from argparse import ArgumentParser as _ArgumentParser
from argparse import BooleanOptionalAction as _BooleanOptionalAction
from deserializer import deserialize as _deserialize
from deserializer import set_log_level as _deserialize_log_level
from autoxuexiplaywright import APPNAME as _APPNAME
from autoxuexiplaywright import __name__ as _logger_name
from autoxuexiplaywright.config import Config as _Config
from autoxuexiplaywright.config import get_config as _get_config
from autoxuexiplaywright.module import load_modules as _load_modules
from autoxuexiplaywright.ui.tui import launch as _launch_tui
from autoxuexiplaywright.storage import get_state_path as _get_state
from autoxuexiplaywright.storage import get_config_path as _config_path
from autoxuexiplaywright.localize import gettext as __


try:
    from autoxuexiplaywright.ui.qt import launch as _launch
except ImportError:
    _launch = _launch_tui


def main():
    """Main entrypoint for command autoxuexiplaywright."""
    parser = _ArgumentParser()
    _ = parser.add_argument(
        "--gui",
        action=_BooleanOptionalAction,
        help=__("If enable gui mode."),
    )
    _ = parser.add_argument(
        "--config",
        "-c",
        type=_Path,
        help=__("The path to config file."),
    )
    _ = parser.add_argument(
        "--debug",
        action=_BooleanOptionalAction,
        help=__("If enable debug mode."),
    )
    args = parser.parse_args()
    default_config = _config_path(_Path("config.json"))
    current_directory_default_config = _Path("config.json")
    log_file = _get_state(_Path(_APPNAME + ".log"))
    log_file.parent.mkdir(parents=True, exist_ok=True)

    init_level = (
        logging.DEBUG if isinstance(args.debug, bool) and args.debug else logging.INFO
    )
    logger = logging.getLogger(_logger_name)
    logger.setLevel(init_level)
    fmt = logging.Formatter(
        "%(asctime)s-%(levelname)s-%(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(
        logging.FileHandler(
            log_file,
            mode="w",
        ),
    )
    for handler in logger.handlers:
        handler.setFormatter(fmt)
        handler.setLevel(logger.level)

    _load_modules()

    config_path = (
        args.config
        if isinstance(args.config, _Path)
        else default_config
        if default_config.exists()
        else current_directory_default_config
    )
    config_dict = _get_config(config_path)
    if config_dict is None:
        logger.info(__("Using default config."))
        config = _Config()
    else:
        logger.info(
            __("Deserializing config from file %(config_path)s."),
            {"config_path": config_path},
        )
        _deserialize_log_level("DEBUG" if args.debug else "INFO")
        config = _deserialize(_Config, config_dict)
    _deserialize_log_level("DEBUG" if config.debug else "INFO")
    if isinstance(args.gui, bool):
        config.gui = args.gui
    if isinstance(args.debug, bool):
        config.debug = args.debug
    logger.setLevel(logging.DEBUG if config.debug else logging.INFO)
    for handler in logger.handlers:
        handler.setLevel(logger.level)
    if config.gui:
        config.gui = _launch != _launch_tui
        logger.debug(
            __("GUI mode enabled: %(gui)s"),
            {"gui": config.gui},
        )
        _launch(config)
    else:
        _launch_tui(config)


if __name__ == "__main__":
    main()  # python -m autoxuexiplaywright
