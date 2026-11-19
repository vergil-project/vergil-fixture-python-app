"""The registered subcommands, in the order ``--help`` lists them.

To add a subcommand, write its module here, defining a ``COMMAND``, and add
it to :data:`COMMANDS`.
"""

from __future__ import annotations

from vergil_fixture_python_app.commands import compare, greet, keys, latest, normalize, sort

COMMANDS = (
    greet.COMMAND,
    compare.COMMAND,
    keys.COMMAND,
    sort.COMMAND,
    normalize.COMMAND,
    latest.COMMAND,
)
