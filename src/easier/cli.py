from typing import Annotated

import typer

from easier.scaffold import (
    create_project_scaffold,
    start_analysis
)
from easier.config import (
    VALID_NOTEBOOK_TYPES,
    VALID_PKG_MANAGERS,
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
    NotebookType,
    PkgManager,
)
from easier.utils import run_command, parse_notebook_type, parse_pkg_manager

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)


@app.command()
def create(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name for analysis to create inside the current project"),
    ],
    notebook_type: Annotated[
        NotebookType,
        typer.Option(
            "--notebook-type",
            "-n",
            help="The type of notebook to create",
            parser=parse_notebook_type,
            metavar="|".join(VALID_NOTEBOOK_TYPES),
        ),
    ] = DEFAULT_NOTEBOOK_TYPE,
    pkg_manager: Annotated[
        PkgManager,
        typer.Option(
            "--pkg-manager",
            "-p",
            help="The package manager to use",
            parser=parse_pkg_manager,
            metavar="|".join(VALID_PKG_MANAGERS),
        ),
    ] = DEFAULT_PKG_MANAGER,
) -> None:
    """Scaffold a folder inside the current project and add shared dependencies."""
    run_command(
        lambda: create_project_scaffold(
            analysis_name=analysis_name,
            notebook_type=notebook_type,
            pkg_manager=pkg_manager,
        )
    )


@app.command()
def start(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name for analysis to start in"),
    ],
) -> None:
    """Start the analysis."""
    run_command(lambda: start_analysis(analysis_name=analysis_name))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
