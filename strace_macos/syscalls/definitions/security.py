"""Security and access control syscall definitions.

Priority 7: Lowest priority, includes MAC (Mandatory Access Control),
code signing, and System Integrity Protection syscalls.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef

# All security syscalls (11 total) with full argument definitions
SECURITY_SYSCALLS: list[SyscallDef] = [
    # MAC (Mandatory Access Control) syscalls
    SyscallDef(numbers.SYS___mac_syscall, "__mac_syscall", ["string", "int", "pointer"]),  # 381
    SyscallDef(numbers.SYS___mac_get_file, "__mac_get_file", ["string", "pointer"]),  # 382
    SyscallDef(numbers.SYS___mac_set_file, "__mac_set_file", ["string", "pointer"]),  # 383
    SyscallDef(numbers.SYS___mac_get_link, "__mac_get_link", ["string", "pointer"]),  # 384
    SyscallDef(numbers.SYS___mac_set_link, "__mac_set_link", ["string", "pointer"]),  # 385
    SyscallDef(numbers.SYS___mac_get_fd, "__mac_get_fd", ["int", "pointer"]),  # 388
    SyscallDef(numbers.SYS___mac_set_fd, "__mac_set_fd", ["int", "pointer"]),  # 389
    SyscallDef(
        numbers.SYS___mac_mount,
        "__mac_mount",
        ["string", "string", "int", "pointer", "pointer"],
    ),  # 424
    SyscallDef(numbers.SYS___mac_getfsstat, "__mac_getfsstat", ["pointer", "int", "int"]),  # 426
    # Code signing and SIP
    SyscallDef(numbers.SYS_csops, "csops", ["pid_t", "unsigned int", "pointer", "size_t"]),  # 169
    SyscallDef(numbers.SYS_csrctl, "csrctl", ["uint32_t", "pointer", "size_t"]),  # 465
]
