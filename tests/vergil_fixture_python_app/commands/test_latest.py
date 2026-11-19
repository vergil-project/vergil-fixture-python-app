"""The ``latest`` subcommand."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_latest_prints_the_newest_version(run: Callable[..., Result]) -> None:
    result = run("latest", "1.2.0", "1.10.0", "1.9.9")
    assert result.code == 0
    assert result.out == "1.10.0\n"
    assert result.err == ""


def test_latest_counts_a_pre_release_by_default(run: Callable[..., Result]) -> None:
    result = run("latest", "1.0", "2.0rc1")
    assert result.out == "2.0rc1\n"


@pytest.mark.parametrize("flag", ["-s", "--stable"])
def test_latest_stable_skips_pre_and_dev_releases(run: Callable[..., Result], flag: str) -> None:
    result = run("latest", flag, "1.0", "2.0rc1", "2.0.dev3", "1.5.post1")
    assert result.code == 0
    assert result.out == "1.5.post1\n"


def test_latest_prints_the_version_as_given(run: Callable[..., Result]) -> None:
    result = run("latest", "V2.0", "1.0")
    assert result.out == "V2.0\n"


def test_latest_prints_the_first_of_equal_versions(run: Callable[..., Result]) -> None:
    result = run("latest", "1.0.0", "1.0", "1")
    assert result.out == "1.0.0\n"


def test_latest_accepts_a_single_version(run: Callable[..., Result]) -> None:
    result = run("latest", "3.1")
    assert result.code == 0
    assert result.out == "3.1\n"


def test_latest_refuses_an_invalid_version(run: Callable[..., Result]) -> None:
    result = run("latest", "1.0", "banana")
    assert result.code == 1
    assert result.out == ""
    assert "not a valid version: 'banana'" in result.err


def test_latest_stable_refuses_when_every_version_is_a_pre_release(
    run: Callable[..., Result],
) -> None:
    result = run("latest", "--stable", "1.0a1", "1.0.dev1")
    assert result.code == 1
    assert result.out == ""
    assert "no stable version among those given" in result.err


def test_latest_needs_a_version(run: Callable[..., Result]) -> None:
    result = run("latest")
    assert result.code == 2
    assert "the following arguments are required: version" in result.err
