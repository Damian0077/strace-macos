"""Signal handling syscall definitions.

Priority 5: Lower priority, implement after core functionality works.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef
from strace_macos.syscalls.symbols import decode_signal, decode_sigprocmask_how

# All signal handling syscalls (13 total) with full argument definitions
SIGNAL_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS_kill, "kill", ["pid_t", "int"], [None, decode_signal]),  # 37
    SyscallDef(
        numbers.SYS_sigaction,
        "sigaction",
        ["int", "pointer", "pointer"],
        [decode_signal, None, None],
    ),  # 46
    SyscallDef(numbers.SYS_sigpending, "sigpending", ["pointer"]),  # 52
    SyscallDef(numbers.SYS_sigaltstack, "sigaltstack", ["pointer", "pointer"]),  # 53
    SyscallDef(numbers.SYS_sigsuspend, "sigsuspend", ["pointer"]),  # 111
    SyscallDef(numbers.SYS_sigreturn, "sigreturn", ["pointer", "int"]),  # 184
    SyscallDef(numbers.SYS_sigsuspend_nocancel, "__sigsuspend_nocancel", ["pointer"]),  # 410
    SyscallDef(
        numbers.SYS___pthread_kill,
        "__pthread_kill",
        ["pointer", "int"],
        [None, decode_signal],
    ),  # 328
    SyscallDef(
        numbers.SYS___pthread_sigmask,
        "__pthread_sigmask",
        ["int", "pointer", "pointer"],
        [decode_sigprocmask_how, None, None],
    ),  # 329
    SyscallDef(
        numbers.SYS_sigprocmask,
        "sigprocmask",
        ["int", "pointer", "pointer"],
        [decode_sigprocmask_how, None, None],
    ),  # 48 (also in process, but primarily signal)
    SyscallDef(
        numbers.SYS___sigwait, "__sigwait", ["pointer", "pointer"]
    ),  # 330 (also in process, but primarily signal)
    SyscallDef(numbers.SYS___sigwait_nocancel, "__sigwait_nocancel", ["pointer", "pointer"]),  # 422
    SyscallDef(
        numbers.SYS___disable_threadsignal,
        "__disable_threadsignal",
        ["int"],
        [decode_signal],
    ),  # 331
]
