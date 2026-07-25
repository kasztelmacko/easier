from typing import Literal
from pathlib import Path


EASIER_CONFIG_FILENAME: str = ".easier.toml"
SKILLS_DIR: Path = Path(__file__).resolve().parent / "skills"

REQUIRED_DEPENDENCIES: tuple[str, ...] = (
    "marimo>=0.23.15",
    "pandas",
    "plotly",
)
COMMON_SKILLS: tuple[str, ...] = ("data-science-expert", "deep-research",)
MARIMO_SKILLS: tuple[str, ...] = ("marimo-pair", "marimo-notebook", "anywidget-generator",)
JUPYTER_SKILLS: tuple[str, ...] = ("jupyter-notebook",)

NotebookType = Literal["marimo", "jupyter"]
PkgManager = Literal["poetry", "uv"]

VALID_NOTEBOOK_TYPES: tuple[NotebookType, ...] = ("marimo", "jupyter")
VALID_PKG_MANAGERS: tuple[PkgManager, ...] = ("poetry", "uv")

DEFAULT_NOTEBOOK_TYPE: NotebookType = "marimo"
DEFAULT_PKG_MANAGER: PkgManager = "poetry"