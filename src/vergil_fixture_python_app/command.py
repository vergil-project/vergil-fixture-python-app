"""The shape every subcommand takes.

A subcommand is one module under :mod:`vergil_fixture_python_app.commands`
that defines a :class:`Command`. Adding a subcommand is a new module, one
entry in :data:`vergil_fixture_python_app.commands.COMMANDS`, and its tests;
nothing else changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

    from rich.console import Console


class CommandError(Exception):
    """A failure a subcommand reports to the user.

    The CLI prints the message on stderr, prefixed with the program name, and
    exits with status 1.
    """


@dataclass(frozen=True)
class Command:
    """One subcommand: its name, its one-line help, its arguments and its handler.

    ``configure`` adds the subcommand's arguments to its parser. ``run`` does
    the work, printing to ``console``, and returns the exit status; it raises
    :class:`CommandError` for a failure the user should see.
    """

    name: str
    help: str
    configure: Callable[[argparse.ArgumentParser], None]
    run: Callable[[argparse.Namespace, Console], int]
