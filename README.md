# EZenv

Create all virtual environments in a single, centralized directory.

**WHY?**

- From time to time I feel like I want to delete all unused venvs but its annoying to traverse all projects and look for ".venv*" dirs. So its nice to have them all in one place.
- Also, I can have running Time Machine and avoid backing up (by ignoring a single dir) all python virtual envs!
- And on top of that, I can quickly decide if I want Arm64 venv or x64 venv (which has better support, but runs slower via Rosetta).

## Usage

```sh
export EZVENV_TARGET=$HOME/Virtualenvs  # where all my venvs will be

cd ~/Projects/myproject
ezenv python3.10
```

That last command will:

1. look for **python 3.10.x** in your PATH
1. create virtualenv in `EZVENV_TARGET` in deterministic format, in our example its gonna be
    - `/Users/me/Virtualenvs/Projects-myproject__x86_64-py3.10.9`
1. create `,venv3.10.9` file in your project directory, which is an easy way to activate your venv like
    - `source ,venv3.10.9`

## 1. Settings

Set env vars:

```sh
EZVENV_TARGET
EZVENV_SHELL  # optional
```

### 1.1 `EZVENV_TARGET`

Tell **EZenv** where to save your virtual envs. Directory must exist.

### 1.2 `EZVENV_SHELL` (optional)

Tell **EZenv** which shell you are using. It will adjust `,venvX.Y.Z` file. Possible options are:

1. `SH`
    - default, in case you use `sh`, `bash`, `zsh` and similar
1. `FISH`
    - in case you use fish shell
1. `PS`
    - in case you use PowerShell 🤷🏻‍♂️
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
