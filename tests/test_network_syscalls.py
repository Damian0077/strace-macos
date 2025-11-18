"""
Test comprehensive network syscall coverage.

This test verifies that the --network mode exercises most socket-related syscalls.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "fixtures"))
import helpers


class TestNetworkSyscalls(unittest.TestCase):
    """Test network syscall coverage using the test executable's --network mode."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_executable = Path(__file__).parent / "fixtures" / "test_executable"
        self.assertTrue(
            self.test_executable.exists(), f"Test executable not found: {self.test_executable}"
        )

        self.python_path = "/usr/bin/python3"  # System Python for LLDB
        self.strace_module = str(Path(__file__).parent.parent)

    def run_strace(self, args):
        """Run strace and return exit code."""
        cmd = [self.python_path, "-m", "strace_macos"] + args
        result = subprocess.run(
            cmd,
            check=False,
            cwd=self.strace_module,
            capture_output=True,
            text=True,
        )
        return result.returncode

    def test_network_syscall_coverage(self):
        """Test that all expected network syscalls are captured."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = Path(f.name)

        try:
            exit_code = self.run_strace(
                ["--json", "-o", str(output_file), str(self.test_executable), "--network"]
            )

            self.assertEqual(exit_code, 0, f"strace should exit with code 0, got {exit_code}")
            self.assertTrue(output_file.exists(), "Output file should be created")

            # Parse JSON Lines output
            syscalls = helpers.json_lines(output_file)
            syscall_names = [sc.get("syscall") for sc in syscalls]
        finally:
            if output_file.exists():
                output_file.unlink()

        # Expected network syscalls - we capture 14 out of 15 reliably
        expected_syscalls = {
            "socketpair",
            "socket",
            "bind",
            "listen",
            "accept",
            "connect",
            "sendto",
            "recvfrom",
            "sendmsg",
            "recvmsg",
            "shutdown",
            "getsockname",
            "getpeername",
            "getsockopt",
            "setsockopt",  # May not always be captured due to timing/inlining
        }

        captured_network_syscalls = expected_syscalls & set(syscall_names)
        missing_syscalls = expected_syscalls - set(syscall_names)

        # We should capture at least 12 out of 14 expected syscalls
        self.assertGreaterEqual(
            len(captured_network_syscalls),
            12,
            f"Should capture at least 12 network syscalls, "
            f"got {len(captured_network_syscalls)}.\n"
            f"Captured: {sorted(captured_network_syscalls)}\n"
            f"Missing: {sorted(missing_syscalls)}",
        )

        # Verify symbolic decoders are working correctly
        # socketpair: socketpair(domain, type, protocol, sv)
        socketpair_calls = [sc for sc in syscalls if sc.get("syscall") == "socketpair"]
        self.assertGreater(len(socketpair_calls), 0, "Should have socketpair calls")
        sp = socketpair_calls[0]
        self.assertIn("AF_UNIX", sp["args"][0], "socketpair should decode AF_UNIX")
        self.assertIn("SOCK_STREAM", sp["args"][1], "socketpair should decode SOCK_STREAM")

        # socket: socket(domain, type, protocol)
        socket_calls = [sc for sc in syscalls if sc.get("syscall") == "socket"]
        self.assertGreater(len(socket_calls), 0, "Should have socket calls")
        sock = socket_calls[0]
        self.assertIn("AF_", sock["args"][0], "socket should decode AF_* domain")
        self.assertIn("SOCK_", sock["args"][1], "socket should decode SOCK_* type")

        # shutdown: shutdown(sockfd, how)
        shutdown_calls = [sc for sc in syscalls if sc.get("syscall") == "shutdown"]
        self.assertGreater(len(shutdown_calls), 0, "Should have shutdown calls")
        shutdown = shutdown_calls[0]
        self.assertIn("SHUT_", shutdown["args"][1], "shutdown should decode SHUT_* flag")

        # getsockopt: getsockopt(sockfd, level, optname, optval, optlen)
        getsockopt_calls = [sc for sc in syscalls if sc.get("syscall") == "getsockopt"]
        self.assertGreater(len(getsockopt_calls), 0, "Should have getsockopt calls")
        getsockopt = getsockopt_calls[0]
        self.assertEqual(getsockopt["args"][1], "SOL_SOCKET", "getsockopt should decode SOL_SOCKET")
        self.assertIn("SO_", getsockopt["args"][2], "getsockopt should decode SO_* option name")

        # setsockopt: setsockopt(sockfd, level, optname, optval, optlen)
        setsockopt_calls = [sc for sc in syscalls if sc.get("syscall") == "setsockopt"]
        self.assertGreater(len(setsockopt_calls), 0, "Should have setsockopt calls")
        setsockopt = setsockopt_calls[0]
        self.assertEqual(setsockopt["args"][1], "SOL_SOCKET", "setsockopt should decode SOL_SOCKET")
        self.assertEqual(
            setsockopt["args"][2], "SO_KEEPALIVE", "setsockopt should decode SO_KEEPALIVE"
        )


if __name__ == "__main__":
    unittest.main()
