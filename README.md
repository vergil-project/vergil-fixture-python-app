# vergil-fixture-python-app

This is a **Vergil test fixture** with no users: a small, real Python
command-line application that Vergil itself is tested against. It exercises
the Python `vrg-validate` gates, CI, the docs site, the dependency audit and
updates, and the tagged release of an application, each run for real through
Vergil's full cycle. The design is in
[`epics/1091-language-fixture-repos/spec.md`](https://github.com/vergil-project/.github/blob/develop/epics/1091-language-fixture-repos/spec.md).

## Table of Contents

- [Status](#status)
- [Overview](#overview)
- [Getting Started](#getting-started)
- [License](#license)

## Status

A test fixture. It is never published to a package registry.

## Overview

`vergil-fixture-python-app` has these subcommands:

- `greet NAME` prints `Hello, NAME`.
- `compare LEFT RIGHT` orders two versions by the PEP 440 rules.
- `keys FILE` lists the top-level keys of a YAML mapping and their types.
- `sort VERSION...` lists versions in PEP 440 order, one per line.
- `normalize VERSION...` prints the PEP 440 normal form of each version.
- `latest VERSION...` prints the newest version, optionally skipping pre-releases.
- `match SPECIFIER VERSION...` prints the versions a PEP 440 specifier allows.
- `bump PART VERSION` prints the next major, minor or micro release after a version.
- `base VERSION...` prints the base version (epoch and release) of each version.
- `public VERSION...` prints the public version (no local label) of each version.
- `local VERSION...` prints the local label (the part after `+`) of each version.
- `epoch VERSION...` prints the PEP 440 epoch (`0` when absent) of each version.

Its runtime dependencies are `rich`, `PyYAML` and `packaging`. Each fixture
run adds one small change, so a new subcommand is one module under
`src/vergil_fixture_python_app/commands/`, one entry in its `COMMANDS`
tuple, and its tests.

## Getting Started

See the [documentation](https://vergil-project.github.io/vergil-fixture-python-app/).
Validate with `vrg-container-run -- vrg-validate`.

## License

MIT — see [LICENSE](LICENSE).
