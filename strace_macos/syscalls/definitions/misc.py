"""Miscellaneous syscall definitions.

These are syscalls that don't fit into the main categories.
Priority 7: Lowest priority.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef

# Miscellaneous syscalls (22 total) - truly miscellaneous syscalls that don't fit other categories
MISC_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS_syscall, "syscall", ["int", "pointer"]),  # 0
    SyscallDef(
        numbers.SYS_crossarch_trap,
        "crossarch_trap",
        ["uint32_t", "uint32_t", "uint32_t", "uint32_t"],
    ),  # 38
    SyscallDef(numbers.SYS_acct, "acct", ["string"]),  # 51
    SyscallDef(numbers.SYS_reboot, "reboot", ["int", "string"]),  # 55
    SyscallDef(numbers.SYS_swapon, "swapon", []),  # 85
    SyscallDef(
        numbers.SYS_connectx,
        "connectx",
        [
            "int",
            "pointer",
            "socklen_t",
            "pointer",
            "socklen_t",
            "uint32_t",
            "pointer",
            "pointer",
        ],
    ),  # 455
    SyscallDef(
        numbers.SYS_grab_pgo_data,
        "grab_pgo_data",
        ["pointer", "int", "pointer", "size_t", "pointer", "pointer"],
    ),  # 469
    SyscallDef(
        numbers.SYS_map_with_linking_np,
        "map_with_linking_np",
        ["pointer", "size_t", "int", "int", "int", "off_t", "pointer"],
    ),  # 470
    SyscallDef(numbers.SYS_fileport_makeport, "fileport_makeport", ["int", "pointer"]),  # 473
    SyscallDef(numbers.SYS_fileport_makefd, "fileport_makefd", ["pointer"]),  # 474
    SyscallDef(numbers.SYS_necp_open, "necp_open", ["int"]),  # 501
    # Process/resource limit control
    SyscallDef(
        numbers.SYS_proc_rlimit_control,
        "proc_rlimit_control",
        ["pid_t", "int", "pointer"],
    ),  # 454
    # Code signing/profiling
    SyscallDef(
        numbers.SYS_csops_audittoken,
        "csops_audittoken",
        ["pid_t", "unsigned int", "pointer", "size_t", "pointer"],
    ),  # 170
    # Thread self-accounting
    SyscallDef(
        numbers.SYS_thread_selfcounts, "thread_selfcounts", ["int", "pointer", "size_t"]
    ),  # 186
    # Duplicate entry already in file.py
    SyscallDef(
        numbers.SYS_fsetattrlist,
        "fsetattrlist",
        ["int", "pointer", "pointer", "size_t", "uint32_t"],
    ),  # 229
]
