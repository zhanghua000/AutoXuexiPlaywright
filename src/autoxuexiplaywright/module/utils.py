"""Utils for autoxuexiplaywright.module pagkage."""

import logging
from semver import Version as _SemVer
from typing import Callable as _Callable
from collections.abc import Iterator
from autoxuexiplaywright import __version__ as _appversion
from autoxuexiplaywright.localize import gettext as __
from autoxuexiplaywright.module.module import Module as _Module


_modules: list[_Module] = []
_current_api_level = _SemVer.parse(_appversion)


def module_entrance[T: _Module](api_level: _SemVer) -> _Callable[[type[T]], type[T]]:
    """Register the module.

    Example:
        ```python
        @module_entrance(SemVer.parse("0.1.0"))
        class MyModule(Module): ...
        ```
    """

    def wrapper(module_type: type[T]) -> type[T]:
        logger = logging.getLogger(__name__)
        try:
            instance = module_type()
        except Exception as e:
            logger.error(
                __("Failed to create instance for %(name)s because %(e)s."),
                {"name": module_type.__name__, "e": e},
            )
        else:
            if not api_level.is_compatible(_current_api_level):
                logger.warning(
                    __("Found obsolete module %(name)s by %(author)s."),
                    {"name": instance.name, "author": instance.author},
                )
            if instance not in _modules and instance.initialized:
                logger.debug(
                    __("Load module %(name)s by %(author)s successfully."),
                    {"name": instance.name, "author": instance.author},
                )
                _modules.append(instance)
                _modules.sort(key=lambda m: m.priority)
        return module_type

    return wrapper


def iter_module_type[T: _Module](module_type: type[T]) -> Iterator[T]:
    """Iter the module matches type given.

    Args:
        module_type (type[Module]): The type of module.

    Yields:
        The module instance which matches type given.
    """
    for module in _modules:
        if isinstance(module, module_type):
            yield module
