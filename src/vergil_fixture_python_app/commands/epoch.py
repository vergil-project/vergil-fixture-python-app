"""``epoch VERSION...``: print the epoch of each version."""

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
    epochs: list[int] = []
    for text in texts:
        try:
            epochs.append(Version(text).epoch)
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    for epoch in epochs:
        console.print(Text(str(epoch)))
    return 0


COMMAND = Command(
    name="epoch",
    help="Print the PEP 440 epoch (0 when absent) of each version.",
    configure=_configure,
    run=_run,
)
