"""Syscall definitions organized by category."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class SyscallDef:
    """Definition of a single syscall.

    Attributes:
        number: Syscall number (from sys/syscall.h)
        name: Syscall name (e.g., "open", "read")
        arg_types: List of argument type hints (e.g., ["string", "int", "int"])
        arg_decoders: Optional list of decoder functions for symbolic decoding
                      (None means no decoder for that argument position)
        output_params: Optional list of (arg_index, struct_name) tuples indicating
                       which arguments are output parameters that should be decoded
                       at syscall exit. E.g., [(1, "stat")] means arg 1 is a pointer
                       to struct stat that gets filled by the syscall.
        buffer_params: Optional list of (arg_index, size_arg_index, direction) tuples
                       indicating buffer parameters. Direction is "in" for write buffers
                       (shown on entry) or "out" for read buffers (shown on exit).
                       E.g., [(1, 2, "out")] for read(fd, buf, count) means arg 1 is
                       a buffer whose size is in arg 2, shown on exit.
    """

    number: int
    name: str
    arg_types: list[str]
    arg_decoders: list[Callable[[int], str] | None] | None = field(default=None)
    output_params: list[tuple[int, str]] | None = field(default=None)
    buffer_params: list[tuple[int, int, str]] | None = field(default=None)
