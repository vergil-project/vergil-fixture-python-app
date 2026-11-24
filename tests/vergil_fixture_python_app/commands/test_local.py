"""The ``local`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_local_prints_the_local_label(run: Callable[..., Result]) -> None:
    result = run("local", "1.2.3+local.7", "2.0rc1+abc")
    assert result.code == 0
    assert result.out == "local.7\nabc\n"
    assert result.err == ""


def test_local_prints_the_normal_form(run: Callable[..., Result]) -> None:
    result = run("local", "1.0+Ubuntu-1_LTS", "2.0+007")
    assert result.out == "ubuntu.1.lts\n7\n"


def test_local_refuses_a_version_without_a_label_and_prints_nothing(
    run: Callable[..., Result],
) -> None:
    result = run("local", "1.0+abc", "3.1")
    assert result.code == 1
    assert result.out == ""
    assert "no local label: '3.1'" in result.err


def test_local_refuses_an_invalid_version_and_prints_nothing(run: Callable[..., Result]) -> None:
    result = run("local", "1.5+abc", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_local_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("local")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
