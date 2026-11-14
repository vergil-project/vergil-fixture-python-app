# Getting Started

The fixture is never published to a package registry. Run it from a clone:

```bash
git clone https://github.com/vergil-project/vergil-fixture-python-app.git
cd vergil-fixture-python-app
uv sync
uv run vergil-fixture-python-app greet Ada
```

Or install it as a tool straight from the repository:

```bash
uv tool install git+https://github.com/vergil-project/vergil-fixture-python-app
vergil-fixture-python-app --help
```

## Validation

As in every Vergil repository, validation is one command, run in the
project's dev container:

```bash
vrg-container-run -- vrg-validate
```
