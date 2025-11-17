"""Helper utilities for strace-macos tests."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from multiprocessing.synchronize import Event
    from pathlib import Path


def wait_for_ready(event: Event, timeout: float = 5.0) -> None:
    """Block until the target process signals it is ready to be traced.

    Args:
        event: Multiprocessing event to wait on
        timeout: Maximum time to wait in seconds

    Raises:
        TimeoutError: If the event is not set within the timeout period
    """
    if not event.wait(timeout=timeout):
        msg = "target process never became ready"
        raise TimeoutError(msg)


def json_lines(path: Path) -> list[dict[str, Any]]:
    """Parse JSON Lines file and return list of parsed objects.

    Args:
        path: Path to JSON Lines file

    Returns:
        List of parsed JSON objects, one per line

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If any line is invalid JSON
    """
    syscalls: list[dict[str, Any]] = []
    with path.open() as f:
        for raw_line in f:
            line = raw_line.strip()
            if line:  # Skip empty lines
                syscalls.append(json.loads(line))
    return syscalls


def verify_syscall_in_json(syscalls: list[dict[str, Any]], expected_name: str) -> bool:
    """Check if a syscall with the given name exists in the syscalls list.

    Args:
        syscalls: List of syscall dictionaries from JSON Lines output
        expected_name: Name of the syscall to find

    Returns:
        True if found, False otherwise
    """
    syscall_names = [sc.get("syscall") for sc in syscalls]
    return expected_name in syscall_names


def verify_json_syscall_structure(syscall: dict[str, Any]) -> bool:
    """Verify that a syscall dictionary has the expected JSON structure.

    Args:
        syscall: Syscall dictionary to verify

    Returns:
        True if structure is valid, False otherwise
    """
    required_keys = {"syscall", "args", "return", "pid", "timestamp"}
    return all(key in syscall for key in required_keys)


def verify_text_output_format(content: str) -> bool:
    """Verify that text output matches strace format.

    Args:
        content: Text output from strace-macos

    Returns:
        True if format looks valid, False otherwise
    """
    # Check for basic strace format: "syscall(...) = retval"
    return ") =" in content or ") = ?" in content
