"""The ``sort`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_sort_lists_versions_oldest_first(run: Callable[..., Result]) -> None:
    result = run("sort", "1.10.0", "1.2.0", "1.0.0rc1", "2.0", "1.0.0")
    assert result.code == 0
    assert result.out == "1.0.0rc1\n1.0.0\n1.2.0\n1.10.0\n2.0\n"
    assert result.err == ""


@pytest.mark.parametrize("flag", ["-r", "--reverse"])
def test_sort_reverse_lists_the_newest_first(run: Callable[..., Result], flag: str) -> None:
    result = run("sort", flag, "1.2.0", "1.10.0", "1.0.0")
    assert result.code == 0
    assert result.out == "1.10.0\n1.2.0\n1.0.0\n"


def test_sort_prints_each_version_as_given(run: Callable[..., Result]) -> None:
    result = run("sort", "V1.0", "0.9.post1")
    assert result.out == "0.9.post1\nV1.0\n"


@pytest.mark.parametrize("reverse", [(), ("--reverse",)])
def test_sort_keeps_equal_versions_in_the_order_given(
    run: Callable[..., Result], reverse: tuple[str, ...]
) -> None:
    result = run("sort", *reverse, "1.0.0", "1.0", "1")
    assert result.out == "1.0.0\n1.0\n1\n"


def test_sort_accepts_a_single_version(run: Callable[..., Result]) -> None:
    result = run("sort", "3.1")
    assert result.code == 0
    assert result.out == "3.1\n"


def test_sort_refuses_an_invalid_version(run: Callable[..., Result]) -> None:
    result = run("sort", "1.0", "banana", "2.0")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_sort_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("sort")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
