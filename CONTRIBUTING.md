# Code-Generator Contribution Guide

Hi! Thank for your interest in contributing to Code-Generator.
Before submitting your contribution, please make sure to take a moment and read through the following guide:

## Repo Setup

**Quickstart guide for first-time contributors**

<details>

- Install [miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html) for your system.

- Create an isolated conda environment for Code-Generator:

  ```sh
  conda create -n code-generator-dev python=3.8
  ```

- Activate the newly created environment:

  ```sh
  conda activate code-generator-dev
  ```

- When developing please take care of preserving `.gitignore` file and make use of `.git/info/exclude` to exclude custom files like: `.idea`, `.vscode` etc.

- Please refer to [github first contributions guidelines](https://github.com/firstcontributions/first-contributions) and don't hesitate to ask the pytorch-ignite community in case of any doubt.

</details>

To develop and test Code-Generator:

- Fork this repository.

- Clone the repo and install dependencies.

  ```sh
  git clone https://github.com/<your-github-username>/code-generator.git
  cd code-generator
  pip install -r requirements-dev.txt
  ```

- Generate and run the tests.
  ```sh
  bash .github/run_test.sh generate
  bash .github/run_test.sh unittest
  ```

## Code development

### Codebase structure

- [app](https://github.com/pytorch-ignite/code-generator/tree/master/app) - Directory containing files about Streamlit App and code generation
- [templates](https://github.com/pytorch-ignite/code-generator/tree/master/templates) - Directory containing ML/DL Templates
- [tests](https://github.com/pytorch-ignite/code-generator/tree/master/tests) - Directory containing test related files

> TIP
>
> If you are adding a new template, use Single Model, Singe Optimizer Template from
> [Code-Generator](https://share.streamlit.io/pytorch-ignite/code-generator) itself
> to generate a base template and extend according to the new template you want to add.

## Pull Request Guidelines

- Checkout a topic branch from a base branch, e.g. `master`.

- If adding a new template:

  - Please open a suggestion issue first and have it approved before working on it.
  - Add accompanying test cases – internal tests should live in `_test_internal.py` and the rest in `test_all.py`.

- It's OK to have multiple small commits as you work on the PR - GitHub can automatically squash them before merging.

- Make sure tests pass!

- To ensure the codebase complies with a style guide, we use flake8, black and isort tools to format and check codebase for compliance with PEP8. Install and run with:

  ```sh
  # install code formatting dependencies
  bash .github/run_code_style.sh install
  # format the codes
  bash .github/run_code_style.sh fmt
  # lint the codes
  bash .github/run_code_style.sh lint
  ```

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
git checkout master
git merge upstream/master
```
