"""``bump PART VERSION``: print the next release after a version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console

PARTS = ("major", "minor", "micro")


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("part", choices=PARTS, help="the release number to raise")
    parser.add_argument("version", help="the version to bump")


def _run(args: argparse.Namespace, console: Console) -> int:
    part: str = args.part
    text: str = args.version
    try:
        version = Version(text)
    except InvalidVersion as exc:
        raise CommandError(f"not a valid version: {text!r}") from exc
    # Pad to major.minor.micro, raise the named part and zero the ones after it.
    release = [*version.release, 0, 0][:3]
    index = PARTS.index(part)
    release[index] += 1
    release[index + 1 :] = [0] * (2 - index)
    bumped = ".".join(str(number) for number in release)
    if version.epoch:
        bumped = f"{version.epoch}!{bumped}"
    console.print(Text(bumped))
    return 0


COMMAND = Command(
    name="bump",
    help="Print the next major, minor or micro release of a version.",
    configure=_configure,
    run=_run,
)
