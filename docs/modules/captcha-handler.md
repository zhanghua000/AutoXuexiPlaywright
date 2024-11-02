# Captcha Handler

Captcha handler is provider which will be called to handle captcha element, once one of them succeeds to call, other handlers will be ignored.

## Create captcha handler

Simply inherit `autoxuexiplaywright.sdk.CaptchaHandler` and finish all abstract attributes. The register it with `autoxuexiplaywright.sdk.module_entrance` decorator.

## Example

Here is a basic template to create the module, besides, you can check [captcha_handlers](../../src/autoxuexiplaywright/processor/captcha_handlers)
for an implementation by us. Althouth it does not belongs to a standalone python package, it still uses same way to be loaded.

```python
from typing import final
from typing import override
from semver import Version
from playwright.async_api import Locator
from autoxuexiplaywright.sdk import CaptchaHandler
from autoxuexiplaywright.sdk import module_entrance


@module_entrance(Version(4, 0, 0))
@final
class MyCustomCaptchaHandler(CaptchaHandler):
    @property
    @override
    def name(self) -> str:
        return self.__class__.__name__
        
    @property
    @override
    def author(self) -> str:
        return "You"
        
    @override
    async def solve(self, locator: Locator) -> bool:
        # Check if you support it and solve it if possible here.
        ...
```

Note the `@final` decorator, it is just let type checker know this class cannot be inherited so everything is abstract is not allowed.

If you need to do something at initialization, you can override `__init__` method, 
but do not forget to call `super().__init__()` or your module may not being initialized properly.

If you want to adjust your module's priority, you can override `priority` property.
But most of the time this is not encouraged to do so.
