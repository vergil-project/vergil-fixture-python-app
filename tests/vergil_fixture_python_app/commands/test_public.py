"""The ``public`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_public_drops_the_local_label(run: Callable[..., Result]) -> None:
    result = run("public", "1.2.3+local.7", "2.0+ubuntu-1", "3.1")
    assert result.code == 0
    assert result.out == "1.2.3\n2.0\n3.1\n"
    assert result.err == ""


def test_public_keeps_every_other_part(run: Callable[..., Result]) -> None:
    result = run("public", "1!2.0rc1.post3.dev4+abc")
    assert result.out == "1!2.0rc1.post3.dev4\n"


def test_public_prints_the_normal_form(run: Callable[..., Result]) -> None:
    result = run("public", "V01.002-ALPHA1+X")
    assert result.out == "1.2a1\n"


def test_public_refuses_an_invalid_version_and_prints_nothing(run: Callable[..., Result]) -> None:
    result = run("public", "1.5", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_public_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("public")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
