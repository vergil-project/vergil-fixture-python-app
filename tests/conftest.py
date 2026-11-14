"""Shared test helpers: run the CLI in-process and capture what it printed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from vergil_fixture_python_app.cli import main

if TYPE_CHECKING:
    from collections.abc import Callable

# Environment variables that change how rich renders. They are cleared so
# every test sees plain, uncoloured, 80-column output wherever it runs.
_RICH_ENV = ("FORCE_COLOR", "NO_COLOR", "TTY_COMPATIBLE", "TTY_INTERACTIVE", "COLUMNS", "LINES")


@dataclass(frozen=True)
class Result:
    """One CLI run: its exit status and what it wrote to stdout and stderr."""

    code: int
    out: str
    err: str


@pytest.fixture(autouse=True)
def _plain_rich(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _RICH_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def run(capsys: pytest.CaptureFixture[str]) -> Callable[..., Result]:
    """Run the CLI with the given arguments and return a :class:`Result`.

    An ``argparse`` exit (``SystemExit``) is returned as a result too, so a
    test can check the usage error's status and message the same way.
    """

    def _run(*argv: str) -> Result:
        try:
            code = main(list(argv))
        except SystemExit as exc:
            assert isinstance(exc.code, int)
            code = exc.code
        captured = capsys.readouterr()
        return Result(code=code, out=captured.out, err=captured.err)

    return _run
