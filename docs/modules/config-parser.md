# Config Parser

Config parser is config provider which will be called to obtain config given from commandline or default paths, once one of them succeeds to call, other providers will be ignored.

## Create config parser

Simply inherit `autoxuexiplaywright.sdk.ConfigParser` and finish all abstract attributes. The register it with `autoxuexiplaywright.sdk.module_entrance` decorator.

## Example

Here is a basic template to create the module, besides, you can check [config_parsers](../../src/autoxuexiplaywright/config)
for an implementation by us. Althouth it does not belongs to a standalone python package, it still uses same way to be loaded.

```python
from typing import final
from typing import override
from semver import Version
from pathlib import Path
from autoxuexiplaywright.sdk import ConfigJsonType
from autoxuexiplaywright.sdk import ConfigParser
from autoxuexiplaywright.sdk import module_entrance


@module_entrance(Version(4, 0, 0))
@final
class MyCustomConfigParser(ConfigParser):
    @property
    @override
    def name(self) -> str:
        return self.__class__.__name__
        
    @property
    @override
    def author(self) -> str:
        return "You"
        
    @override
    def is_support(self, path: Path) -> bool:
        # Check if the path given is supported.
        ...
        
    @override
    def get_config(self, path: Path) -> ConfigJsonType:
        #Do parse job yourself.
        ...
```

Note the `@final` decorator, it is just let type checker know this class cannot be inherited so everything is abstract is not allowed.

If you need to do something at initialization, you can override `__init__` method, 
but do not forget to call `super().__init__()` or your module may not being initialized properly.

If you want to adjust your module's priority, you can override `priority` property.
But most of the time this is not encouraged to do so.
