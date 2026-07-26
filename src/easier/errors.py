from easier.config import VALID_NOTEBOOK_TYPES, VALID_PKG_MANAGERS, VALID_AI_AGENTS
from pathlib import Path


class PackageManagerNotFoundError(Exception):
    def __init__(self, selected: str, available: list[str]) -> None:
        self.selected = selected
        self.available = available
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        supported = ", ".join(VALID_PKG_MANAGERS)
        if self.available:
            detected = ", ".join(self.available)
            suggestion = ", ".join(
                f"easier create <analysis> --pkg-manager {name}"
                for name in self.available
            )
            return (
                f"{self.selected} was not found on PATH. "
                f"Detected: {detected}. Try: {suggestion}"
            )
        return (
            f"{self.selected} was not found on PATH. "
            f"None of the supported package managers ({supported}) were detected."
        )


class AnalysisNotFoundError(Exception):
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        super().__init__(
            f"Analysis folder not found: {project_root}. "
            "Run `easier create <analysis_name>` first."
        )


class AnalysisConfigNotFoundError(Exception):
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        super().__init__(
            f"Analysis config not found: {config_path}. "
            "Run `easier create <analysis_name>` first."
        )


class InvalidAnalysisConfigError(Exception):
    def __init__(self, config_path: Path, reason: str) -> None:
        self.config_path = config_path
        self.reason = reason
        valid_notebooks = ", ".join(VALID_NOTEBOOK_TYPES)
        valid_pkg_managers = ", ".join(VALID_PKG_MANAGERS)
        valid_ai_agents = ", ".join(VALID_AI_AGENTS)
        super().__init__(
            f"Invalid analysis config at {config_path}: {reason}. "
            f"Expected notebook_type in ({valid_notebooks}), "
            f"pkg_manager in ({valid_pkg_managers}), "
            f"and optional ai_agent in ({valid_ai_agents})."
        )
