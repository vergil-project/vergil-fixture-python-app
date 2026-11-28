"""The ``epoch`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_epoch_prints_the_epoch(run: Callable[..., Result]) -> None:
    result = run("epoch", "1!2.0", "3.1")
    assert result.code == 0
    assert result.out == "1\n0\n"
    assert result.err == ""


def test_epoch_is_zero_when_absent(run: Callable[..., Result]) -> None:
    result = run("epoch", "1.2.3", "2.0rc1+abc")
    assert result.out == "0\n0\n"


def test_epoch_prints_each_version_in_the_order_given(run: Callable[..., Result]) -> None:
    result = run("epoch", "2!1.0", "0!5.0", "10!0.1.dev4")
    assert result.out == "2\n0\n10\n"


def test_epoch_refuses_an_invalid_version_and_prints_nothing(run: Callable[..., Result]) -> None:
    result = run("epoch", "1!2.0", "banana", "3.1")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_epoch_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("epoch")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
