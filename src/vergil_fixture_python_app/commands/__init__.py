"""The registered subcommands, in the order ``--help`` lists them.

To add a subcommand, write its module here, defining a ``COMMAND``, and add
it to :data:`COMMANDS`.
"""

from __future__ import annotations

from vergil_fixture_python_app.commands import (
    base,
    bump,
    compare,
    greet,
    keys,
    latest,
    local,
    match,
    normalize,
    public,
    sort,
)

COMMANDS = (
    greet.COMMAND,
    compare.COMMAND,
    keys.COMMAND,
    sort.COMMAND,
    normalize.COMMAND,
    latest.COMMAND,
    match.COMMAND,
    bump.COMMAND,
    base.COMMAND,
    public.COMMAND,
    local.COMMAND,
)
