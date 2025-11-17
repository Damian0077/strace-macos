"""Architecture-specific abstractions for syscall tracing."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lldb


class Architecture(ABC):
    """Abstract base class for architecture-specific behavior."""

    @property
    @abstractmethod
    def arg_registers(self) -> list[str]:
        """Register names for function arguments."""

    @property
    @abstractmethod
    def return_register(self) -> str:
        """Register name for return values."""

    @abstractmethod
    def get_return_address(
        self, frame: lldb.SBFrame, process: lldb.SBProcess, lldb_module: object
    ) -> int | None:
        """Get the return address for the current function call.

        Args:
            frame: LLDB stack frame
            process: LLDB process
            lldb_module: LLDB module for error handling

        Returns:
            Return address or None if unable to determine
        """


class ARM64Architecture(Architecture):
    """ARM64 (AArch64) architecture."""

    @property
    def arg_registers(self) -> list[str]:
        """ARM64 calling convention: x0-x7 for first 8 arguments."""
        return ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"]

    @property
    def return_register(self) -> str:
        """ARM64 uses x0 for return values."""
        return "x0"

    def get_return_address(
        self,
        frame: lldb.SBFrame,
        process: lldb.SBProcess,  # noqa: ARG002
        lldb_module: object,  # noqa: ARG002
    ) -> int | None:
        """Get return address from lr (link register / x30).

        Args:
            frame: LLDB stack frame
            process: LLDB process (unused on ARM64)
            lldb_module: LLDB module (unused on ARM64)

        Returns:
            Return address from lr register or None if invalid
        """
        lr_reg = frame.FindRegister("lr")
        if not lr_reg or not lr_reg.IsValid():
            return None
        return lr_reg.GetValueAsUnsigned()  # type: ignore[no-any-return]


class X8664Architecture(Architecture):
    """x86_64 (AMD64) architecture."""

    @property
    def arg_registers(self) -> list[str]:
        """x86_64 calling convention: rdi, rsi, rdx, rcx, r8, r9 for first 6 arguments."""
        return ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

    @property
    def return_register(self) -> str:
        """x86_64 uses rax for return values."""
        return "rax"

    def get_return_address(
        self, frame: lldb.SBFrame, process: lldb.SBProcess, lldb_module: object
    ) -> int | None:
        """Get return address from stack (at [rsp]).

        Args:
            frame: LLDB stack frame
            process: LLDB process
            lldb_module: LLDB module for error handling

        Returns:
            Return address from stack or None if unable to read
        """
        sp_reg = frame.FindRegister("rsp")
        if not sp_reg or not sp_reg.IsValid():
            return None

        sp = sp_reg.GetValueAsUnsigned()
        error = lldb_module.SBError()  # type: ignore[attr-defined]
        return_address_bytes = process.ReadMemory(sp, 8, error)
        if error.Fail():
            return None

        return int.from_bytes(return_address_bytes, byteorder="little")


def detect_architecture(target: lldb.SBTarget) -> Architecture | None:
    """Detect architecture from LLDB target.

    Args:
        target: LLDB target

    Returns:
        Architecture instance or None if unsupported
    """
    arch = target.GetTriple().split("-")[0]

    if arch in ("arm64", "aarch64", "arm64e"):
        return ARM64Architecture()
    if arch in ("x86_64", "i386"):
        return X8664Architecture()
    return None
