import argparse
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from enum import Enum
from pathlib import Path
from typing import NoReturn

import virtualenv
import virtualenv.discovery.builtin


class Arch(Enum):
    X86_64 = "intel"
    ARM64 = "arm"


class Shell(Enum):
    SH = ""
    PS = ".ps1"
    CSH = ".csh"
    FISH = ".fish"


def main(python: str = "python", arch: Arch = Arch.X86_64) -> int:
    # load settings via env vars
    ezenv_shell: str = os.getenv("EZENV_SHELL", "sh")
    ezenv_target: str = os.getenv("EZENV_TARGET", "")

    # check settings
    try:
        my_shell = getattr(Shell, ezenv_shell.upper())
    except AttributeError:
        raise SystemExit(
            f" :: ERROR :: '{ezenv_shell}' is not allowed value for EZENV_SHELL."
        )
    my_target = Path(ezenv_target)
    if not my_target.exists():
        raise SystemExit(f" :: ERROR :: '{ezenv_target}' does not exist.")

    # find all interpreters
    interpreters: list[str] = (
        subprocess.run(f"which -a {python}", shell=True, capture_output=True)
        .stdout.decode()
        .strip()
        .split("\n")
    )
    if not interpreters:
        raise SystemExit(f" :: ERROR :: No interpreters found for '{python}'")

    exe: str = python
    if platform.system().lower() == "darwin":
        # look for "arm64" intepreter(s) only on MacOS, else its redundant
        arch_found: bool = False
        now_in_use: tuple[str, ...] = Path(sys.executable).parts[:-1]
        for exe in interpreters:
            if Path(exe).parts[:-1] == now_in_use:
                continue  # skip THIS env which is used for running this module
            if (
                subprocess.run(f"file {exe}", shell=True, capture_output=True)
                .stdout.strip()
                .decode()
                .endswith(arch.name.lower())
            ):
                arch_found = True
                break
        if not arch_found:
            msg = f" :: ERROR :: Python interpreter with arch {arch.value} not found"
            raise SystemExit(msg)

    # get info about what python its gonna be used
    cli_args: list[str] = ["--python", exe]
    fakenv: virtualenv.run.Session = virtualenv.session_via_cli(["fake"] + cli_args)
    interpreter: virtualenv.discovery.builtin.PathPythonInfo = fakenv.interpreter
    python_ver: str = interpreter.version_str

    print(f" :: found {exe} (arch {arch.name})")

    # /Users/dimsi/foo/bar -> foo/bar
    p: Path = Path(".").absolute().relative_to(Path.home())

    # foo/bar -> foo-bar
    p_dashed: str = "-".join(p.parts)

    # $VENVS/foo-bar-py3.10.7
    outdir: Path = my_target / f"{p_dashed}-py{arch.name.lower()}-{python_ver}"
    if outdir.exists():
        msg: str = f"""\
            Folder '{outdir}' exists.
            Overwrite? [y/N]
            """
        yn: str = input(textwrap.dedent(msg)) or "n"
        if yn.lower() in {"n", "no"}:
            raise SystemExit("Exit.")
        else:
            # delete existing venv dir to create fresh
            shutil.rmtree(outdir)

    # add dest path to args
    cli_args.insert(0, str(outdir))

    # safe option if case base python changes (eg. brew pythons)
    cli_args.append("--always-copy")

    # actually create it
    virtualenv.cli_run(args=cli_args)

    print(f" :: virtualenv {' '.join(cli_args)}")

    # activation script, use as: "source ,venvX.Y.Z"
    text = f"source {outdir}/bin/activate{my_shell.value}\n"
    Path(f",venv{python_ver}").write_text(text)

    return 0


def parse_args() -> argparse.Namespace:

    DEFAULT_ARCH: str = "intel"

    parser = argparse.ArgumentParser()
    parser.add_argument("python")
    parser.add_argument(
        "--arch",
        type=str,
        choices=[e.value for e in Arch],
        default=DEFAULT_ARCH,
        help=f"ask EZenv to find python intepreter of given architecture, default={DEFAULT_ARCH}",
    )

    return parser.parse_args()


def cli() -> NoReturn:
    args: argparse.Namespace = parse_args()
    ret: int = 1
    try:
        ret = main(python=args.python, arch=Arch(args.arch))
    except KeyboardInterrupt:
        raise SystemExit("Exit")

    raise SystemExit(ret)


if __name__ == "__main__":
    cli()
