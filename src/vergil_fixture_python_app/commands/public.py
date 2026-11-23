"""``public VERSION...``: print the public version of each version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to make public")


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    # Parse every version before printing any, so a bad one prints nothing.
    publics: list[str] = []
    for text in texts:
        try:
            publics.append(Version(text).public)
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    for public in publics:
        console.print(Text(public))
    return 0


COMMAND = Command(
    name="public",
    help="Print the public version (no local label) of each version.",
    configure=_configure,
    run=_run,
)
