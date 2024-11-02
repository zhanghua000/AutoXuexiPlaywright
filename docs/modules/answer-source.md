# Answer Source

Answer source is answer provider which will be called to obtain answer one by one, once one of them succeeds to call, other sources will be ignored.

## Create answer source

Simply inherit `autoxuexiplaywright.sdk.AnswerSource` and finish all abstract attributes. The register it with `autoxuexiplaywright.sdk.module_entrance` decorator.

## Example

Here is a basic template to create the module, besides, you can check [answer_sources](../../src/autoxuexiplaywright/processor/answer_sources)
for an implementation by us. Althouth it does not belongs to a standalone python package, it still uses same way to be loaded.

```python
from typing import final
from typing import override
from semver import Version
from collections.abc import AsyncIterator
from autoxuexiplaywright.sdk import AnswerSource
from autoxuexiplaywright.sdk import module_entrance


@module_entrance(Version(4, 0, 0))
@final
class MyCustomAnswerSource(AnswerSource):
    @property
    @override
    def name(self) -> str:
        return self.__class__.__name__
        
    @property
    @override
    def author(self) -> str:
        return "You"
        
    @override
    async def get_answer(self, title: str) -> AsyncIterator[str]:
        # Yield your answers here
        ...
```

Note the `@final` decorator, it is just let type checker know this class cannot be inherited so everything is abstract is not allowed.

If you need to do something at initialization, you can override `__init__` method, 
but do not forget to call `super().__init__()` or your module may not being initialized properly.

If you want to adjust your module's priority, you can override `priority` property.
But most of the time this is not encouraged to do so.
