# Usage

```text
vergil-fixture-python-app <command> [arguments]
```

`vergil-fixture-python-app --help` lists the commands, and
`vergil-fixture-python-app <command> --help` describes one.

## Exit status

| Status | Meaning |
|---|---|
| 0 | The command succeeded. |
| 1 | The command failed. The reason is on stderr, after `vergil-fixture-python-app:`. |
| 2 | The command line was not valid. |

## `greet NAME`

Print a greeting. The name is printed exactly as given.

```console
$ vergil-fixture-python-app greet Ada
Hello, Ada
```

An empty or whitespace-only name fails.

## `compare LEFT RIGHT`

Order two versions by the [PEP 440](https://peps.python.org/pep-0440/)
rules, using `packaging`. It prints the two versions as given, with `<`,
`>` or `==` between them.

```console
$ vergil-fixture-python-app compare 1.2.0 1.10.0
1.2.0 < 1.10.0
$ vergil-fixture-python-app compare 1.0 1.0.0
1.0 == 1.0.0
```

A version that is not valid under PEP 440 fails.

## `keys FILE`

Read a YAML file with `PyYAML` and list its top-level keys, in file order,
with the type of each value, as a `rich` table under the file's path.

```console
$ vergil-fixture-python-app keys config.yaml
config.yaml
┏━━━━━━━━━┳━━━━━━┓
┃ Key     ┃ Type ┃
┡━━━━━━━━━╇━━━━━━┩
│ name    │ str  │
│ version │ int  │
└─────────┴──────┘
```

A file that cannot be read, is not valid YAML, or does not hold a mapping
fails.

## `sort [--reverse] VERSION...`

List one or more versions in [PEP 440](https://peps.python.org/pep-0440/)
order, oldest first, one per line, each printed as given. `--reverse` (`-r`)
lists the newest first. Equal versions, such as `1.0` and `1.0.0`, keep the
order they were given in.

```console
$ vergil-fixture-python-app sort 1.10.0 1.2.0 1.0.0rc1
1.0.0rc1
1.2.0
1.10.0
$ vergil-fixture-python-app sort --reverse 1.10.0 1.2.0
1.10.0
1.2.0
```

A version that is not valid under PEP 440 fails, and nothing is printed.
