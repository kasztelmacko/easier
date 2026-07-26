import tomllib
import sys
from typing import Callable, Sequence, cast
import typer
from pathlib import Path
from typing import Any
from easier.config import (
    VALID_NOTEBOOK_TYPES,
    VALID_PKG_MANAGERS,
    VALID_AI_AGENTS,
    AiAgent,
    NotebookType,
    PkgManager,
    EASIER_CONFIG_FILENAME,
    SKILLS_DIR,
)

CURSOR_RULE_FRONTMATTER = """\
---
description: {description}
alwaysApply: true
---

"""
from easier.errors import (
    InvalidAnalysisConfigError,
    AnalysisConfigNotFoundError,
    AnalysisNotFoundError,
    PackageManagerNotFoundError,
)

CLI_ERRORS = (
    PackageManagerNotFoundError,
    AnalysisNotFoundError,
    AnalysisConfigNotFoundError,
    InvalidAnalysisConfigError,
    ValueError,
)

def run_command(action: Callable[[], None]) -> None:
    try:
        action()
    except CLI_ERRORS as exc:
        print(exc, file=sys.stderr)
        raise typer.Exit(1) from None


def parse_choice(value: str, valid: Sequence[str]) -> str:
    normalized = value.lower()
    if normalized not in valid:
        choices = ", ".join(repr(item) for item in valid)
        raise typer.BadParameter(f"'{value}' is not one of {choices}.")
    return normalized


def parse_notebook_type(value: str) -> NotebookType:
    return cast(NotebookType, parse_choice(value, VALID_NOTEBOOK_TYPES))


def parse_pkg_manager(value: str) -> PkgManager:
    return cast(PkgManager, parse_choice(value, VALID_PKG_MANAGERS))


def parse_ai_agent(value: str) -> AiAgent:
    return cast(AiAgent, parse_choice(value, VALID_AI_AGENTS))


def write_analysis_rules(root: Path, ai_agent: AiAgent, body: str) -> None:
    if ai_agent == "cursor":
        path = root / ".cursor" / "rules" / "analysis_rules.mdc"
        path.write_text(
            CURSOR_RULE_FRONTMATTER.format(description="Analysis workspace conventions")
            + body,
            encoding="utf-8",
        )
    elif ai_agent == "claude":
        (root / "CLAUDE.md").write_text(body, encoding="utf-8")
    elif ai_agent == "codex":
        (root / ".agents" / "prompts" / "analysis_rules.md").write_text(
            body, encoding="utf-8"
        )
    elif ai_agent == "copilot":
        (root / ".github" / "copilot-instructions.md").write_text(
            body, encoding="utf-8"
        )
    else:
        raise ValueError(f"Invalid AI agent: {ai_agent}")


def read_skill_description(skill_name: str) -> str:
    """Return the one-line frontmatter description from a packaged skill."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        return ""

    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ""

    end = text.find("\n---", 3)
    if end == -1:
        return ""

    for line in text[3:end].splitlines():
        stripped = line.strip()
        if stripped.startswith("description:"):
            value = stripped[len("description:") :].strip()
            if value.startswith((">", "|")):
                return ""
            return value.strip("\"'")
    return ""


def load_analysis_config(root: Path) -> tuple[NotebookType, PkgManager]:
    if not root.is_dir():
        raise AnalysisNotFoundError(project_root=root)

    config_path: Path = root / EASIER_CONFIG_FILENAME
    if not config_path.is_file():
        raise AnalysisConfigNotFoundError(config_path=config_path)

    with config_path.open("rb") as config_file:
        data: dict[str, Any] = tomllib.load(config_file)

    notebook_type: NotebookType | None = data.get("notebook_type")
    pkg_manager: PkgManager | None = data.get("pkg_manager")
    ai_agent = data.get("ai_agent")

    if notebook_type not in VALID_NOTEBOOK_TYPES:
        raise InvalidAnalysisConfigError(
            config_path=config_path,
            reason=f"invalid or missing notebook_type {notebook_type!r}",
        )
    if pkg_manager not in VALID_PKG_MANAGERS:
        raise InvalidAnalysisConfigError(
            config_path=config_path,
            reason=f"invalid or missing pkg_manager {pkg_manager!r}",
        )
    # ai_agent is optional for scaffolds created before --ai existed
    if ai_agent is not None and ai_agent not in VALID_AI_AGENTS:
        raise InvalidAnalysisConfigError(
            config_path=config_path,
            reason=f"invalid ai_agent {ai_agent!r}",
        )

    return notebook_type, pkg_manager