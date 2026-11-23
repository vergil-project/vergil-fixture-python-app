"""The ``base`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_base_drops_every_part_after_the_release(run: Callable[..., Result]) -> None:
    result = run("base", "1.2.3rc1", "2.0.post1", "3.1.dev4", "4.0+local.7")
    assert result.code == 0
    assert result.out == "1.2.3\n2.0\n3.1\n4.0\n"
    assert result.err == ""


def test_base_keeps_the_epoch(run: Callable[..., Result]) -> None:
    result = run("base", "1!2.0a1")
    assert result.out == "1!2.0\n"


def test_base_prints_the_normal_form_of_the_release(run: Callable[..., Result]) -> None:
    result = run("base", "V01.002", "1.0.0")
    assert result.out == "1.2\n1.0.0\n"


def test_base_refuses_an_invalid_version_and_prints_nothing(run: Callable[..., Result]) -> None:
    result = run("base", "1.5", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_base_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("base")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
