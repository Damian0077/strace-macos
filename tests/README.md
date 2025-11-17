# strace-macos Tests

This directory contains integration tests for strace-macos.

## Running Tests

**Important**: Tests must be run with macOS system Python (`/usr/bin/python3`)
because strace-macos depends on LLDB, which only works with system Python.

### Run all tests

From the package root (`pkgs/strace-macos/`):

```bash
# Using the test runner script
/usr/bin/python3 run_tests.py

# Or using unittest directly
/usr/bin/python3 -m unittest discover tests/ -v
```

### Run specific test file

```bash
/usr/bin/python3 -m unittest tests.test_spawn -v
```

### Run specific test class

```bash
/usr/bin/python3 -m unittest tests.test_spawn.TestSpawn -v
```

### Run specific test method

```bash
/usr/bin/python3 -m unittest tests.test_spawn.TestSpawn.test_spawn_simple_command -v
```

## Test Structure

Tests are organized into multiple files (13 tests total):

- **test_spawn.py** (3 tests) - Tests for spawning and tracing new processes
  - Simple command execution
  - Python script with file operations
  - Failing command exit code propagation

- **test_attach.py** (4 tests) - Tests for attaching to running processes
  - Attach to file operations
  - Attach to network operations
  - Attach to long-running process
  - Error handling for non-existent PID

- **test_output_formats.py** (2 tests) - Tests for JSON and text output formats
  - JSON Lines format validation
  - Text format (strace-compatible) validation

- **test_filtering.py** (3 tests) - Tests for syscall filtering options
  (`-e trace=`)
  - Filter specific syscalls
  - Filter by syscall class (file)
  - Filter by syscall class (network)

- **test_statistics.py** (1 test) - Tests for summary statistics (`-c`)
  - Summary table generation

## Test Fixtures

- **fixtures/test_programs.py** - Python functions that trigger specific
  syscalls
- **fixtures/helpers.py** - Helper utilities for JSON/text output validation
- **base.py** - Base test case class with common setup (temp directories, etc.)

## Requirements

- **Must use `/usr/bin/python3`** (macOS system Python) - LLDB Python bindings
  only work with system Python
- Tests must be run from the package root so Python can import the
  `strace_macos` module
- All tests use Python's built-in `unittest` framework (no external
  dependencies)
