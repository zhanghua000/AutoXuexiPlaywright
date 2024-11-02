# Migrations to legacy styled modules.

## What is legacy styled modules?

We have created a module system since V2, it is basically importing a standalone .py file. 
You create a py file and place it at modules folder, and we will load it automatically to invoke your code.

## Why it needs migrations

Althouth it did work, it has those disadvantages:

1. Dependencies

    Managing its dependencies is almost impossible. As we do not have a standard to exchange it.

2. Performance

    Python will compile .py to .pyc for speed. But for Unix users who install .py to a non-writable place like `/usr/share/autoxuexiplaywright/modules`,
    python cannot write such cache files.
    
3. Code maintainance

    Importing such standalone .py files instead normal python packages is also a disaster. 
    We need to do so many complex, low-level and easy-to-break works to import it correctly.
    See [here](https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly) for more info.
    
## What is the advantages

1. You can manage your module's dependencies easily as new styled modules are also normal python packages, you can use anything you like on it. 
    Dependencies are included in its `pyproject.toml`. You can use whatever buildsystem supports, like `setuptools`, `pdm`, `hatch` to build it.
    
2. Its installation and uninstallation are easy-to-made. New styled modules are python packages, 
    so you can install through commands like `pip install` and uninstall through commands like `pip uninstall`.
    
3. .pyc files are placed correctly. Python's installer will compile .py to .pyc when installs the package, so you do not worry about compiling .py manually.

4. Codes are easy to be maintained. New styled modules are very easy to be load, just use python's mechanism. Loading modules can be done with `EntryPoint.load` method.

## How to migration

You can use whatever python package manager you like. Just ensure they supports [this](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#advanced-plugins).
We will use [pdm](https://pdm-project.org/) as an example.

1. Prepare project

    Simply create a new python project by running `pdm init` in an empty directory and filling basic information.
    
2. Set entrypoint

    This is where magic happens. You just need to define an entrypoint in table `project.entry-points."autoxuexiplaywright.modules"`.
    For example, you can define like this:
    ```toml
    [project.entry-points."autoxuexiplaywright"]
    my-extension = "my_extension"
    ```
    
3. Setup dependencies
    
    Run `pdm add <package>` to add dependencies to your project. But please make sure you have added `autoxuexiplaywright`, 
    as we do not publish this program on PyPI, you need to add this package with other methods like tarball, wheel or git repository.
    For example, you can run `pdm add git+https://github.com/AutoXuexiPlaywright/AutoXuexiPlaywright.git#tag=v4.0.0` to add git repository with pinned version to v4.0.0.
    
4. Write the code

    You can write actual working code now, see [README.md](./README.md) for more info.
    If you just want to port your existing module into new style, you can copy its content and paste to file `__init__.py` in your project source.
    For project managed by pdm, this file is usually placed at `src/<project>/__init__.py`.
    
5. Installation

    Build your module project with package manager, for pdm managed project, you can run `pdm build` to build everything, and you will find wheel at `dist` folder.
    Users should install the wheel to install module, when AutoXuexiPlaywright starts, we will load the module automatically.
