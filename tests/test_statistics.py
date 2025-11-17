"""Integration tests for summary statistics (-c option)."""

from __future__ import annotations

from strace_macos.__main__ import main
from tests.base import StraceTestCase


class TestStatistics(StraceTestCase):
    """Test -c option for syscall summary statistics."""

    def test_summary_statistics_table(self) -> None:
        """Test -c option produces summary statistics table."""
        output_file = self.temp_dir / "trace.txt"
        test_file = self.temp_dir / "test.txt"

        # Use spawn mode with test executable (avoids SIP issues with system binaries)
        exit_code = main(
            [
                "-o",
                str(output_file),
                "-c",
                str(self.test_executable),
                "--file-ops",
                str(test_file),
            ]
        )

        assert exit_code == 0, "strace should exit with code 0"

        # Verify summary table was generated
        assert output_file.exists(), "Output file should be created"
        content = output_file.read_text()

        assert len(content) > 0, "Output should not be empty"

        # Verify summary table headers
        assert "calls" in content, "Summary should contain 'calls' column"
        assert "syscall" in content, "Summary should contain 'syscall' column"

        # Verify some syscalls appear in summary
        assert "open" in content or "openat" in content, "Summary should contain open/openat"
        assert "write" in content, "Summary should contain write"
        assert "read" in content, "Summary should contain read"
        assert "close" in content, "Summary should contain close"


if __name__ == "__main__":
    import unittest

    unittest.main()
