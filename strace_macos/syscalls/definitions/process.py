"""Process management syscall definitions.

Priority 3: Required for process tests.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef
from strace_macos.syscalls.symbols import (
    decode_idtype,
    decode_prio_which,
    decode_rlimit_resource,
    decode_rusage_who,
    decode_sigprocmask_how,
    decode_wait_options,
    decode_waitid_options,
)

# All process management syscalls (72 total) with full argument definitions
PROCESS_SYSCALLS: list[SyscallDef] = [
    SyscallDef(numbers.SYS_exit, "exit", ["int"]),  # 1
    SyscallDef(numbers.SYS_fork, "fork", []),  # 2
    SyscallDef(
        numbers.SYS_wait4,
        "wait4",
        ["pid_t", "pointer", "int", "pointer"],
        [None, None, decode_wait_options, None],
    ),  # 7
    SyscallDef(numbers.SYS_getpid, "getpid", []),  # 20
    SyscallDef(numbers.SYS_setuid, "setuid", ["uid_t"]),  # 23
    SyscallDef(numbers.SYS_getuid, "getuid", []),  # 24
    SyscallDef(numbers.SYS_geteuid, "geteuid", []),  # 25
    SyscallDef(numbers.SYS_getppid, "getppid", []),  # 39
    SyscallDef(numbers.SYS_getegid, "getegid", []),  # 43
    SyscallDef(numbers.SYS_getgid, "getgid", []),  # 47
    SyscallDef(
        numbers.SYS_sigprocmask,
        "sigprocmask",
        ["int", "pointer", "pointer"],
        [decode_sigprocmask_how, None, None],
    ),  # 48
    SyscallDef(numbers.SYS_getlogin, "getlogin", ["pointer", "uint32_t"]),  # 49
    SyscallDef(numbers.SYS_setlogin, "setlogin", ["string"]),  # 50
    SyscallDef(numbers.SYS_execve, "execve", ["string", "pointer", "pointer"]),  # 59
    SyscallDef(numbers.SYS_vfork, "vfork", []),  # 66
    SyscallDef(numbers.SYS_oslog_coproc_reg, "oslog_coproc_reg", ["pointer", "size_t"]),  # 67
    SyscallDef(numbers.SYS_oslog_coproc, "oslog_coproc", ["pointer", "size_t", "size_t"]),  # 68
    SyscallDef(numbers.SYS_getgroups, "getgroups", ["uint32_t", "pointer"]),  # 79
    SyscallDef(numbers.SYS_setgroups, "setgroups", ["uint32_t", "pointer"]),  # 80
    SyscallDef(numbers.SYS_getpgrp, "getpgrp", []),  # 81
    SyscallDef(numbers.SYS_setpgid, "setpgid", ["pid_t", "pid_t"]),  # 82
    SyscallDef(numbers.SYS_setreuid, "setreuid", ["uid_t", "uid_t"]),  # 126
    SyscallDef(numbers.SYS_setregid, "setregid", ["gid_t", "gid_t"]),  # 127
    SyscallDef(
        numbers.SYS_setpriority,
        "setpriority",
        ["int", "int", "int"],
        [decode_prio_which, None, None],
    ),  # 96
    SyscallDef(
        numbers.SYS_getpriority,
        "getpriority",
        ["int", "int"],
        [decode_prio_which, None],
    ),  # 100
    SyscallDef(
        numbers.SYS_getrusage,
        "getrusage",
        ["int", "pointer"],
        [decode_rusage_who, None],
    ),  # 117
    SyscallDef(numbers.SYS_setsid, "setsid", []),  # 147
    SyscallDef(numbers.SYS_getpgid, "getpgid", ["pid_t"]),  # 151
    SyscallDef(numbers.SYS_setprivexec, "setprivexec", ["int"]),  # 152
    SyscallDef(
        numbers.SYS_waitid,
        "waitid",
        ["int", "uint64_t", "pointer", "int"],
        [decode_idtype, None, None, decode_waitid_options],
    ),  # 173
    SyscallDef(numbers.SYS_setgid, "setgid", ["gid_t"]),  # 181
    SyscallDef(numbers.SYS_setegid, "setegid", ["gid_t"]),  # 182
    SyscallDef(numbers.SYS_seteuid, "seteuid", ["uid_t"]),  # 183
    SyscallDef(
        numbers.SYS_getrlimit,
        "getrlimit",
        ["uint32_t", "pointer"],
        [decode_rlimit_resource, None],
    ),  # 194
    SyscallDef(
        numbers.SYS_setrlimit,
        "setrlimit",
        ["uint32_t", "pointer"],
        [decode_rlimit_resource, None],
    ),  # 195
    SyscallDef(
        numbers.SYS_initgroups, "initgroups", ["string", "int", "pointer", "uint32_t"]
    ),  # 243
    SyscallDef(
        numbers.SYS_posix_spawn,
        "posix_spawn",
        ["pointer", "string", "pointer", "pointer", "pointer", "pointer"],
    ),  # 244
    SyscallDef(numbers.SYS_sem_wait, "sem_wait", ["pointer"]),  # 271
    SyscallDef(numbers.SYS_sem_trywait, "sem_trywait", ["pointer"]),  # 272
    SyscallDef(numbers.SYS_settid, "settid", ["uid_t", "gid_t"]),  # 285
    SyscallDef(numbers.SYS_gettid, "gettid", ["pointer", "pointer"]),  # 286
    SyscallDef(numbers.SYS_getsid, "getsid", ["pid_t"]),  # 310
    SyscallDef(numbers.SYS_settid_with_pid, "settid_with_pid", ["pid_t", "int"]),  # 311
    SyscallDef(
        numbers.SYS_process_policy,
        "process_policy",
        ["int", "int", "uint64_t", "uint32_t", "pointer", "pid_t", "uint64_t"],
    ),  # 323
    SyscallDef(numbers.SYS_issetugid, "issetugid", []),  # 327
    SyscallDef(numbers.SYS___sigwait, "__sigwait", ["pointer", "pointer"]),  # 330
    SyscallDef(
        numbers.SYS___semwait_signal,
        "__semwait_signal",
        ["int", "int", "int", "int", "int64_t", "int32_t"],
    ),  # 334
    SyscallDef(
        numbers.SYS_proc_info,
        "proc_info",
        ["int32_t", "int32_t", "uint32_t", "uint64_t", "pointer", "int32_t"],
    ),  # 336
    SyscallDef(
        numbers.SYS_workq_kernreturn,
        "workq_kernreturn",
        ["int", "pointer", "int", "int"],
    ),  # 368
    SyscallDef(
        numbers.SYS___mac_execve,
        "__mac_execve",
        ["string", "pointer", "pointer", "pointer"],
    ),  # 380
    SyscallDef(numbers.SYS___mac_get_proc, "__mac_get_proc", ["pointer"]),  # 386
    SyscallDef(numbers.SYS___mac_set_proc, "__mac_set_proc", ["pointer"]),  # 387
    SyscallDef(numbers.SYS___mac_get_pid, "__mac_get_pid", ["pid_t", "pointer"]),  # 390
    SyscallDef(
        numbers.SYS_wait4_nocancel,
        "__wait4_nocancel",
        ["pid_t", "pointer", "int", "pointer"],
        [None, None, decode_wait_options, None],
    ),  # 400
    SyscallDef(
        numbers.SYS_waitid_nocancel,
        "__waitid_nocancel",
        ["int", "uint64_t", "pointer", "int"],
        [decode_idtype, None, None, decode_waitid_options],
    ),  # 416
    SyscallDef(numbers.SYS_sem_wait_nocancel, "__sem_wait_nocancel", ["pointer"]),  # 420
    SyscallDef(numbers.SYS___sigwait_nocancel, "__sigwait_nocancel", ["pointer", "pointer"]),  # 422
    SyscallDef(
        numbers.SYS___semwait_signal_nocancel,
        "__semwait_signal_nocancel",
        ["int", "int", "int", "int", "int64_t", "int32_t"],
    ),  # 423
    SyscallDef(numbers.SYS_pid_suspend, "pid_suspend", ["pid_t"]),  # 433
    SyscallDef(numbers.SYS_pid_resume, "pid_resume", ["pid_t"]),  # 434
    SyscallDef(numbers.SYS_pid_hibernate, "pid_hibernate", ["pid_t"]),  # 435
    SyscallDef(
        numbers.SYS_proc_rlimit_control,
        "proc_rlimit_control",
        ["pid_t", "int", "pointer"],
    ),  # 446
    SyscallDef(
        numbers.SYS_proc_uuid_policy,
        "proc_uuid_policy",
        ["uint32_t", "pointer", "size_t", "uint32_t"],
    ),  # 452
    SyscallDef(numbers.SYS_sfi_pidctl, "sfi_pidctl", ["uint32_t", "pid_t", "uint32_t"]),  # 457
    SyscallDef(numbers.SYS_coalition, "coalition", ["uint32_t", "pointer", "size_t"]),  # 458
    SyscallDef(
        numbers.SYS_coalition_info,
        "coalition_info",
        ["uint32_t", "pointer", "pointer", "size_t"],
    ),  # 459
    SyscallDef(numbers.SYS_proc_trace_log, "proc_trace_log", ["pid_t", "uint64_t"]),  # 477
    SyscallDef(
        numbers.SYS_persona,
        "persona",
        ["uint32_t", "uint32_t", "pointer", "pointer", "size_t", "pointer"],
    ),  # 494
    SyscallDef(
        numbers.SYS_ulock_wait,
        "ulock_wait",
        ["uint32_t", "pointer", "uint64_t", "uint32_t"],
    ),  # 515
    SyscallDef(
        numbers.SYS_coalition_ledger,
        "coalition_ledger",
        ["uint32_t", "uint64_t", "pointer", "size_t"],
    ),  # 532
    SyscallDef(
        numbers.SYS_task_inspect_for_pid,
        "task_inspect_for_pid",
        ["int", "int", "uint64_t"],
    ),  # 538
    SyscallDef(
        numbers.SYS_ulock_wait2,
        "ulock_wait2",
        ["uint32_t", "pointer", "uint64_t", "uint64_t", "uint64_t"],
    ),  # 544
    SyscallDef(
        numbers.SYS_proc_info_extended_id,
        "proc_info_extended_id",
        [
            "int32_t",
            "int32_t",
            "uint32_t",
            "uint32_t",
            "pointer",
            "uint32_t",
            "pointer",
            "int32_t",
        ],
    ),  # 545
    SyscallDef(
        numbers.SYS_coalition_policy_set,
        "coalition_policy_set",
        ["uint64_t", "uint32_t", "pointer", "size_t"],
    ),  # 556
    SyscallDef(
        numbers.SYS_coalition_policy_get,
        "coalition_policy_get",
        ["uint64_t", "uint32_t", "pointer", "size_t"],
    ),  # 557
]
