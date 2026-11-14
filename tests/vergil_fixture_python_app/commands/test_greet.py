"""The ``greet`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_greet_says_hello(run: Callable[..., Result]) -> None:
    result = run("greet", "Ada")
    assert result.code == 0
    assert result.out == "Hello, Ada\n"
    assert result.err == ""


def test_greet_prints_the_name_literally(run: Callable[..., Result]) -> None:
    # rich markup in the name is text, not styling.
    result = run("greet", "[bold]Ada[/bold]")
    assert result.code == 0
    assert result.out == "Hello, [bold]Ada[/bold]\n"


def test_greet_does_not_wrap_a_long_name(run: Callable[..., Result]) -> None:
    name = "A" * 200
    result = run("greet", name)
    assert result.out == f"Hello, {name}\n"


@pytest.mark.parametrize("name", ["", "   "])
def test_greet_refuses_an_empty_name(run: Callable[..., Result], name: str) -> None:
    result = run("greet", name)
    assert result.code == 1
    assert result.out == ""
    assert "the name must not be empty" in result.err


def test_greet_needs_a_name(run: Callable[..., Result]) -> None:
    result = run("greet")
    assert result.code == 2
    assert "the following arguments are required: name" in result.err
