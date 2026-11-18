"""``normalize VERSION...``: print the PEP 440 normal form of each version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to normalize")


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    # Parse every version before printing any, so a bad one prints nothing.
    normalized: list[str] = []
    for text in texts:
        try:
            normalized.append(str(Version(text)))
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    for line in normalized:
        console.print(Text(line))
    return 0


COMMAND = Command(
    name="normalize",
    help="Print the PEP 440 normal form of each version, one per line.",
    configure=_configure,
    run=_run,
)
