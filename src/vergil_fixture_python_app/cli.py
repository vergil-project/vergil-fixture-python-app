"""The ``vergil-fixture-python-app`` entry point.

It builds one ``argparse`` subcommand for each :class:`Command` in
:data:`~vergil_fixture_python_app.commands.COMMANDS` and runs the one named
on the command line.
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console

from vergil_fixture_python_app.command import CommandError
from vergil_fixture_python_app.commands import COMMANDS

PROG = "vergil-fixture-python-app"


def build_parser() -> argparse.ArgumentParser:
    """The parser for the program, with every registered subcommand."""
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="A small command-line program that serves as a Vergil test fixture.",
    )
    subparsers = parser.add_subparsers(
        title="commands", dest="command", metavar="<command>", required=True
    )
    for command in COMMANDS:
        sub = subparsers.add_parser(command.name, help=command.help, description=command.help)
        command.configure(sub)
        sub.set_defaults(handler=command.run)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the program on ``argv`` (``sys.argv[1:]`` when ``None``).

    Returns the exit status. A usage error exits with status 2, through
    ``argparse``; a :class:`CommandError` is printed on stderr and returns 1.
    """
    args = build_parser().parse_args(argv)
    console = Console(highlight=False, soft_wrap=True)
    try:
        status: int = args.handler(args, console)
    except CommandError as exc:
        print(f"{PROG}: {exc}", file=sys.stderr)
        return 1
    return status
