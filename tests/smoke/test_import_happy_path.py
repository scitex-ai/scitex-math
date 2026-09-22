"""Smoke: installed package rounds to the requested parity (PS-211).

Subprocess-driven (``sys.executable <tmp script>``) so this proves the
installed distribution resolves — an in-process import would not.
Hermetic: no network, no credentials, no writes outside tmp dirs.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.smoke

_PROBE = (
    "from scitex_math import to_even, to_odd\n"
    "print(to_even(5), to_odd(6))\n"
)


def test_subprocess_parity_helpers_round_down_correctly(tmp_path: Path) -> None:
    # Arrange
    probe = tmp_path / "probe_math.py"
    probe.write_text(_PROBE)
    argv = [sys.executable, str(probe)]

    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=30)

    # Assert
    assert (completed.returncode, completed.stdout.split()) == (0, ["4", "5"])
