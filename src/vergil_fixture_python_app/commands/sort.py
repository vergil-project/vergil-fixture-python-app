"""``sort VERSION...``: list versions in PEP 440 order, one per line."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to sort")
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="list the newest version first"
    )


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    reverse: bool = args.reverse
    keyed: list[tuple[Version, str]] = []
    for text in texts:
        try:
            keyed.append((Version(text), text))
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    # Sort on the version alone, so equal versions keep the order given.
    keyed.sort(key=lambda pair: pair[0], reverse=reverse)
    for _, text in keyed:
        console.print(Text(text))
    return 0


COMMAND = Command(
    name="sort",
    help="List versions in PEP 440 order, one per line.",
    configure=_configure,
    run=_run,
)
