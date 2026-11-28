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

## `normalize VERSION...`

Print the [PEP 440](https://peps.python.org/pep-0440/) normal form of one
or more versions, using `packaging`, one per line in the order given. The
normal form drops a leading `v` and a zero epoch, lowercases, and spells
pre-, post- and development releases and local labels the standard way.

```console
$ vergil-fixture-python-app normalize V1.0 1.0-alpha.1 1.0-1 1.0+Ubuntu-1
1.0
1.0a1
1.0.post1
1.0+ubuntu.1
```

A version that is not valid under PEP 440 fails, and nothing is printed.

## `latest [--stable] VERSION...`

Print the newest of one or more versions by the
[PEP 440](https://peps.python.org/pep-0440/) rules, using `packaging`,
printed as given. Of equal versions, such as `1.0` and `1.0.0`, the first
given is printed. `--stable` (`-s`) skips pre-releases and development
releases.

```console
$ vergil-fixture-python-app latest 1.2.0 1.10.0 2.0rc1
2.0rc1
$ vergil-fixture-python-app latest --stable 1.2.0 1.10.0 2.0rc1
1.10.0
```

A version that is not valid under PEP 440 fails, and so does `--stable`
when every version given is a pre-release or development release.

## `match SPECIFIER VERSION...`

Print the versions that a [PEP 440](https://peps.python.org/pep-0440/)
version specifier, such as `>=1.2,<2` or `~=1.4`, allows, using
`packaging`, one per line in the order given, each printed as given. A
pre-release or development release is judged by the specifier like any
other version.

```console
$ vergil-fixture-python-app match '>=1.2,<2' 1.0 1.10.0 2.0 1.2
1.10.0
1.2
```

A specifier or version that is not valid under PEP 440 fails, and nothing
is printed. So does a run in which no version matches.

## `bump PART VERSION`

Print the next `major`, `minor` or `micro` release after a
[PEP 440](https://peps.python.org/pep-0440/) version, using `packaging`.
The named release number goes up by one and the ones after it become `0`.
The result always has three release numbers: a shorter version is padded
with `0` and a longer one is cut to three. Any pre-release, post-release,
development or local part is dropped, and an epoch is kept.

```console
$ vergil-fixture-python-app bump minor 1.2.3
1.3.0
$ vergil-fixture-python-app bump micro 1.2
1.2.1
```

A version that is not valid under PEP 440 fails, and so does a part other
than `major`, `minor` or `micro`.

## `base VERSION...`

Print the base version of each of one or more
[PEP 440](https://peps.python.org/pep-0440/) versions, using `packaging`,
one per line in the order given. The base version is the epoch and the
release numbers only, in normal form: any pre-release, post-release,
development or local part is dropped. Unlike `bump`, the release numbers
are neither padded nor cut.

```console
$ vergil-fixture-python-app base 1.2.3rc1 2.0.post1 '1!3.1.dev4'
1.2.3
2.0
1!3.1
```

A version that is not valid under PEP 440 fails, and nothing is printed.

## `public VERSION...`

Print the public version of each of one or more
[PEP 440](https://peps.python.org/pep-0440/) versions, using `packaging`,
one per line in the order given. The public version is the version in
normal form without its local label (the part after `+`). Unlike `base`,
it keeps every other part: the epoch and any pre-release, post-release or
development part.

```console
$ vergil-fixture-python-app public 1.2.3+local.7 2.0rc1+abc 3.1
1.2.3
2.0rc1
3.1
```

A version that is not valid under PEP 440 fails, and nothing is printed.

## `local VERSION...`

Print the local label of each of one or more
[PEP 440](https://peps.python.org/pep-0440/) versions, using `packaging`,
one per line in the order given. The local label is the part after `+`, in
normal form: lower case, with `-` and `_` separators written as `.`, and
leading zeros dropped from a numeric segment. It is the part `public` drops.

```console
$ vergil-fixture-python-app local 1.2.3+local.7 2.0rc1+Ubuntu-1
local.7
ubuntu.1
```

A version that is not valid under PEP 440 fails, and so does a version with
no local label; either way nothing is printed.

## `epoch VERSION...`

Print the [PEP 440](https://peps.python.org/pep-0440/) epoch of each of one
or more versions, using `packaging`, one per line in the order given. The
epoch is the integer before `!`, and is `0` when the version has none.

```console
$ vergil-fixture-python-app epoch 1!2.0 3.1 2!0.1.dev4
1
0
2
```

A version that is not valid under PEP 440 fails, and nothing is printed.
