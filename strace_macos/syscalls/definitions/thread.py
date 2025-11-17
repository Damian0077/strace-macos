"""Thread management syscall definitions.

Priority 5: Lower priority, implement after core functionality works.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef

# All thread management syscalls (10 total) with full argument definitions
THREAD_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS___pthread_canceled, "__pthread_canceled", ["int"]),  # 333
    SyscallDef(numbers.SYS___pthread_markcancel, "__pthread_markcancel", ["int"]),  # 332
    SyscallDef(numbers.SYS___pthread_chdir, "__pthread_chdir", ["string"]),  # 348
    SyscallDef(numbers.SYS___pthread_fchdir, "__pthread_fchdir", ["int"]),  # 349
    SyscallDef(
        numbers.SYS_bsdthread_create,
        "bsdthread_create",
        ["pointer", "pointer", "pointer", "pointer", "uint32_t"],
    ),  # 360
    SyscallDef(
        numbers.SYS_bsdthread_terminate,
        "bsdthread_terminate",
        ["pointer", "size_t", "uint32_t", "uint32_t"],
    ),  # 361
    SyscallDef(
        numbers.SYS_bsdthread_register,
        "bsdthread_register",
        ["pointer", "pointer", "int"],
    ),  # 366
    SyscallDef(
        numbers.SYS_bsdthread_ctl,
        "bsdthread_ctl",
        ["pointer", "uint64_t", "pointer", "pointer"],
    ),  # 449
    SyscallDef(numbers.SYS_thread_selfusage, "thread_selfusage", []),  # 475
    SyscallDef(numbers.SYS_thread_selfid, "thread_selfid", []),  # 539
]
