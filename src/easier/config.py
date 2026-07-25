from typing import Literal

REQUIRED_DEPENDENCIES = (
    "marimo>=0.23.15",
    "pandas",
    "plotly",
)

NotebookType = Literal["marimo", "jupyter"]
PkgManager = Literal["poetry", "uv"]

VALID_NOTEBOOK_TYPES: tuple[NotebookType, ...] = ("marimo", "jupyter")
VALID_PKG_MANAGERS: tuple[PkgManager, ...] = ("poetry", "uv")

DEFAULT_NOTEBOOK_TYPE: NotebookType = "marimo"
DEFAULT_PKG_MANAGER: PkgManager = "poetry"