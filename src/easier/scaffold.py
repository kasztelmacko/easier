from easier.initialization_objects import MakeDirectories, MakeFiles, InstallDependencies, RunCurlCommands
from pathlib import Path
from typing import Literal


def create_project_scaffold(
    project_name: str,
    notebook_type: Literal["marimo", "jupyter"] = "marimo",
    pkg_manager: Literal["poetry", "uv"] = "poetry",
) -> None:
    project_root = Path.cwd()
    scaffold_root = project_root / project_name

    MakeDirectories().run(root=scaffold_root)
    MakeFiles(notebook_type=notebook_type).run(root=scaffold_root)
    RunCurlCommands().run(root=scaffold_root)
    InstallDependencies(pkg_manager=pkg_manager).run(root=project_root)