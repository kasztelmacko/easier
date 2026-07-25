# Design: easier create as project addon

Date: 2026-07-25

## Goal

`easier create <folder>` scaffolds a folder inside an existing Poetry/uv project and adds shared deps to that project’s environment. It must not create a nested project or nested `.venv`.

## Behavior

1. Require a `pyproject.toml` in the current working directory (the host project).
2. Create `./<folder>/` with `context/`, `.claude/prompts/`, and a notebook (`notebook.py` or `notebook.ipynb`).
3. Do **not** write a nested `pyproject.toml` or `README.md`.
4. Add deps at the host project root:
   - poetry (default): `poetry add marimo>=0.23.15 pandas plotly`
   - uv: `uv add marimo>=0.23.15 pandas plotly`
5. Keep `--pkg-manager` default as `poetry`.

## Out of scope

Standalone nested projects, dual-mode CLI flags.
