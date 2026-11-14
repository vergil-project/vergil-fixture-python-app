"""``keys FILE``: list the top-level keys of a YAML mapping and their types."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from rich.table import Table
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("file", type=Path, help="the YAML file to read")


def _load(path: Path) -> dict[object, object]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CommandError(f"cannot read {path}: {exc.strerror}") from exc
    try:
        # Bytes, so YAML's own encoding detection applies and an undecodable
        # file is a YAMLError like any other malformed document.
        document = yaml.safe_load(data)
    except yaml.YAMLError as exc:
        raise CommandError(f"{path} is not valid YAML: {exc}") from exc
    if not isinstance(document, dict):
        raise CommandError(f"{path} does not hold a YAML mapping (found {type(document).__name__})")
    return document


def _run(args: argparse.Namespace, console: Console) -> int:
    path: Path = args.file
    document = _load(path)
    table = Table()
    table.add_column("Key")
    table.add_column("Type")
    for key, value in document.items():
        table.add_row(Text(str(key)), type(value).__name__)
    console.print(Text(str(path)))
    console.print(table)
    return 0


COMMAND = Command(
    name="keys",
    help="List the top-level keys of a YAML mapping and their types.",
    configure=_configure,
    run=_run,
)
