from pathlib import Path
import shutil
import subprocess
from easier.config import (
    REQUIRED_DEPENDENCIES,
    VALID_PKG_MANAGERS,
    DEFAULT_PKG_MANAGER,
    NotebookType,
    PkgManager,
)
from easier.errors import PackageManagerNotFoundError


class Step:
    def run(self, root: Path) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class MakeDirectories(Step):
    def run(self, root: Path) -> None:
        root.mkdir()
        (root / "context").mkdir()
        (root / ".agents").mkdir()
        (root / ".agents" / "prompts").mkdir()
        (root / ".agents" / "skills").mkdir()


class MakeFiles(Step):
    def __init__(self, notebook_type: NotebookType = "marimo"):
        self.notebook_type = notebook_type

    def run(self, root: Path) -> None:
        (root / "context" / "analysis_context.md").touch()
        (root / "context" / "analysis_progress.md").touch()
        (root / "context" / "analysis_notes.md").touch()

        if self.notebook_type == "marimo":
            (root / "notebook.py").touch()
        elif self.notebook_type == "jupyter":
            (root / "notebook.ipynb").touch()
        else:
            raise ValueError(f"Invalid notebook type: {self.notebook_type}")


class InstallDependencies(Step):
    def __init__(self, pkg_manager: PkgManager = DEFAULT_PKG_MANAGER):
        self.pkg_manager: PkgManager = pkg_manager

    def run(self, root: Path) -> None:
        if not (root / "pyproject.toml").is_file():
            raise FileNotFoundError(
                f"No pyproject.toml found in {root}. "
                "Run easier create from an existing poetry/uv project root."
            )

        if shutil.which(self.pkg_manager) is None:
            available = [
                name for name in VALID_PKG_MANAGERS if shutil.which(name) is not None
            ]
            raise PackageManagerNotFoundError(
                selected=self.pkg_manager,
                available=available,
            )

        if self.pkg_manager == "poetry":
            subprocess.run(
                ["poetry", "add", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        elif self.pkg_manager == "uv":
            subprocess.run(
                ["uv", "pip", "install", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        else:
            raise ValueError(f"Invalid package manager: {self.pkg_manager}")

class RunCurlCommands(Step):
    def run(self, root: Path) -> None:
        subprocess.run(
            [
                "curl",
                "-fsSL",
                "https://docs.marimo.io/CLAUDE.md",
                "-o",
                str(root / ".agents" / "prompts" / "marimo.md"),
            ],
            check=True,
        )
