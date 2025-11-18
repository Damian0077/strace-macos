"""Integration tests for attaching to running processes."""

from __future__ import annotations

import subprocess
import threading
import time
import unittest

from strace_macos.__main__ import main
from tests.base import StraceTestCase
from tests.fixtures import helpers


class TestAttach(StraceTestCase):
    """Test attaching to already-running processes."""

    def test_attach_to_file_operations(self) -> None:
        """Test attaching to a process performing file operations."""
        output_file = self.temp_dir / "trace.jsonl"

        # Start target process
        proc = subprocess.Popen(
            [
                str(self.test_executable),
                "--file-ops-loop",
                str(self.temp_dir / "test.txt"),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Wait for "READY" signal
            assert proc.stdout is not None
            line = proc.stdout.readline()
            assert line.strip() == b"READY", "Process should signal ready"

            # Attach and trace in background thread
            def trace_process() -> None:
                main(["--json", "-o", str(output_file), "-p", str(proc.pid)])

            trace_thread = threading.Thread(target=trace_process)
            trace_thread.daemon = True
            trace_thread.start()

            # Let it trace for a short time to collect syscalls
            time.sleep(2)

            # Terminate the target process
            proc.terminate()
            proc.wait(timeout=5)

            # Wait for trace thread to finish
            trace_thread.join(timeout=5)

            # Verify output
            assert output_file.exists(), "Output file should be created"

            syscalls = helpers.json_lines(output_file)
            assert len(syscalls) > 0, "Should capture syscalls"

            # Verify we captured file operations
            syscall_names = [sc["syscall"] for sc in syscalls]
            assert "open" in syscall_names or "openat" in syscall_names, (
                "Should capture open/openat syscall"
            )
        finally:
            # Ensure process is cleaned up
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_attach_to_network_operations(self) -> None:
        """Test attaching to a process performing network operations."""
        output_file = self.temp_dir / "trace.jsonl"

        # Start target process
        proc = subprocess.Popen(
            [str(self.test_executable), "--network-loop"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Wait for "READY" signal
            assert proc.stdout is not None
            line = proc.stdout.readline()
            assert line.strip() == b"READY", "Process should signal ready"

            # Attach and trace in background thread
            def trace_process() -> None:
                main(["--json", "-o", str(output_file), "-p", str(proc.pid)])

            trace_thread = threading.Thread(target=trace_process)
            trace_thread.daemon = True
            trace_thread.start()

            # Let it trace for a short time to collect syscalls
            time.sleep(2)

            # Terminate the target process
            proc.terminate()
            proc.wait(timeout=5)

            # Wait for trace thread to finish
            trace_thread.join(timeout=5)

            # Verify output
            assert output_file.exists(), "Output file should be created"

            syscalls = helpers.json_lines(output_file)
            syscall_names = [sc["syscall"] for sc in syscalls]

            # Verify network syscalls (--network-loop uses socketpair, not socket/connect)
            assert "socketpair" in syscall_names, "Should capture socketpair syscall"
            assert "sendto" in syscall_names, "Should capture sendto syscall"
            assert "shutdown" in syscall_names, "Should capture shutdown syscall"
        finally:
            # Ensure process is cleaned up
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_attach_to_long_running_process(self) -> None:
        """Test attaching to a long-running process and detaching cleanly."""
        output_file = self.temp_dir / "trace.jsonl"

        # Start long-running process
        proc = subprocess.Popen(
            [str(self.test_executable), "--long-running"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Wait for "READY" signal
            assert proc.stdout is not None
            line = proc.stdout.readline()
            assert line.strip() == b"READY", "Process should signal ready"

            # Attach in a thread so we can interrupt it
            def trace_process() -> None:
                main(["--json", "-o", str(output_file), "-p", str(proc.pid)])

            trace_thread = threading.Thread(target=trace_process)
            trace_thread.daemon = True
            trace_thread.start()

            # Let it trace for a short time
            time.sleep(2)

            # Terminate the target process
            proc.terminate()
            proc.wait(timeout=5)

            # Wait for trace thread to finish
            trace_thread.join(timeout=5)

            # Verify we captured some syscalls before termination
            assert output_file.exists(), "Output file should be created"

            syscalls = helpers.json_lines(output_file)
            assert len(syscalls) > 0, "Should capture syscalls from long-running process"
        finally:
            # Ensure process is cleaned up
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    def test_attach_to_nonexistent_pid(self) -> None:
        """Test that attaching to a non-existent PID fails gracefully."""
        output_file = self.temp_dir / "trace.jsonl"

        # Use a PID that definitely doesn't exist (very high number)
        nonexistent_pid = 999999

        # Should fail to attach
        exit_code = main(["--json", "-o", str(output_file), "-p", str(nonexistent_pid)])

        assert exit_code != 0, "Should fail when attaching to non-existent PID"


if __name__ == "__main__":
    import unittest

    unittest.main()
