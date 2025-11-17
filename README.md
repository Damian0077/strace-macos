# strace-macos

A system call tracer for macOS using the LLDB debugger API.

**Status**: Beta - Core functionality works, but some features are still in development.

## Features

- ✅ **Works with SIP enabled** - Unlike `dtruss`, doesn't require disabling System Integrity Protection
- ✅ **Pure Python implementation** - No kernel extensions or compiled components
- ✅ **Multiple output formats** - JSON Lines and strace-compatible text output
- ✅ **Syscall filtering** - Filter by syscall name or category (`-e trace=file`, `-e trace=network`)
- ✅ **Symbolic decoding** - Automatically decodes flags, error codes, and struct fields
- ✅ **Color output** - Syntax highlighting when output is a TTY
- ✅ **Summary statistics** - Time/call/error counts with `-c`

## Installation

### With Nix Flakes

```bash
# Run directly
nix run github:Mic92/strace-macos -- ls

# Install to profile
nix profile install github:Mic92/strace-macos

# Development shell
nix develop
```

### Manual Installation

strace-macos requires macOS system Python (has LLDB bindings):

```bash
git clone https://github.com/Mic92/strace-macos
cd strace-macos
/usr/bin/python3 -m pip install --user -e .
```

## Usage

### Trace a command

```bash
# Basic usage
strace ls -la

# Output to file
strace -o trace.txt ls

# JSON output
strace --json ls > trace.jsonl

# Filter syscalls
strace -e trace=open,close ls
strace -e trace=file ls        # All file operations
strace -e trace=network curl   # Network syscalls only
```

### Attach to running process

```bash
strace -p 1234
```

### Summary statistics

```bash
strace -c ls
# % time     seconds  usecs/call     calls    errors syscall
# ------ ----------- ----------- --------- --------- ----------------
#  45.23    0.001234          12       103           read
#  32.10    0.000876           8       110           write
#  ...
```

## Requirements

- macOS 12+ (Monterey or later)
- Apple Silicon (ARM64) or Intel (x86_64)
- Xcode Command Line Tools (for LLDB)
- System Python (`/usr/bin/python3`)

**Important**: Must use macOS system Python - LLDB bindings don't work with Homebrew/pyenv/Nix Python.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development environment setup
- Code style guidelines
- Testing instructions
- How to add new syscalls
- Pull request process

**Current Status**: 3/13 tests passing (spawn functionality working)

## Architecture

```
strace-macos (Python CLI)
    ↓
LLDB Python API
    ↓
debugserver (macOS debugging APIs)
    ↓
Target Process
```

The tracer uses LLDB's Python bindings to:
1. Set breakpoints at syscall entry/exit points
2. Read CPU registers to extract syscall arguments
3. Decode arguments symbolically (flags, errno, structs)
4. Format output in strace-compatible or JSON format

## Implementation Status

**Working**:
- ✅ Spawn and trace new processes
- ✅ Basic syscall capture (entry/exit)
- ✅ Argument decoding (integers, strings, pointers)
- ✅ Symbolic flag decoding (O_RDONLY, etc.)
- ✅ Error code decoding (ENOENT, etc.)
- ✅ JSON and text output formats
- ✅ Color output with syntax highlighting

**In Progress**:
- 🚧 Attach to running processes
- 🚧 Syscall filtering (`-e trace=`)
- 🚧 Network syscalls (socket, connect, etc.)
- 🚧 Summary statistics (`-c`)
- 🚧 Struct decoding (stat, etc.)

**Planned**:
- ⏳ Multi-threaded process support
- ⏳ Follow forks (`-f`)
- ⏳ String truncation control (`-s`)
- ⏳ Relative/absolute timestamps (`-t`, `-tt`, `-ttt`)

## Why not dtruss?

macOS ships with `dtruss`, a DTrace-based syscall tracer. However:

- ❌ Requires disabling System Integrity Protection (SIP)
- ❌ Doesn't work on modern macOS versions without workarounds
- ❌ Limited filtering capabilities
- ❌ No symbolic decoding of arguments

strace-macos works with SIP enabled and provides richer output.

## Comparison with Linux strace

strace-macos aims for compatibility with Linux strace where possible:

| Feature | Linux strace | strace-macos |
|---------|-------------|--------------|
| Basic tracing | ✅ | ✅ |
| Attach to PID | ✅ | 🚧 |
| Syscall filtering | ✅ | 🚧 |
| Summary stats | ✅ | 🚧 |
| Follow forks | ✅ | ⏳ |
| Symbolic decoding | ✅ | ✅ |
| JSON output | ❌ | ✅ |
| Color output | ❌ | ✅ |

## License

MIT License - see LICENSE file for details.

## Author

Jörg Thalheim <joerg@thalheim.io>

## See Also

- [CONTRIBUTING.md](CONTRIBUTING.md) - Development and contribution guide
- [tests/README.md](tests/README.md) - Test suite documentation
