from dataclasses import dataclass
from typing import Literal
from pathlib import Path


EASIER_CONFIG_FILENAME: str = ".easier.toml"
SKILLS_DIR: Path = Path(__file__).resolve().parent / "skills"
TEMPLATES_DIR: Path = Path(__file__).resolve().parent / "templates"

REQUIRED_DEPENDENCIES: tuple[str, ...] = (
    "marimo>=0.23.15",
    "pandas",
    "plotly",
)
COMMON_SKILLS: tuple[str, ...] = ("data-science-expert", "deep-research",)
CONVERSATION_SKILLS: tuple[str, ...] = ("plan", "plan-revise", "summarize")
MARIMO_SKILLS: tuple[str, ...] = ("marimo-pair", "marimo-notebook", "anywidget-generator",)
JUPYTER_SKILLS: tuple[str, ...] = ("jupyter-notebook",)

NotebookType = Literal["marimo", "jupyter"]
PkgManager = Literal["poetry", "uv"]
AiAgent = Literal["cursor", "claude", "codex", "copilot"]

VALID_NOTEBOOK_TYPES: tuple[NotebookType, ...] = ("marimo", "jupyter")
VALID_PKG_MANAGERS: tuple[PkgManager, ...] = ("poetry", "uv")
VALID_AI_AGENTS: tuple[AiAgent, ...] = ("cursor", "claude", "codex", "copilot")

DEFAULT_NOTEBOOK_TYPE: NotebookType = "marimo"
DEFAULT_PKG_MANAGER: PkgManager = "poetry"


@dataclass(frozen=True)
class AiLayout:
    """Per-agent paths relative to the analysis root."""

    root_dirs: tuple[Path, ...]
    skills_dir: Path


AI_LAYOUTS: dict[AiAgent, AiLayout] = {
    "cursor": AiLayout(
        root_dirs=(Path(".cursor"), Path(".cursor") / "rules", Path(".cursor") / "skills"),
        skills_dir=Path(".cursor") / "skills",
    ),
    "claude": AiLayout(
        root_dirs=(Path(".claude"), Path(".claude") / "skills"),
        skills_dir=Path(".claude") / "skills",
    ),
    "codex": AiLayout(
        root_dirs=(
            Path(".agents"),
            Path(".agents") / "prompts",
            Path(".agents") / "skills",
        ),
        skills_dir=Path(".agents") / "skills",
    ),
    "copilot": AiLayout(
        root_dirs=(
            Path(".github"),
            Path(".github") / "skills",
            Path(".github") / "instructions",
        ),
        skills_dir=Path(".github") / "skills",
    ),
}
