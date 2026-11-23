"""The CLI shell: subcommand dispatch, usage errors and error reporting."""

from __future__ import annotations

from typing import TYPE_CHECKING

from vergil_fixture_python_app.cli import PROG, build_parser
from vergil_fixture_python_app.commands import COMMANDS

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests.conftest import Result


def test_every_command_is_registered_once() -> None:
    names = [command.name for command in COMMANDS]
    assert names == [
        "greet",
        "compare",
        "keys",
        "sort",
        "normalize",
        "latest",
        "match",
        "bump",
        "base",
        "public",
    ]
    assert len(set(names)) == len(names)


def test_help_lists_every_command(run: Callable[..., Result]) -> None:
    result = run("--help")
    assert result.code == 0
    assert result.out.startswith(f"usage: {PROG} ")
    for command in COMMANDS:
        assert command.name in result.out
        assert command.help in result.out


def test_no_command_is_a_usage_error(run: Callable[..., Result]) -> None:
    result = run()
    assert result.code == 2
    assert "the following arguments are required: <command>" in result.err
    assert result.out == ""


def test_unknown_command_is_a_usage_error(run: Callable[..., Result]) -> None:
    result = run("frobnicate")
    assert result.code == 2
    assert "invalid choice: 'frobnicate'" in result.err


def test_a_command_error_is_reported_with_the_program_name(run: Callable[..., Result]) -> None:
    result = run("greet", "")
    assert result.code == 1
    assert result.out == ""
    assert result.err == f"{PROG}: the name must not be empty\n"


def test_build_parser_binds_each_command_to_its_handler() -> None:
    parser = build_parser()
    args = parser.parse_args(["greet", "Ada"])
    assert args.handler is COMMANDS[0].run
