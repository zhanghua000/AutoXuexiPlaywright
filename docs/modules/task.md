# Task

Task is operations providers which will be called to handle tasks generated from status page, the first one supports task title will be used, other providers will be ignored.

## Create answer source

Simply inherit `autoxuexiplaywright.sdk.Task` and finish all abstract attributes. The register it with `autoxuexiplaywright.sdk.module_entrance` decorator.

## Example

Here is a basic template to create the module, besides, you can check [tasks](../../src/autoxuexiplaywright/processor/tasks)
for an implementation by us. Althouth it does not belongs to a standalone python package, it still uses same way to be loaded.

```python
from typing import final
from typing import override
from semver import Version
from playwright.async_api import Page
from autoxuexiplaywright.sdk import Task
from autoxuexiplaywright.sdk import module_entrance


@module_entrance(Version(4, 0, 0))
@final
class MyCustomTask(Task):
    @property
    @override
    def name(self) -> str:
        return self.__class__.__name__
        
    @property
    @override
    def author(self) -> str:
        return "You"
        
    @properly
    @override
    def requires(self) -> list[Task]:
        # Let us know what you need, 
        # most of the time it should be login.
        # You can use `autoxuexiplaywright.processor.first_task`
        # or `autoxuexiplaywright.processor.iter_task` to find out
        # what you need.
        ...
    
    @properly
    @override
    def handles(self) -> list[str]:
        # What task title(s) can you handle.
        ...
        
    @override
    async def _handle(self, page: Page, task_name: str) -> bool:
        # Do your operations here.
        ...
```

Note the `@final` decorator, it is just let type checker know this class cannot be inherited so everything is abstract is not allowed.

If you need to do something at initialization, you can override `__init__` method, 
but do not forget to call `super().__init__()` or your module may not being initialized properly.

If you want to adjust your module's priority, you can override `priority` property.
But most of the time this is not encouraged to do so.
