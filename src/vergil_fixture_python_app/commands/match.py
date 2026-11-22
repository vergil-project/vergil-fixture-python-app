"""``match SPECIFIER VERSION...``: print the versions a specifier allows."""

from __future__ import annotations

from typing import TYPE_CHECKING

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version
from rich.text import Text

from vergil_fixture_python_app.command import Command, CommandError

if TYPE_CHECKING:
    import argparse

    from rich.console import Console


def _configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("specifier", help="a version specifier, such as '>=1.0,<2'")
    parser.add_argument("versions", nargs="+", metavar="version", help="a version to check")


def _run(args: argparse.Namespace, console: Console) -> int:
    spec_text: str = args.specifier
    texts: list[str] = args.versions
    try:
        specifier = SpecifierSet(spec_text)
    except InvalidSpecifier as exc:
        raise CommandError(f"not a valid specifier: {spec_text!r}") from exc
    # Parse every version before printing any, so a bad one prints nothing.
    parsed: list[tuple[Version, str]] = []
    for text in texts:
        try:
            parsed.append((Version(text), text))
        except InvalidVersion as exc:
            raise CommandError(f"not a valid version: {text!r}") from exc
    # Pre-releases are judged by the specifier alone, like any other version.
    matches = [text for version, text in parsed if specifier.contains(version, prereleases=True)]
    if not matches:
        raise CommandError(f"no version matches {spec_text!r}")
    for text in matches:
        console.print(Text(text))
    return 0


COMMAND = Command(
    name="match",
    help="Print the versions a PEP 440 specifier allows.",
    configure=_configure,
    run=_run,
)
