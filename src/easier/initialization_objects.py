from pathlib import Path
import shutil
import subprocess
import sys
from easier.config import (
    REQUIRED_DEPENDENCIES,
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
    NotebookType,
    PkgManager,
    EASIER_CONFIG_FILENAME,
    VALID_PKG_MANAGERS,
    SKILLS_DIR,
    COMMON_SKILLS,
    MARIMO_SKILLS,
    JUPYTER_SKILLS,
)
from easier.errors import PackageManagerNotFoundError
from easier.utils import load_project_config

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
            available: list[PkgManager] = [
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


class InstallSkills(Step):
    def __init__(self, notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE) -> None:
        self.notebook_type: NotebookType = notebook_type

    def _copy_skills(self, root: Path, skill_names: tuple[str, ...]) -> None:
        for skill_name in skill_names:
            source = SKILLS_DIR / skill_name
            destination = root / ".agents" / "skills" / skill_name
            if not source.is_dir():
                print(
                    f"Warning: packaged skill '{skill_name}' not found at {source}; "
                    "skipping.",
                    file=sys.stderr,
                )
                continue
            shutil.copytree(source, destination, dirs_exist_ok=True)

    def run(self, root: Path) -> None:
        self._copy_skills(root, COMMON_SKILLS)
        if self.notebook_type == "marimo":
            self._copy_skills(root, MARIMO_SKILLS)
        elif self.notebook_type == "jupyter":
            self._copy_skills(root, JUPYTER_SKILLS)


class WriteConfig(Step):
    def __init__(
        self,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
        pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
    ) -> None:
        self.notebook_type: NotebookType = notebook_type
        self.pkg_manager: PkgManager = pkg_manager

    def run(self, root: Path) -> None:
        config_path: Path = root / EASIER_CONFIG_FILENAME
        config_path.write_text(
            f'notebook_type = "{self.notebook_type}"\n'
            f'pkg_manager = "{self.pkg_manager}"\n',
            encoding="utf-8",
        )


class RunBashCommands(Step):
    def __init__(
        self,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
        pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
    ) -> None:
        self.notebook_type: NotebookType = notebook_type
        self.pkg_manager: PkgManager = pkg_manager

    def run(self, root: Path) -> None:
        if self.notebook_type == "marimo":
            subprocess.run(
                [self.pkg_manager, "run", "marimo", "edit", "--watch", "notebook.py"],
                cwd=root,
                check=True,
            )
        elif self.notebook_type == "jupyter":
            subprocess.run(
                [self.pkg_manager, "run", "jupyter", "notebook.ipynb"],
                cwd=root,
                check=True,
            )
        else:
            raise ValueError(f"Invalid notebook type: {self.notebook_type}")
