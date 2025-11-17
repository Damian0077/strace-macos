"""Typed syscall arguments for better formatting and highlighting."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SyscallArg(ABC):
    """Base class for typed syscall arguments."""

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of the argument."""
        ...


class IntArg(SyscallArg):
    """Signed integer argument."""

    def __init__(self, value: int, symbolic: str | None = None) -> None:
        """Initialize an integer argument.

        Args:
            value: The integer value
            symbolic: Optional symbolic representation (e.g., "AT_FDCWD" for -2)
        """
        self.value = value
        self.symbolic = symbolic

    def __str__(self) -> str:
        """Return string representation."""
        return self.symbolic if self.symbolic else str(self.value)


class UnsignedArg(SyscallArg):
    """Unsigned integer argument."""

    def __init__(self, value: int) -> None:
        """Initialize an unsigned integer argument.

        Args:
            value: The unsigned integer value
        """
        self.value = value

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.value)


class PointerArg(SyscallArg):
    """Memory pointer/address argument."""

    def __init__(self, address: int) -> None:
        """Initialize a pointer argument.

        Args:
            address: The memory address
        """
        self.address = address

    def __str__(self) -> str:
        """Return string representation as hex."""
        return f"0x{self.address:x}"


class StringArg(SyscallArg):
    """String argument (typically a file path or text)."""

    def __init__(self, value: str) -> None:
        """Initialize a string argument.

        Args:
            value: The string value
        """
        self.value = value

    def __str__(self) -> str:
        """Return string representation with quotes."""
        # Escape special characters for display
        escaped = self.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'


class FileDescriptorArg(SyscallArg):
    """File descriptor argument (special case of int)."""

    def __init__(self, fd: int) -> None:
        """Initialize a file descriptor argument.

        Args:
            fd: The file descriptor number
        """
        self.fd = fd

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.fd)


class FlagsArg(SyscallArg):
    """Flags/bitmask argument (displayed as hex or symbolic)."""

    def __init__(self, value: int, symbolic: str | None = None) -> None:
        """Initialize a flags argument.

        Args:
            value: The flags value
            symbolic: Optional symbolic representation (e.g., "O_WRONLY|O_CREAT")
        """
        self.value = value
        self.symbolic = symbolic

    def __str__(self) -> str:
        """Return string representation."""
        return self.symbolic if self.symbolic else f"0x{self.value:x}"


class StructArg(SyscallArg):
    """Decoded struct argument (e.g., struct stat output)."""

    def __init__(self, fields: dict[str, str | int]) -> None:
        """Initialize a struct argument.

        Args:
            fields: Dictionary of field names to their decoded values
                   Values can be strings (already formatted) or ints (will be formatted)
        """
        self.fields = fields

    def __str__(self) -> str:
        """Return string representation as {field1=value1, field2=value2, ...}."""
        if not self.fields:
            return "{}"

        field_strs = []
        for name, value in self.fields.items():
            if isinstance(value, str):
                field_strs.append(f"{name}={value}")
            else:
                field_strs.append(f"{name}={value}")

        return "{" + ", ".join(field_strs) + "}"


class BufferArg(SyscallArg):
    """Buffer argument showing actual data (for read/write syscalls)."""

    def __init__(self, data: bytes, address: int, max_display: int = 32) -> None:
        """Initialize a buffer argument.

        Args:
            data: The actual buffer data
            address: The memory address of the buffer
            max_display: Maximum number of bytes to display (default 32)
        """
        self.data = data
        self.address = address
        self.max_display = max_display

    def __str__(self) -> str:
        """Return string representation showing buffer contents."""
        if not self.data:
            return '""'

        # Try to decode as UTF-8 text
        try:
            text = self.data[: self.max_display].decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            # Binary data - show as hex
            hex_data = self.data[: self.max_display].hex()
            suffix = "..." if len(self.data) > self.max_display else ""
            hex_bytes = " \\x".join(hex_data[i : i + 2] for i in range(0, len(hex_data), 2))
            return f'"\\x{hex_bytes}{suffix}"'
        else:
            # Escape special characters
            escaped = (
                text.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t")
            )
            suffix = "..." if len(self.data) > self.max_display else ""
            return f'"{escaped}{suffix}"'


class UnknownArg(SyscallArg):
    """Unknown or unparsable argument."""

    def __str__(self) -> str:
        """Return string representation."""
        return "?"
