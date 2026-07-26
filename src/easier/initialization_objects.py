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
    AiAgent,
    AiLayout,
    AI_LAYOUTS,
    EASIER_CONFIG_FILENAME,
    VALID_PKG_MANAGERS,
    SKILLS_DIR,
    TEMPLATES_DIR,
    COMMON_SKILLS,
    CONVERSATION_SKILLS,
    MARIMO_SKILLS,
    JUPYTER_SKILLS,
)
from easier.errors import PackageManagerNotFoundError
from easier.cli_styling import print_figlet, print_normal_help, print_skills_help, print_start
from easier.utils import CURSOR_RULE_FRONTMATTER, write_analysis_rules

COPILOT_INSTRUCTIONS_FRONTMATTER = """\
---
applyTo: "**"
---

"""


class PrintToConsole():
    def __init__(self, notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE) -> None:
        self.notebook_type: NotebookType = notebook_type

    def create(self) -> None:
        print_figlet()
        print_normal_help()
        print_skills_help()

    def help(self) -> None:
        print_figlet()
        print_normal_help()

    def start(self) -> None:
        if self.notebook_type == "marimo":
            print_start()



class MakeDirectories():
    def __init__(self, ai_agent: AiAgent) -> None:
        self.layout: AiLayout = AI_LAYOUTS[ai_agent]

    def create(self, root: Path) -> None:
        root.mkdir()
        (root / "context").mkdir()
        (root / "context" / "other_context").mkdir()
        for relative in self.layout.root_dirs:
            (root / relative).mkdir(parents=True, exist_ok=True)


class MakeFiles():
    def __init__(self, ai_agent: AiAgent, notebook_type: NotebookType = "marimo") -> None:
        self.ai_agent: AiAgent = ai_agent
        self.notebook_type = notebook_type

    def create(self, root: Path) -> None:
        (root / "context" / "analysis_context.md").touch()
        (root / "context" / "analysis_plan.md").touch()
        (root / "context" / "analysis_progress.md").touch()
        (root / "context" / "analysis_assistant_notes.md").touch()
        (root / "context" / "analysis_user_notes.md").touch()

        rules_body = (TEMPLATES_DIR / "analysis_rules.md").read_text(encoding="utf-8")
        write_analysis_rules(root, self.ai_agent, rules_body)

        if self.notebook_type == "marimo":
            (root / "notebook.py").touch()
        elif self.notebook_type == "jupyter":
            (root / "notebook.ipynb").touch()
        else:
            raise ValueError(f"Invalid notebook type: {self.notebook_type}")


class InstallDependencies():
    def __init__(self, pkg_manager: PkgManager = DEFAULT_PKG_MANAGER):
        self.pkg_manager: PkgManager = pkg_manager

    def create(self, root: Path) -> None:
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


class RunCurlCommands():
    def __init__(
        self,
        ai_agent: AiAgent,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
    ) -> None:
        self.ai_agent: AiAgent = ai_agent
        self.notebook_type: NotebookType = notebook_type

    def create(self, root: Path) -> None:
        if self.notebook_type != "marimo":
            return

        content = self._download_marimo_docs()
        self._write_marimo_docs(root, content)

    def _download_marimo_docs(self) -> str:
        result = subprocess.run(
            [
                "curl",
                "-fsSL",
                "https://docs.marimo.io/CLAUDE.md",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def _write_marimo_docs(self, root: Path, content: str) -> None:
        if self.ai_agent == "cursor":
            path = root / ".cursor" / "rules" / "marimo.mdc"
            path.write_text(
                CURSOR_RULE_FRONTMATTER.format(description="Marimo notebook guidance")
                + content,
                encoding="utf-8",
            )
        elif self.ai_agent == "claude":
            claude_path = root / "CLAUDE.md"
            existing = claude_path.read_text(encoding="utf-8") if claude_path.is_file() else ""
            claude_path.write_text(
                existing.rstrip() + "\n\n---\n\n" + content.lstrip(),
                encoding="utf-8",
            )
        elif self.ai_agent == "codex":
            (root / ".agents" / "prompts" / "marimo.md").write_text(
                content, encoding="utf-8"
            )
        elif self.ai_agent == "copilot":
            path = root / ".github" / "instructions" / "marimo.instructions.md"
            path.write_text(
                COPILOT_INSTRUCTIONS_FRONTMATTER + content,
                encoding="utf-8",
            )
        else:
            raise ValueError(f"Invalid AI agent: {self.ai_agent}")


class InstallSkills():
    def __init__(
        self,
        ai_agent: AiAgent,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
    ) -> None:
        self.layout: AiLayout = AI_LAYOUTS[ai_agent]
        self.notebook_type: NotebookType = notebook_type

    def _copy_skills(self, root: Path, skill_names: tuple[str, ...]) -> None:
        for skill_name in skill_names:
            source = SKILLS_DIR / skill_name
            destination = root / self.layout.skills_dir / skill_name
            if not source.is_dir():
                print(
                    f"Warning: packaged skill '{skill_name}' not found at {source}; "
                    "skipping.",
                    file=sys.stderr,
                )
                continue
            shutil.copytree(source, destination, dirs_exist_ok=True)

    def create(self, root: Path) -> None:
        self._copy_skills(root, COMMON_SKILLS)
        self._copy_skills(root, CONVERSATION_SKILLS)
        if self.notebook_type == "marimo":
            self._copy_skills(root, MARIMO_SKILLS)
        elif self.notebook_type == "jupyter":
            self._copy_skills(root, JUPYTER_SKILLS)


class WriteConfig():
    def __init__(
        self,
        ai_agent: AiAgent,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
        pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
    ) -> None:
        self.ai_agent: AiAgent = ai_agent
        self.notebook_type: NotebookType = notebook_type
        self.pkg_manager: PkgManager = pkg_manager

    def create(self, root: Path) -> None:
        config_path: Path = root / EASIER_CONFIG_FILENAME
        config_path.write_text(
            f'ai_agent = "{self.ai_agent}"\n'
            f'notebook_type = "{self.notebook_type}"\n'
            f'pkg_manager = "{self.pkg_manager}"\n',
            encoding="utf-8",
        )


class RunBashCommands():
    def __init__(
        self,
        notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
        pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
    ) -> None:
        self.notebook_type: NotebookType = notebook_type
        self.pkg_manager: PkgManager = pkg_manager

    def start(self, root: Path) -> None:
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
