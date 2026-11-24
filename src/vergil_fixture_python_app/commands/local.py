"""``local VERSION...``: print the local label of each version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to read")


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    # Read every version before printing any, so a bad one prints nothing.
    labels: list[str] = []
    for text in texts:
        try:
            label = Version(text).local
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
        if label is None:
            raise CommandError(f"no local label: {text!r}")
        labels.append(label)
    for label in labels:
        console.print(Text(label))
    return 0


COMMAND = Command(
    name="local",
    help="Print the local label (the part after +) of each version.",
    configure=_configure,
    run=_run,
)
