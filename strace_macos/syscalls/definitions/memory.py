"""Memory management syscall definitions.

Priority 4: Lower priority, implement after core functionality works.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef
from strace_macos.syscalls.symbols import (
    decode_madvise_advice,
    decode_map_flags,
    decode_mlockall_flags,
    decode_msync_flags,
    decode_prot_flags,
)

# All memory management syscalls (13 total) with full argument definitions
MEMORY_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS_munmap, "munmap", ["pointer", "size_t"]),  # 73
    SyscallDef(
        numbers.SYS_mprotect,
        "mprotect",
        ["pointer", "size_t", "int"],
        [None, None, decode_prot_flags],
    ),  # 74
    SyscallDef(
        numbers.SYS_madvise,
        "madvise",
        ["pointer", "size_t", "int"],
        [None, None, decode_madvise_advice],
    ),  # 75
    SyscallDef(numbers.SYS_mincore, "mincore", ["pointer", "size_t", "pointer"]),  # 78
    SyscallDef(
        numbers.SYS_mmap,
        "mmap",
        ["pointer", "size_t", "int", "int", "int", "off_t"],
        [None, None, decode_prot_flags, decode_map_flags, None, None],
    ),  # 197
    SyscallDef(numbers.SYS_mlock, "mlock", ["pointer", "size_t"]),  # 203
    SyscallDef(numbers.SYS_munlock, "munlock", ["pointer", "size_t"]),  # 204
    SyscallDef(numbers.SYS_minherit, "minherit", ["pointer", "size_t", "int"]),  # 250
    SyscallDef(numbers.SYS_shared_region_check_np, "shared_region_check_np", ["pointer"]),  # 294
    SyscallDef(
        numbers.SYS_vm_pressure_monitor,
        "vm_pressure_monitor",
        ["int", "int", "pointer"],
    ),  # 296
    SyscallDef(numbers.SYS_mlockall, "mlockall", ["int"], [decode_mlockall_flags]),  # 324
    SyscallDef(numbers.SYS_munlockall, "munlockall", []),  # 325
    SyscallDef(
        numbers.SYS_shared_region_map_and_slide_2_np,
        "shared_region_map_and_slide_2_np",
        ["uint32_t", "uint32_t", "pointer", "uint32_t", "pointer", "uint64_t"],
    ),  # 536
    SyscallDef(
        numbers.SYS_msync_nocancel,
        "__msync_nocancel",
        ["pointer", "size_t", "int"],
        [None, None, decode_msync_flags],
    ),  # 405
    SyscallDef(
        numbers.SYS_msync,
        "msync",
        ["pointer", "size_t", "int"],
        [None, None, decode_msync_flags],
    ),  # 65 (from file.py but is memory op)
    SyscallDef(
        numbers.SYS_mremap_encrypted,
        "mremap_encrypted",
        ["pointer", "size_t", "uint32_t", "uint32_t", "uint32_t"],
    ),  # 489 (also in file.py, but primarily memory op)
]
