"""Integration tests for output formats (JSON and text)."""

from __future__ import annotations

import re

from strace_macos.__main__ import main
from tests.base import StraceTestCase
from tests.fixtures import helpers


class TestOutputFormats(StraceTestCase):
    """Test JSON and text output format generation."""

    def test_json_output_format(self) -> None:
        """Test JSON Lines output format (primary format)."""
        output_file = self.temp_dir / "trace.jsonl"
        test_file = self.temp_dir / "test.txt"

        # Trace test executable with JSON output (spawn mode)
        exit_code = main(
            [
                "--json",
                "-o",
                str(output_file),
                str(self.test_executable),
                "--file-ops",
                str(test_file),
            ]
        )

        assert exit_code == 0, "strace should exit with code 0"
        assert output_file.exists(), "Output file should be created"

        # Verify JSON structure
        syscalls = helpers.json_lines(output_file)
        assert len(syscalls) > 0, "Should capture syscalls"

        # Verify each syscall has required JSON fields
        for sc in syscalls:
            assert helpers.verify_json_syscall_structure(sc), (
                f"Invalid JSON structure for syscall: {sc}"
            )
            # Verify field types
            assert isinstance(sc["syscall"], str), "syscall name should be string"
            assert isinstance(sc["args"], list), "args should be list"
            assert isinstance(sc["pid"], int), "pid should be int"
            assert isinstance(sc["timestamp"], (int, float)), "timestamp should be numeric"

        # Check that arguments are not all placeholders ("?")
        # The test program always does file operations, so we should always see open calls
        open_calls = [sc for sc in syscalls if sc["syscall"] in ("open", "openat")]
        assert len(open_calls) > 0, (
            "Should capture at least one open/openat syscall from file operations"
        )

        # Check that at least one open/openat call has the test file path
        expected_basename = test_file.name
        found_test_file = False

        for sc in open_calls:
            if len(sc["args"]) == 0:
                continue

            # First arg (or second for openat) should be the path string
            path_arg_idx = 1 if sc["syscall"] == "openat" else 0
            if len(sc["args"]) <= path_arg_idx:
                continue

            path_arg = sc["args"][path_arg_idx]
            # Check if this open call is for our test file
            if expected_basename in str(path_arg):
                found_test_file = True
                break

        assert found_test_file, (
            f"Should find at least one open/openat call with file '{expected_basename}' in {len(open_calls)} open calls"
        )

        # Check that return values are captured
        # close() should return 0 on success
        close_calls = [sc for sc in syscalls if sc["syscall"] == "close"]
        if close_calls:
            assert close_calls[0]["return"] == 0, (
                f"close() should return 0, got: {close_calls[0]['return']}"
            )

    def test_text_output_format(self) -> None:
        """Test human-readable text output format (strace-compatible)."""
        output_file = self.temp_dir / "trace.txt"
        test_file = self.temp_dir / "test.txt"

        # Trace WITHOUT --json flag (text is default) using spawn mode
        exit_code = main(
            [
                "-o",
                str(output_file),
                str(self.test_executable),
                "--file-ops",
                str(test_file),
            ]
        )

        assert exit_code == 0, "strace should exit with code 0"
        assert output_file.exists(), "Output file should be created"
        content = output_file.read_text()

        assert len(content) > 0, "Output should not be empty"

        # Verify strace-like format
        assert helpers.verify_text_output_format(content), (
            "Output should match strace format (syscall(...) = retval)"
        )

        # Check for expected syscalls in text
        assert "open(" in content or "openat(" in content, "Should contain open/openat syscall"
        assert "write(" in content, "Should contain write syscall"
        assert "read(" in content, "Should contain read syscall"
        assert "close(" in content, "Should contain close syscall"

        # Check that path arguments are properly parsed (not "?" placeholders)
        # Parse open/openat calls and verify they contain the actual path
        # Pattern matches: open("path", ...) or openat(fd, "path", ...)
        open_pattern = r"open(?:at)?\([^)]+\)"
        open_calls = re.findall(open_pattern, content)

        assert len(open_calls) > 0, "Should find at least one open/openat call in text output"

        # Check that at least one open call has the actual test file name
        # The test program is called with the full path as argv[2]
        # Check basename to avoid /var vs /private/var issues on macOS
        expected_basename = test_file.name
        found_path = False
        for call in open_calls:
            if expected_basename in call:
                found_path = True
                break

        assert found_path, (
            f"Should find open/openat call with file '{expected_basename}' in: {open_calls}"
        )

        # Check that return values are captured
        # close() should return 0 on success
        close_pattern = r"close\([^)]+\) = (\S+)"
        close_matches = re.findall(close_pattern, content)
        if close_matches:
            assert close_matches[0] == "0", f"close() should return 0, got: {close_matches[0]}"


if __name__ == "__main__":
    import unittest

    unittest.main()
