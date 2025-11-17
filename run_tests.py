#!/usr/bin/python3
"""Test runner for strace-macos.

This script runs all tests from the package root directory so that
imports can find the strace_macos module.

IMPORTANT: Must be run with /usr/bin/python3 (macOS system Python)
because strace-macos depends on LLDB, which only works with system Python.

Usage:
    /usr/bin/python3 run_tests.py              # Run all tests
    /usr/bin/python3 run_tests.py -v           # Verbose output
"""

from __future__ import annotations

import sys
import unittest

if __name__ == "__main__":
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2 if "-v" in sys.argv else 1)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
