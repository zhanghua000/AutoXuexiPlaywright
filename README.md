# AutoXuexiPlaywright

## What is this?

A script to finish XuexiQiangguo's everyday task automatically.

## Changes since legacy version

This is a completely rewrite, you can see [CHANGELOG.md](./CHANGELOG.md) for more info.

## How to use?

1. Download wheel from [Release](https://github.com/AutoXuexiPlaywright/AutoXuexiPlaywright/releases) or [Build](#how-to-build) it yourself.

2. Install the wheel by running `pip install /path/to/wheel.whl` in terminal.
   If you want to use gui, install `[gui]` dependencies specifiers.
   If you want to use uvloop, install `[uvloop]` dependencies specifiers.

3. Install the browser by running `playwright install` in terminal.

4. Launch the program by running `autoxuexiplaywright` in terminal.

> [!TIP]
> You can run `playwright install --help` to see how to avoid installing all browsers.
> You can also skip installing browser and set customized browser executable path.
> But your custom browser is still needed to be supported by playwright.

## How to build?

1. Prepare Python: We need 3.12 and above as we use many new-introduced features of Python, such as `type` statement.

2. Install pdm: We use pdm to manage dependencies, see [here](https://pdm-project.org/en/latest/#installation) if you need help.

3. Install dependencies: Run `pdm install` to install basic dependencies. Run `pdm install --dev` if you need extra dependencies for developing.

4. Build the wheel: Run `pdm build` to build the wheel, you can get wheel at `dist` directory.

## Notes

1. This tool is under heavy development and may not as stable as other tools. Some features may also don't work as expected. Everyone's pull request to improve this tool is welcome.

2. This tool is designed only finishing tasks listed on [website](https://xuexi.cn), your max score in one day is 30 after using this tool correctly because some tasks are only available on mobile app.

3. This tool is just for researching purpose, we don't be responsible for any result by using this tool. There is also no guarantee or warranty. **Use it at your own risk.**
