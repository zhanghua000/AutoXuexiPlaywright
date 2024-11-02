"""Utils for autoxuexiplaywright.processor.tasks package."""

from collections.abc import Iterator as _Iterator
from autoxuexiplaywright.sdk import Task as _Task
from autoxuexiplaywright.module import iter_module_type as _filter_module


def iter_task(handle: str | None = None) -> _Iterator[_Task]:
    """Iter the task that can handle the task string given.

    Yields:
        Task: The instance of task that has `handle`
        in its `handles` property.
    """
    for module in _filter_module(_Task):
        if handle is None or handle in module.handles:
            yield module


def first_task(handle: str) -> _Task:
    """Get first task that can handle the task string.

    Raises:
        ValueError: If no task is found.
    """
    for task in iter_task(handle):
        return task
    raise ValueError("No task is found.")


def clean_string(i: str) -> str:
    """Clean the string to remove useless parts."""
    return i.strip().replace("\n", "")
