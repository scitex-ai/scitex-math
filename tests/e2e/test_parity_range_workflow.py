"""E2E: parity rounding matches an independent reference over a range (PS-212).

The full story — a subprocess maps ``to_even`` / ``to_odd`` over
``range(-6, 7)`` and the outputs equal an independent round-down
reference computed here (``n - 1`` for the wrong parity, ``n``
otherwise — exact for integers). Real code paths, real filesystem, no
network. Gated on ``RUN_E2E=1`` (skipped by default).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.environ.get("RUN_E2E") != "1",
        reason="e2e: set RUN_E2E=1 to run end-to-end workflows",
    ),
]

_PROBE = (
    "from scitex_math import to_even, to_odd\n"
    "print([to_even(i) for i in range(-6, 7)])\n"
    "print([to_odd(i) for i in range(-6, 7)])\n"
)


def test_parity_rounding_matches_reference_over_range(tmp_path: Path) -> None:
    # Arrange
    probe = tmp_path / "probe_e2e.py"
    probe.write_text(_PROBE)
    argv = [sys.executable, str(probe)]
    span = range(-6, 7)
    expected = [
        str([i if i % 2 == 0 else i - 1 for i in span]),
        str([i if i % 2 == 1 else i - 1 for i in span]),
    ]

    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=60)

    # Assert
    assert (completed.returncode, completed.stdout.splitlines()) == (0, expected)
