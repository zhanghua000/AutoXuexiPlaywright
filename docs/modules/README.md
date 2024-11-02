# Documentation about modules of AutoXuexiPlaywright

## Migrations

If you go here for a migration guide, see [migrations.md](./migrations.md) for more info.

## Module types

We have many module types, most of the time, you should inherit it and completes all abstract attributes, and register it. Here is the list of module types:

1. [Answer source](./answer-source.md): Get answer from customized places.

2. [Captcha handler](./captcha-handler.md): Handle possible captcha on web page.

3. [Config parser](./config-parser.md): Provide ability to parse custom format of config.

4. [Reader](./reader.md): Do custom work on web page when reads news/videos.

5. [Record supported answer source](./record-supported-answer-source.md): Same to Answer source but it supports recording answer from webpage.

6. [Task](./task.md): Handle custom tasks on webpage.

See hyperlinks above for detailed guide to write proper code for modules.

> [!NOTE]
> If you want to create module but types above are not suitable, 
> you can always inherit `autoxuexiplaywright.module.Module` and create a generic module.
> You still need to decorate it with `autoxuexiplaywright.sdk.module_entrance` decorator.

## Create new modules

If you want to start from scratch to create your own module, you should follow those steps to make sure we can load it automatically:

1. Initialize a new python project.

    This depends your python package manager, you have to see its document for more info.
    
2. Add entrypoint.

    Your python package manager must support [PEP518](https://peps.python.org/pep-0518/), which defines a modern standard for storaging metadata of Python project.
    The you ned to create a table named `project.entry-points."autoxuexiplaywright.modules"`, 
    see [here](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#advanced-plugins) to fill it correctly.
    The double quotes are required because `autoxuexiplaywright.modules` is the table's name, 
    if there is no double quote, toml parser will think that there is a table named `autoxuexiplaywright` which contains a table named `modules`.

3. Write your code

    Then you can write your module as normal python package, you can use whatever you like. 
    But please add `autoxuexiplaywright` in its dependencies and register your module with `autoxuexiplaywright.sdk.module_entrance` decorator.
    As we do not upload to PyPI, you have to add `autoxuexiplaywright` with other methods, like wheel, source code tarball, or even VCS repository.
    
4. Distribute your module

    Your python package manager should provide command to build your project and generate a wheel, simply distributing that wheel should be fine.
