"""``latest VERSION...``: print the newest of the versions given."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to consider")
    parser.add_argument(
        "-s",
        "--stable",
        action="store_true",
        help="skip pre-releases and development releases",
    )


def _run(args: argparse.Namespace, console: Console) -> int:
    texts: list[str] = args.versions
    stable: bool = args.stable
    best: tuple[Version, str] | None = None
    for text in texts:
        try:
            version = Version(text)
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
        if stable and version.is_prerelease:
            continue
        # Strictly newer only, so the first of equal versions is the one printed.
        if best is None or version > best[0]:
            best = (version, text)
    if best is None:
        raise CommandError("no stable version among those given")
    console.print(Text(best[1]))
    return 0


COMMAND = Command(
    name="latest",
    help="Print the newest of the versions given, as given.",
    configure=_configure,
    run=_run,
)
