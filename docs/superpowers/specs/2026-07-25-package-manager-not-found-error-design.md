# Package Manager Not Found Error

## Goal

When `easier create` uses a package manager that is not installed (or not on `PATH`), show a clear message that names the selected manager, lists which supported managers are available, and suggests the correct `--pkg-manager` flag — instead of a raw `FileNotFoundError` traceback.

## Scope

In scope:

- Custom exception in a new `src/easier/errors.py`
- Pre-check in `InstallDependencies` before running install commands
- CLI catch that prints a short message and exits with code 1

Out of scope:

- Auto-switching to a detected package manager
- Wrapping `subprocess.CalledProcessError` (install failures keep the normal traceback)
- Changing the default `pkg_manager` from `poetry`

## Behavior

Before `subprocess.run` in `InstallDependencies.run`:

1. Call `shutil.which(self.pkg_manager)`.
2. If missing, scan `VALID_PKG_MANAGERS` with `shutil.which` to build `available`.
3. Raise `PackageManagerNotFoundError(selected=..., available=...)`.

Message examples:

- Selected missing, one alternative found:  
  `poetry was not found on PATH. Detected: uv. Try: easier create <project> --pkg-manager uv`
- Selected missing, none found:  
  `poetry was not found on PATH. None of the supported package managers (poetry, uv) were detected.`

Existing checks stay unchanged (`pyproject.toml` presence, invalid manager `ValueError`). Successful `which` proceeds to the existing poetry/uv install commands.

## Components

### `src/easier/errors.py`

- `PackageManagerNotFoundError(Exception)` with attributes `selected: str` and `available: list[str]`
- `__str__` builds the user-facing message described above

### `src/easier/initialization_objects.py`

- Import and raise `PackageManagerNotFoundError` when the selected binary is missing
- Do not catch `FileNotFoundError` from `subprocess.run` for this case (pre-check avoids it)

### `src/easier/cli.py`

- Catch `PackageManagerNotFoundError` around `create_project_scaffold`
- Print the exception message to stderr
- `sys.exit(1)`

## Testing notes

Manual check: with `uv` available and `poetry` not on PATH, `uv run easier create test` (default poetry) should print the custom message and exit 1 without a traceback. With `--pkg-manager uv`, install should proceed as today.
