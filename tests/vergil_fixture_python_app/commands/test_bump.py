"""The ``bump`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


@pytest.mark.parametrize(
    ("part", "version", "expected"),
    [
        ("major", "1.2.3", "2.0.0"),
        ("minor", "1.2.3", "1.3.0"),
        ("micro", "1.2.3", "1.2.4"),
        ("minor", "1.2", "1.3.0"),
        ("micro", "3", "3.0.1"),
        ("micro", "1.2.3.4", "1.2.4"),
        ("minor", "v1.9.0rc1", "1.10.0"),
        ("micro", "1.2.3.post1+local.2", "1.2.4"),
        ("major", "1!2.0", "1!3.0.0"),
    ],
)
def test_bump_prints_the_next_release(
    run: Callable[..., Result], part: str, version: str, expected: str
) -> None:
    result = run("bump", part, version)
    assert result.code == 0
    assert result.out == f"{expected}\n"
    assert result.err == ""


def test_bump_refuses_an_invalid_version(run: Callable[..., Result]) -> None:
    result = run("bump", "minor", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_bump_refuses_an_unknown_part(run: Callable[..., Result]) -> None:
    result = run("bump", "patch", "1.2.3")
    assert result.code == 2
    assert "invalid choice: 'patch'" in result.err
