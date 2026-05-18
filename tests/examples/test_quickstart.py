"""Compile-only stub for examples/quickstart.py (PS303)."""

import subprocess
import sys
from pathlib import Path

QUICKSTART = Path(__file__).parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_file_exists_on_disk():
    # Arrange
    target = QUICKSTART
    # Act
    found = target.is_file()
    # Assert
    assert found, f"missing {target}"


def test_quickstart_example_compiles_without_syntax_error():
    # Arrange
    cmd = [sys.executable, "-m", "py_compile", str(QUICKSTART)]
    # Act
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Assert
    assert result.returncode == 0, f"py_compile failed: {result.stderr}"
