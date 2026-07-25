from pathlib import Path
import subprocess
from typing import Literal
from easier.config import REQUIRED_DEPENDENCIES


class Step:
    def run(self, root: Path) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class MakeDirectories(Step):
    def run(self, root: Path) -> None:
        root.mkdir()
        (root / "context").mkdir()
        (root / ".claude").mkdir()
        (root / ".claude" / "prompts").mkdir()


class MakeFiles(Step):
    def __init__(self, notebook_type: Literal["marimo", "jupyter"] = "marimo"):
        self.notebook_type = notebook_type

    def run(self, root: Path) -> None:
        if self.notebook_type == "marimo":
            (root / "notebook.py").touch()
        elif self.notebook_type == "jupyter":
            (root / "notebook.ipynb").touch()
        else:
            raise ValueError(f"Invalid notebook type: {self.notebook_type}")


class InstallDependencies(Step):
    def __init__(self, pkg_manager: Literal["poetry", "uv"] = "poetry"):
        self.pkg_manager = pkg_manager

    def run(self, root: Path) -> None:
        if not (root / "pyproject.toml").is_file():
            raise FileNotFoundError(
                f"No pyproject.toml found in {root}. "
                "Run easier create from an existing poetry/uv project root."
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
                str(root / ".claude" / "prompts" / "marimo.md"),
            ],
            check=True,
        )
