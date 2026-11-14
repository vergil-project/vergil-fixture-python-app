"""``compare LEFT RIGHT``: order two versions by the PEP 440 rules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("left", help="the first version")
    parser.add_argument("right", help="the second version")


def _parse(text: str) -> Version:
    try:
        return Version(text)
    except InvalidVersion as exc:
        raise CommandError(f"not a valid version: {text!r}") from exc


def _run(args: argparse.Namespace, console: Console) -> int:
    left: str = args.left
    right: str = args.right
    left_version, right_version = _parse(left), _parse(right)
    if left_version < right_version:
        relation = "<"
    elif left_version > right_version:
        relation = ">"
    else:
        relation = "=="
    console.print(Text(f"{left} {relation} {right}"))
    return 0


COMMAND = Command(
    name="compare",
    help="Order two versions by the PEP 440 rules.",
    configure=_configure,
    run=_run,
)
