"""The ``keys`` subcommand."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from tests.conftest import Result


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def _rows(out: str) -> list[list[str]]:
    """The words on each output line, with the table's box drawing dropped."""
    return [re.findall(r"[^\s─-╿]+", line) for line in out.splitlines()]


def test_keys_lists_each_top_level_key_and_its_type(
    run: Callable[..., Result], tmp_path: Path
) -> None:
    path = _write(tmp_path, "name: fixture\nversion: 3\ntags: [a, b]\nnested:\n  inner: true\n")
    result = run("keys", str(path))
    assert result.code == 0
    assert result.err == ""
    rows = _rows(result.out)
    assert rows[0] == [str(path)]
    assert [row for row in rows if row] == [
        [str(path)],
        ["Key", "Type"],
        ["name", "str"],
        ["version", "int"],
        ["tags", "list"],
        ["nested", "dict"],
    ]


def test_keys_keeps_the_file_order(run: Callable[..., Result], tmp_path: Path) -> None:
    path = _write(tmp_path, "zebra: 1\napple: 2\n")
    rows = _rows(run("keys", str(path)).out)
    assert rows.index(["zebra", "int"]) < rows.index(["apple", "int"])


def test_keys_shows_a_non_string_key_as_text(run: Callable[..., Result], tmp_path: Path) -> None:
    path = _write(tmp_path, "1: one\n")
    assert ["1", "str"] in _rows(run("keys", str(path)).out)


def test_keys_prints_markup_in_a_key_literally(run: Callable[..., Result], tmp_path: Path) -> None:
    path = _write(tmp_path, "'[bold]k[/bold]': 1\n")
    assert ["[bold]k[/bold]", "int"] in _rows(run("keys", str(path)).out)


def test_keys_refuses_a_missing_file(run: Callable[..., Result], tmp_path: Path) -> None:
    path = tmp_path / "absent.yaml"
    result = run("keys", str(path))
    assert result.code == 1
    assert result.out == ""
    assert f"cannot read {path}: No such file or directory" in result.err


def test_keys_refuses_invalid_yaml(run: Callable[..., Result], tmp_path: Path) -> None:
    path = _write(tmp_path, "a: [unclosed\n")
    result = run("keys", str(path))
    assert result.code == 1
    assert result.out == ""
    assert f"{path} is not valid YAML" in result.err


def test_keys_refuses_a_file_that_is_not_text(run: Callable[..., Result], tmp_path: Path) -> None:
    path = tmp_path / "binary.yaml"
    path.write_bytes(b"a: \xff\xfe\x00\n")
    result = run("keys", str(path))
    assert result.code == 1
    assert result.out == ""
    assert f"{path} is not valid YAML" in result.err


def test_keys_refuses_a_directory(run: Callable[..., Result], tmp_path: Path) -> None:
    result = run("keys", str(tmp_path))
    assert result.code == 1
    assert f"cannot read {tmp_path}: Is a directory" in result.err


def test_keys_refuses_a_document_that_is_not_a_mapping(
    run: Callable[..., Result], tmp_path: Path
) -> None:
    path = _write(tmp_path, "- a\n- b\n")
    result = run("keys", str(path))
    assert result.code == 1
    assert result.out == ""
    assert f"{path} does not hold a YAML mapping (found list)" in result.err


def test_keys_refuses_an_empty_file(run: Callable[..., Result], tmp_path: Path) -> None:
    path = _write(tmp_path, "")
    result = run("keys", str(path))
    assert result.code == 1
    assert f"{path} does not hold a YAML mapping (found NoneType)" in result.err
