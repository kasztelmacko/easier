from typing import Annotated

import click
import typer
from typer.core import TyperGroup

from easier.scaffold import (
    create_analysis_scaffold,
    start_analysis
)
from easier.config import (
    VALID_NOTEBOOK_TYPES,
    VALID_PKG_MANAGERS,
    VALID_AI_AGENTS,
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
    AiAgent,
    NotebookType,
    PkgManager,
)
from easier.utils import (
    run_command,
    parse_ai_agent,
    parse_notebook_type,
    parse_pkg_manager,
)
from easier.initialization_objects import PrintToConsole


class EasierTyperGroup(TyperGroup):
    """Thin hook: delegates all help rendering to PrintToConsole."""

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        PrintToConsole().help()


app = typer.Typer(
    cls=EasierTyperGroup,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)


@app.command()
def create(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name for analysis to create inside the current project"),
    ],
    ai_agent: Annotated[
        AiAgent,
        typer.Option(
            "--ai",
            "-a",
            help="AI agent whose native skills/rules layout to scaffold",
            parser=parse_ai_agent,
            metavar="|".join(VALID_AI_AGENTS),
        ),
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
    """Scaffold a analysis structure inside the current project and add shared dependencies."""
    run_command(
        lambda: create_analysis_scaffold(
            analysis_name=analysis_name,
            ai_agent=ai_agent,
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
