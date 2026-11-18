"""The ``normalize`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("1.0.0", "1.0.0"),
        ("V1.0", "1.0"),
        ("1.0-alpha.1", "1.0a1"),
        ("1.0.0.RC2", "1.0.0rc2"),
        ("1.0-1", "1.0.post1"),
        ("1.0.dev", "1.0.dev0"),
        ("0!01.02", "1.2"),
        ("1!2.0", "1!2.0"),
        ("1.0+Ubuntu-1", "1.0+ubuntu.1"),
    ],
)
def test_normalize_prints_the_normal_form(
    run: Callable[..., Result], given: str, expected: str
) -> None:
    result = run("normalize", given)
    assert result.code == 0
    assert result.out == f"{expected}\n"
    assert result.err == ""


def test_normalize_keeps_the_order_given(run: Callable[..., Result]) -> None:
    result = run("normalize", "2.0-beta", "1.0", "1.0")
    assert result.code == 0
    assert result.out == "2.0b0\n1.0\n1.0\n"


def test_normalize_refuses_an_invalid_version_and_prints_nothing(
    run: Callable[..., Result],
) -> None:
    result = run("normalize", "1.0", "banana", "2.0")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_normalize_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("normalize")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
