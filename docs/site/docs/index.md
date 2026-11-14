# vergil-fixture-python-app

This is a **Vergil test fixture**. It has no users. It is a small, real
Python command-line application that Vergil itself is tested against.

## What it is for

The fixture is managed exactly like a real Vergil Python application, with
every fleet automation enabled. Each fixture run drives it through Vergil's
full cycle for real: a change, a pull request, CI, a merge, a release, and a
validation of the result. A run that goes red shows a Vergil regression
before a real repository meets it.

It exercises:

- the Python `vrg-validate` gates: ruff, mypy, ty, pytest at 100% branch
  coverage, pip-audit and the license check;
- the CI workflows, the docs site build and its publishing to GitHub Pages;
- the dependency audit and updates, through three real runtime
  dependencies: `rich`, `PyYAML` and `packaging`;
- the tagged release of an application.

Nothing it does reaches a package registry.

The design is in the epic's spec,
[Language fixture repos](https://github.com/vergil-project/.github/blob/develop/epics/1091-language-fixture-repos/spec.md).

## The program

`vergil-fixture-python-app` has three subcommands. See [Usage](usage.md).

The program grows by one small change per fixture run, so it is built to
take one more subcommand without restructuring: a subcommand is one module
under `src/vergil_fixture_python_app/commands/`, one entry in its
`COMMANDS` tuple, and its tests.
