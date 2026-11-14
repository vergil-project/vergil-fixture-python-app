"""The ``compare`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("1.2.0", "1.10.0", "1.2.0 < 1.10.0"),
        ("2.0.0", "1.99.99", "2.0.0 > 1.99.99"),
        ("1.0", "1.0.0", "1.0 == 1.0.0"),
        ("1.0.0rc1", "1.0.0", "1.0.0rc1 < 1.0.0"),
    ],
)
def test_compare_orders_two_versions(
    run: Callable[..., Result], left: str, right: str, expected: str
) -> None:
    result = run("compare", left, right)
    assert result.code == 0
    assert result.out == f"{expected}\n"
    assert result.err == ""


@pytest.mark.parametrize(("left", "right"), [("banana", "1.0"), ("1.0", "banana")])
def test_compare_refuses_an_invalid_version(
    run: Callable[..., Result], left: str, right: str
) -> None:
    result = run("compare", left, right)
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_compare_needs_two_versions(run: Callable[..., Result]) -> None:
    result = run("compare", "1.0")
    assert result.code == 2
    assert "the following arguments are required: right" in result.err
