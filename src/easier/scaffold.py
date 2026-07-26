from easier.initialization_objects import (
    PrintToConsole,
    MakeDirectories,
    MakeFiles,
    InstallDependencies,
    InstallSkills,
    RunCurlCommands,
    RunBashCommands,
    WriteConfig,
)
from easier.utils import load_analysis_config
from pathlib import Path
from easier.config import (
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
    AiAgent,
    NotebookType,
    PkgManager,
)


def create_analysis_scaffold(
    analysis_name: str,
    ai_agent: AiAgent,
    notebook_type: NotebookType = DEFAULT_NOTEBOOK_TYPE,
    pkg_manager: PkgManager = DEFAULT_PKG_MANAGER,
) -> None:
    project_root = Path.cwd()
    analysis_root = project_root / analysis_name

    InstallDependencies(pkg_manager=pkg_manager).create(root=project_root)
    PrintToConsole().create()
    MakeDirectories(ai_agent=ai_agent).create(root=analysis_root)
    MakeFiles(ai_agent=ai_agent, notebook_type=notebook_type).create(root=analysis_root)
    RunCurlCommands(ai_agent=ai_agent, notebook_type=notebook_type).create(
        root=analysis_root
    )
    InstallSkills(ai_agent=ai_agent, notebook_type=notebook_type).create(
        root=analysis_root
    )
    WriteConfig(
        ai_agent=ai_agent,
        notebook_type=notebook_type,
        pkg_manager=pkg_manager,
    ).create(root=analysis_root)


def start_analysis(analysis_name: str) -> None:
    project_root = Path.cwd()
    analysis_root = project_root / analysis_name
    notebook_type, pkg_manager = load_analysis_config(analysis_root)
    PrintToConsole(notebook_type=notebook_type).start()
    RunBashCommands(notebook_type=notebook_type, pkg_manager=pkg_manager).start(
        root=analysis_root
    )
