"""Compile test fixtures for strace-macos tests."""

from __future__ import annotations

import atexit
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Global state for lazy compilation
_test_executable_path: Path | None = None
_test_executable_tempdir: Path | None = None


def _cleanup_test_executable() -> None:
    """Clean up the test executable temp directory at exit."""
    global _test_executable_tempdir  # noqa: PLW0602
    if _test_executable_tempdir and _test_executable_tempdir.exists():
        shutil.rmtree(_test_executable_tempdir, ignore_errors=True)


def get_test_executable() -> Path:
    """Get the compiled test executable, compiling it lazily if needed.

    The executable is compiled once and reused for all tests in the test suite.
    It's placed in a temporary directory that is cleaned up at exit.

    Returns:
        Path to the compiled test executable

    Raises:
        RuntimeError: If compilation fails
    """
    global _test_executable_path, _test_executable_tempdir  # noqa: PLW0603

    # Return cached path if already compiled
    if _test_executable_path is not None:
        return _test_executable_path

    # Create temp directory for the test suite
    _test_executable_tempdir = Path(tempfile.mkdtemp(prefix="strace_test_fixture_"))
    atexit.register(_cleanup_test_executable)

    # Compile
    fixtures_dir = Path(__file__).parent
    source_file = fixtures_dir / "test_executable.c"
    output_file = _test_executable_tempdir / "test_executable"

    # Use $CC environment variable with fallback to clang
    cc = os.environ.get("CC", "clang")

    result = subprocess.run(
        [cc, "-o", str(output_file), str(source_file)],
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        msg = f"Failed to compile test executable with {cc}:\n{result.stderr}"
        raise RuntimeError(msg)

    _test_executable_path = output_file
    return output_file
