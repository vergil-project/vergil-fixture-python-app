"""``greet NAME``: print a greeting."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("name", help="who to greet")


def _run(args: argparse.Namespace, console: Console) -> int:
    name: str = args.name
    if not name.strip():
        raise CommandError("the name must not be empty")
    # A Text, not a str, so rich markup in the name is printed as typed.
    console.print(Text(f"Hello, {name}"))
    return 0


COMMAND = Command(name="greet", help="Print a greeting.", configure=_configure, run=_run)
