"""IPC (Inter-Process Communication) syscall definitions.

Priority 6: Lower priority, implement after core functionality works.
"""

from __future__ import annotations

from strace_macos.syscalls import numbers
from strace_macos.syscalls.definitions import SyscallDef
from strace_macos.syscalls.symbols import (
    decode_ipc_cmd,
    decode_ipc_flags,
    decode_shm_flags,
)

# All IPC syscalls (42 total) with full argument definitions
IPC_SYSCALLS: list[SyscallDef] = [
    # I/O multiplexing
    SyscallDef(
        numbers.SYS_select,
        "select",
        ["int", "pointer", "pointer", "pointer", "pointer"],
    ),  # 93
    SyscallDef(numbers.SYS_poll, "poll", ["pointer", "uint32_t", "int"]),  # 230
    SyscallDef(
        numbers.SYS_pselect,
        "pselect",
        ["int", "pointer", "pointer", "pointer", "pointer", "pointer"],
    ),  # 312
    SyscallDef(
        numbers.SYS_select_nocancel,
        "__select_nocancel",
        ["int", "pointer", "pointer", "pointer", "pointer"],
    ),  # 407
    SyscallDef(
        numbers.SYS_pselect_nocancel,
        "__pselect_nocancel",
        ["int", "pointer", "pointer", "pointer", "pointer", "pointer"],
    ),  # 417
    SyscallDef(numbers.SYS_poll_nocancel, "__poll_nocancel", ["pointer", "uint32_t", "int"]),  # 427
    # System V IPC
    SyscallDef(numbers.SYS_semsys, "semsys", ["int", "int", "int", "int", "int"]),  # 251
    SyscallDef(numbers.SYS_msgsys, "msgsys", ["int", "int", "int", "int", "int"]),  # 252
    SyscallDef(numbers.SYS_shmsys, "shmsys", ["int", "int", "int", "int"]),  # 253
    SyscallDef(
        numbers.SYS_semctl,
        "semctl",
        ["int", "int", "int", "pointer"],
        [None, None, decode_ipc_cmd, None],
    ),  # 254
    SyscallDef(
        numbers.SYS_semget,
        "semget",
        ["key_t", "int", "int"],
        [None, None, decode_ipc_flags],
    ),  # 255
    SyscallDef(numbers.SYS_semop, "semop", ["int", "pointer", "size_t"]),  # 256
    SyscallDef(
        numbers.SYS_msgctl,
        "msgctl",
        ["int", "int", "pointer"],
        [None, decode_ipc_cmd, None],
    ),  # 258
    SyscallDef(numbers.SYS_msgget, "msgget", ["key_t", "int"], [None, decode_ipc_flags]),  # 259
    SyscallDef(numbers.SYS_msgsnd, "msgsnd", ["int", "pointer", "size_t", "int"]),  # 260
    SyscallDef(numbers.SYS_msgrcv, "msgrcv", ["int", "pointer", "size_t", "long", "int"]),  # 261
    SyscallDef(
        numbers.SYS_shmat,
        "shmat",
        ["int", "pointer", "int"],
        [None, None, decode_shm_flags],
    ),  # 262
    SyscallDef(
        numbers.SYS_shmctl,
        "shmctl",
        ["int", "int", "pointer"],
        [None, decode_ipc_cmd, None],
    ),  # 263
    SyscallDef(numbers.SYS_shmdt, "shmdt", ["pointer"]),  # 264
    SyscallDef(
        numbers.SYS_shmget,
        "shmget",
        ["key_t", "size_t", "int"],
        [None, None, decode_ipc_flags],
    ),  # 265
    # POSIX semaphores
    SyscallDef(numbers.SYS_sem_wait, "sem_wait", ["pointer"]),  # 271
    SyscallDef(numbers.SYS_sem_trywait, "sem_trywait", ["pointer"]),  # 272
    SyscallDef(numbers.SYS_sem_post, "sem_post", ["pointer"]),  # 273
    # Async I/O
    SyscallDef(numbers.SYS_aio_return, "aio_return", ["pointer"]),  # 314
    SyscallDef(numbers.SYS_aio_suspend, "aio_suspend", ["pointer", "int", "pointer"]),  # 315
    SyscallDef(numbers.SYS_aio_cancel, "aio_cancel", ["int", "pointer"]),  # 316
    SyscallDef(numbers.SYS_aio_error, "aio_error", ["pointer"]),  # 317
    SyscallDef(numbers.SYS_lio_listio, "lio_listio", ["int", "pointer", "int", "pointer"]),  # 320
    # kqueue
    SyscallDef(numbers.SYS_kqueue, "kqueue", []),  # 362
    SyscallDef(
        numbers.SYS_kevent,
        "kevent",
        ["int", "pointer", "int", "pointer", "int", "pointer"],
    ),  # 363
    SyscallDef(
        numbers.SYS_kevent64,
        "kevent64",
        ["int", "pointer", "int", "pointer", "int", "unsigned int", "pointer"],
    ),  # 369
    SyscallDef(
        numbers.SYS_kevent_qos,
        "kevent_qos",
        [
            "int",
            "pointer",
            "int",
            "pointer",
            "int",
            "pointer",
            "pointer",
            "unsigned int",
        ],
    ),  # 374
    SyscallDef(
        numbers.SYS_kevent_id,
        "kevent_id",
        [
            "uint64_t",
            "pointer",
            "int",
            "pointer",
            "int",
            "pointer",
            "pointer",
            "unsigned int",
        ],
    ),  # 375
    # Pthread synchronization (psynch)
    SyscallDef(
        numbers.SYS_psynch_rw_rdlock,
        "psynch_rw_rdlock",
        ["pointer", "uint32_t", "uint32_t", "uint32_t", "int"],
    ),  # 301
    SyscallDef(
        numbers.SYS_psynch_rw_wrlock,
        "psynch_rw_wrlock",
        ["pointer", "uint32_t", "uint32_t", "uint32_t", "int"],
    ),  # 302
    SyscallDef(
        numbers.SYS_psynch_rw_unlock,
        "psynch_rw_unlock",
        ["pointer", "uint32_t", "uint32_t", "uint32_t", "int"],
    ),  # 303
    SyscallDef(
        numbers.SYS_psynch_cvwait,
        "psynch_cvwait",
        [
            "pointer",
            "uint32_t",
            "uint32_t",
            "pointer",
            "uint32_t",
            "uint32_t",
            "uint64_t",
            "uint32_t",
        ],
    ),  # 305
    SyscallDef(
        numbers.SYS_psynch_cvbroad,
        "psynch_cvbroad",
        [
            "pointer",
            "uint32_t",
            "uint32_t",
            "pointer",
            "uint32_t",
            "uint32_t",
            "uint64_t",
            "uint32_t",
        ],
    ),  # 303
    SyscallDef(
        numbers.SYS_psynch_cvsignal,
        "psynch_cvsignal",
        [
            "pointer",
            "uint32_t",
            "uint32_t",
            "pointer",
            "uint32_t",
            "uint32_t",
            "uint32_t",
            "uint32_t",
        ],
    ),  # 304
    SyscallDef(
        numbers.SYS_psynch_mutexwait,
        "psynch_mutexwait",
        ["pointer", "uint32_t", "uint32_t", "uint64_t", "uint32_t"],
    ),  # 301
    SyscallDef(
        numbers.SYS_psynch_mutexdrop,
        "psynch_mutexdrop",
        ["pointer", "uint32_t", "uint32_t", "uint64_t", "uint32_t"],
    ),  # 302
    # Non-cancelable variants
    SyscallDef(
        numbers.SYS_msgsnd_nocancel,
        "__msgsnd_nocancel",
        ["int", "pointer", "size_t", "int"],
    ),  # 418
    SyscallDef(
        numbers.SYS_msgrcv_nocancel,
        "__msgrcv_nocancel",
        ["int", "pointer", "size_t", "long", "int"],
    ),  # 419
    SyscallDef(
        numbers.SYS_aio_suspend_nocancel,
        "__aio_suspend_nocancel",
        ["pointer", "int", "pointer"],
    ),  # 421
    SyscallDef(numbers.SYS_sem_wait_nocancel, "__sem_wait_nocancel", ["pointer"]),  # 420
    # Other IPC
    SyscallDef(numbers.SYS_guarded_kqueue_np, "guarded_kqueue_np", ["pointer", "int"]),  # 443
    SyscallDef(numbers.SYS_ulock_wake, "ulock_wake", ["uint32_t", "pointer", "uint64_t"]),  # 516
    SyscallDef(
        numbers.SYS_kqueue_workloop_ctl,
        "kqueue_workloop_ctl",
        ["pointer", "uint32_t", "pointer", "size_t"],
    ),  # 530
]
