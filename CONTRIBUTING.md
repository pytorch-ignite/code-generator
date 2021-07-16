# Code-Generator Contribution Guide

Hi! Thanks for your interest in contributing to Code-Generator.
Before submitting your contribution, please make sure to take a moment and read through the following guide.

Contributing to Code-Generator can be divided into two parts:

- [Contributing to Code-Generator App](#contributing-to-code-generator-app)
- [Contributing to Templates](#contributing-to-templates)

## Development Setup

> For contributing to templates, this step is NOT strictly required.
> But installing the requirements will allow you to test the app locally.
>
> Or you can send the PR to test the app using PR Preview feature from Netlify.

To contribute to Code-Generator App, you will need Nodejs LTS v14.16.x, VSCode, Vetur, pip or conda, and pnpm package manager.

- Install [VSCode](https://code.visualstudio.com/) according to your OS.

- Install [Vetur extension](https://marketplace.visualstudio.com/items?itemName=octref.vetur) to get syntax highlighting for `.vue` files. You can search `Vetur` in VSCode Extensions Tab to install.

- Install Nodejs LTS v14.16.x from https://nodejs.org for macOS and Windows. For Linux distributions, please follow the steps from [Node.js Website](https://nodejs.org/en/download/package-manager/) and [NodeSource GitHub](https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions).

- Install pnpm from https://pnpm.io/installation. Use standalone script if there is a root issue with installing with npm.

- Create a virtual environment for python.

  - With pip:

    ```sh
    # create a virtual environment with built-in venv.
    python -m venv ~/.code-generator-venv
    # activate the virtual envrionment
    source ~/.code-generator-venv/bin/activate
    ```

  - With conda:
    ```sh
    # create a virtual environment with conda.
    conda create -n code-generator-venv
    # activate the virtual envrionment
    conda activate code-generator-venv
    ```

- Install the dependencies with `pnpm install` and `bash scripts/run_code_style.sh install` in the project root directory. This might take a while to install.

- Run `pnpm run dev` to start local development server and starts editing the codes in the `src` directory. Changes will be updated on the app.

- If you want to test building the app locally, run `pnpm run build`. This will generate the `dist` directory which contains all the codes for the app to run from CDN or web server. You can test the built codes in the `dist` with `pnpm run serve`. However, changes won't be updated on the app with this command.

## Contributing to Code-Generator App

Code-Generator is a web app built with Vue 3. Source code is mainly in the files of `src`, `src/components`, `src/metadata` directories. See [`src/REAME.md`](./src/README.md).

- If you have found bugs, please send a PR fixing the bugs.
- If you have design, layout, and UI improvements, please open a suggestion issue first, discuss with the maintainers, and have it approved before working on it.

## Contributing to Templates

Training codes are generated from templates with [`ejs`](https://ejs.co). Templates live in `src/templates` directory.
To add a new template,

1. Create a folder whose name should start with `template` followed by template name in the `src/templates` directory.

2. Put the template code files in that directory.

3. Training configurations are managed with Argparse + YAML file. A single configuration yaml file is needed. Usually, it is `config.yaml`. What to put inside in `config.yaml` can be copied from `template-common/config.yaml` and adjust with the respective template.

4. To have Ignite core features and distributed training, you have to add some template code in the `main.py`. You can reference the template codes from `template-vision-classification/main.py`. They can be found with below comments.

   - `setup ignite handlers` - to have various useful handlers provided by Ignite core modules.
   - `experiment tracking` - to have experiment trakcing system provided by Ignite contrib integration.
   - `close logger` - to close the experiment tracking loggers after the training finished.
   - `show the last checkpoint filename` - to print the last checkpoint filename (training, evaluation) to find quickly.
   - `main entrypoint` - to have training works with both distributed/non-distributed and launch/spawn training.

5. Once everything looks good, put the template name with respective filenames (in array format) in the `templates.json` in `src/templates` directory. This is required to tell Code-Generator to fetch the files from this template.

6. In the `README.md`, copy the training launch code from `src/template-common/README.md`.

7. For the `requirements.txt`, copy from the `src/template-common/requirements.txt`.

8. For the `utils.py`, copy the starter code from the `src/template-common/utils.py`.

9. You can check if the copied codes needed are up-to-date with the base codes with: `python scripts/check_copies.py`

10. Add model forward and dataloading tests in the `test_all.py`.

## Pull Request Guidelines

- Checkout a topic branch from a base branch, e.g. `main` (currently).

- If adding a new template:

  - Make sure the tests pass.

  - Please open a suggestion issue first and have it approved before working on it.

- It's OK to have multiple small commits as you work on the PR - GitHub can automatically squash them before merging.

- If you contribute to the Code-Generator App itself, you can format with this command:

  ```sh
  # format
  pnpm run fmt
  # lint
  pnpm run lint
  ```

- To ensure the codebase complies with a style guide, we use black and isort tools to format and check codebase for compliance with PEP8. Install and run with:

  ```sh
  # install code formatting dependencies
  bash .github/run_code_style.sh install
  # format the codes
  bash .github/run_code_style.sh fmt
  # lint the codes
  bash .github/run_code_style.sh lint
  ```

_NOTE: Even if you have a half-completed/working PR, sending a PR is still a valid contribution and we can help you finish the PR._

**NOTE : When sending a PR, please kindly check if the changes are required to run in the CI.**

For example, typo changes in `CONTRIBUTING.md`, `README.md` are not required to run in the CI. So, please add `[skip ci]` in the PR title to save the resources.

**NOTE : Those skip statement is case sensitive and needs open bracket `[` and close bracket `]`.**

## Sync up with the upstream

First, make sure you have set [upstream](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork) by running:

```sh
git remote add upstream https://github.com/pytorch-ignite/code-generator
```

Then you can see if you have set up multiple remote correctly by running git remote -v:

```sh
origin  https://github.com/<your-github-username>/code-generator (fetch)
origin  https://github.com/<your-github-username>/code-generator (push)
upstream        https://github.com/pytorch-ignite/code-generator (fetch)
upstream        https://github.com/pytorch-ignite/code-generator (push)
```

Now you can get the latest development into your forked repository with this:

```sh
git fetch --all --prune
git checkout main
git merge upstream/main
```
