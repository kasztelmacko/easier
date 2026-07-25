import tomllib
from pathlib import Path
from typing import Any
from easier.config import (
    VALID_NOTEBOOK_TYPES,
    VALID_PKG_MANAGERS,
    NotebookType,
    PkgManager,
    EASIER_CONFIG_FILENAME,
)
from easier.errors import (
    InvalidAnalysisConfigError,
    AnalysisConfigNotFoundError,
    AnalysisNotFoundError,
)

def load_project_config(root: Path) -> tuple[NotebookType, PkgManager]:
    if not root.is_dir():
        raise AnalysisNotFoundError(project_root=root)

    config_path: Path = root / EASIER_CONFIG_FILENAME
    if not config_path.is_file():
        raise AnalysisConfigNotFoundError(config_path=config_path)

    with config_path.open("rb") as config_file:
        data: dict[str, Any] = tomllib.load(config_file)

    notebook_type: NotebookType | None = data.get("notebook_type")
    pkg_manager: PkgManager | None = data.get("pkg_manager")

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

    return notebook_type, pkg_manager