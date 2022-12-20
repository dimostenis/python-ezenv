# EZenv

Create all virtual environments in a single, centralized directory.

## Usage

```sh
export EZVENV_TARGET=$HOME/Virtualenvs  # where all my venvs will be

cd ~/Projects/myproject
ezenv python3.10
```

Command will:

1. look for **python 3.10.x** in your PATH
1. create virtualenv in `EZVENV_TARGET` in deterministic format, in our example to
    - `/Users/me/Virtualenvs/Projects-myproject-x86_64-py3.10.9`
1. create `,venv3.9.10` file in your project directory, which is an easy way to activate your venv like
    - `source ,venv3.9.10`

## 1. Settings

Set env vars:

```sh
EZVENV_TARGET
EZVENV_SHELL  # optional
```

### 1.1 `EZVENV_TARGET`

Tell **EZenv** where to save your virtual envs. Directory must exist.

### 1.2 `EZVENV_SHELL` (optional)

Tell **EZenv** which shell you are using. Possible options are:

1. `SH`
    - default, in case you use `sh`, `bash`, `zsh` and similar
1. `FISH`
    - in case you use fish shell
1. `PS`
    - in case you use PowerShell
1. `CSH`
    - in case you use C shell

## 2. Prerequisites

- python interpreters in `$PATH`
    - if you need python3.9 venv, you need `python3.9` to exist in your PATH
- `which` utility
    - to find all intepreters
- `file` utility (ONLY if you run MacOS)
    - to check architecture of python iterpreter

## 3. Support

Tested and used on MacOS, but shall work fine on linux too.
