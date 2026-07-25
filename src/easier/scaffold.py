from easier.initialization_objects import (
    MakeDirectories,
    MakeFiles,
    InstallDependencies,
    InstallSkills,
    RunCurlCommands,
    RunBashCommands,
    WriteConfig,
    load_project_config,
)
from pathlib import Path
from easier.config import (
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
    NotebookType,
    PkgManager,
)


def create_project_scaffold(
    analysis_name: str,
    notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
    pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
) -> None:
    project_root = Path.cwd()
    scaffold_root = project_root / analysis_name

    InstallDependencies(pkg_manager=pkg_manager).run(root=project_root)
    MakeDirectories().run(root=scaffold_root)
    MakeFiles(notebook_type=notebook_type).run(root=scaffold_root)
    RunCurlCommands().run(root=scaffold_root)
    InstallSkills(notebook_type=notebook_type).run(root=scaffold_root)
    WriteConfig(notebook_type=notebook_type, pkg_manager=pkg_manager).run(
        root=scaffold_root
    )


def start_analysis(analysis_name: str) -> None:
    project_root = Path.cwd()
    scaffold_root = project_root / analysis_name
    notebook_type, pkg_manager = load_project_config(scaffold_root)
    RunBashCommands(notebook_type=notebook_type, pkg_manager=pkg_manager).run(
        root=scaffold_root
    )
