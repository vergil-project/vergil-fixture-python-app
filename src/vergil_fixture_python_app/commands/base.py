"""``base VERSION...``: print the base version of each version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to reduce")


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    # Parse every version before printing any, so a bad one prints nothing.
    bases: list[str] = []
    for text in texts:
        try:
            bases.append(Version(text).base_version)
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    for base in bases:
        console.print(Text(base))
    return 0


COMMAND = Command(
    name="base",
    help="Print the base version (epoch and release) of each version.",
    configure=_configure,
    run=_run,
)
