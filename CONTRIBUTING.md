# How to contribute

As an open-sourced project, contributions are always welcomed. To prevent unneeded waste of resources, we recommend you folowing those suggestions:

## Issue

If you find a bug or something needs improvements, you can create an issue at [Issues](https://github.com/AutoXuexiPlaywright/AutoXuexiPlaywright/issues), 
but please follow issue templates to provide required information.

## Pull Request

If you have made some changes to the code, you can create a pull request at [Pull Requests](https://github.com/AutoXuexiPlaywright/AutoXuexiPlaywright/pulls).
We have set up GitHub Actions to check code automatically, so if there is something wrong, please fix it in order to get your changes merged.

## Workflows to make changes

If you are new to GitHub, here are some steps to make changes to an existing repository:

1. Fork the repository

    Click [Fork](https://github.com/AutoXuexiPlaywright/AutoXuexiPlaywright/fork) to create a copy of this repository under your GitHub account.
    
2. Clone the code

    Install `git` to clone the code, run `git clone https://github.com/<your-account-name>/AutoXuexiPlaywright` to clone the forked repository to local.
    
3. Change the code

    Use your favorate editor/ide to make changes to the code. But we have some style rules:
    
    - Using `snake_case` for functions and variables, using `SNAKE_CASE` for constraints.
    
    - Using `PascalCase` for classes.
    
    We have some extra rules defined in [pyproject.toml](./pyproject.toml), you can run `pdm run ruff check` to check if your code meets requirements.
    But this requires you installed development dependencies by running `pdm install --dev` command.
    
    Please ensure all tests are passed by running `pdm run pytest`, although this project is hard to create unit tests, it is still tested with pytest
    for code style by `pytest-ruff` package.
    
4. Update the code

    Simply run `git commit` and you should be prompted with a commit message editor.
    We do not have commit message style requirements now, just make your commit easy-to-read.
    
    Optional: Setting up gpg key to sign your commit should help preventing your commit being corrupted.
    
    Notes: Both commit and sign commit requires an email address, if you do not want to use your main email address,
    you can use GitHub's no-reply address, go to [here](https://github.com/settings/emails) to find it out.
    It should end with `@users.noreply.github.com`. Username can be your GitHub account name.
    Email, gpg key and username can be set locally by adding a `--local` flag to `git config` to prevent changing your global config.
    
    After you commited the code, you can run `git push` to push it to your forked repository.
    
5. Create Pull Request

    You should see instruction on webpage by GitHub to create a pull request if you pushed successfully, 
    just follow it and you should create one. Pull request notifies us to check your code and merge it if possible.
    You can reload webpage to see it if it does not appear.
    
    After you created pull request, all future changes will be synced to the pull request so you do not need to create a new one.
    
## Tips for translators

Translating AutoXuexiPlaywright into different languages or fixing translating problems is always welcomed.
We have created some pdm scripts to help with this, but you need to install install `build` group of development dependencies.
Here are scripts maybe useful for you:

- `extract_pot`: This script extracts messages to be translated into a `.pot` file, which can be used to generate `.po` file.
    Usage: `pdm run extract_pot --version=$(pdm show --version)`
    
- `init_po`: This script generates `.po` file from `.pot` file.
    Usage: `pdm run init_po --locale=<locale>`
    
- `update_po`: This script updates existing `.po` file from `.pot` file.
    Usage: `pdm run update_po --locale=<locale>`

After finished translation, you need to commit `.po` file and create pull request so we can see if it is fine to be merged.
