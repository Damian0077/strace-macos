"""System information and control syscall definitions.

Priority 7: Lowest priority, includes sysctl and system information queries.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef

# All system information syscalls (12 total) with full argument definitions
SYSINFO_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS_getdtablesize, "getdtablesize", []),  # 89
    SyscallDef(numbers.SYS_gethostuuid, "gethostuuid", ["pointer", "pointer"]),  # 142
    SyscallDef(
        numbers.SYS_sysctl,
        "sysctl",
        ["pointer", "uint32_t", "pointer", "pointer", "pointer", "size_t"],
    ),  # 202
    SyscallDef(
        numbers.SYS_sysctlbyname,
        "sysctlbyname",
        ["string", "size_t", "pointer", "pointer", "pointer", "size_t"],
    ),  # 274
    SyscallDef(
        numbers.SYS_memorystatus_control,
        "memorystatus_control",
        ["uint32_t", "int32_t", "uint32_t", "pointer", "size_t"],
    ),  # 337
    SyscallDef(numbers.SYS_usrctl, "usrctl", ["uint32_t"]),  # 452
    SyscallDef(
        numbers.SYS_telemetry,
        "telemetry",
        ["uint64_t", "uint64_t", "pointer", "pointer"],
    ),  # 464
    SyscallDef(numbers.SYS_ledger, "ledger", ["int", "pointer", "pointer", "pointer"]),  # 478
    SyscallDef(numbers.SYS_kas_info, "kas_info", ["int", "pointer", "pointer", "pointer"]),  # 487
    SyscallDef(
        numbers.SYS_work_interval_ctl,
        "work_interval_ctl",
        ["uint32_t", "uint64_t", "pointer", "size_t"],
    ),  # 499
    SyscallDef(numbers.SYS_getentropy, "getentropy", ["pointer", "size_t"]),  # 500
    SyscallDef(
        numbers.SYS_memorystatus_available_memory, "memorystatus_available_memory", []
    ),  # 520
]
