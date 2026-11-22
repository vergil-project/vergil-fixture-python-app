"""The ``match`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_match_prints_the_versions_the_specifier_allows(run: Callable[..., Result]) -> None:
    result = run("match", ">=1.2,<2", "1.0", "1.10.0", "2.0", "1.2")
    assert result.code == 0
    assert result.out == "1.10.0\n1.2\n"
    assert result.err == ""


def test_match_prints_each_version_as_given(run: Callable[..., Result]) -> None:
    result = run("match", "==1.0", "V1.0", "1.0.0", "1.1")
    assert result.out == "V1.0\n1.0.0\n"


def test_match_judges_a_pre_release_by_the_specifier_alone(run: Callable[..., Result]) -> None:
    result = run("match", ">=1.0", "2.0rc1", "0.9", "1.5.dev2")
    assert result.code == 0
    assert result.out == "2.0rc1\n1.5.dev2\n"


def test_match_supports_the_compatible_release_operator(run: Callable[..., Result]) -> None:
    result = run("match", "~=1.4", "1.3", "1.4", "1.9.2", "2.0")
    assert result.out == "1.4\n1.9.2\n"


def test_match_refuses_an_invalid_specifier(run: Callable[..., Result]) -> None:
    result = run("match", "about 1.0", "1.0")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid specifier: 'about 1.0'" in result.err


def test_match_refuses_an_invalid_version_and_prints_nothing(run: Callable[..., Result]) -> None:
    result = run("match", ">=1.0", "1.5", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_match_fails_when_no_version_matches(run: Callable[..., Result]) -> None:
    result = run("match", ">=3", "1.0", "2.9")
    assert result.code == 1
    assert result.out == ""
    assert "no version matches '>=3'" in result.err


def test_match_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("match", ">=1.0")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
