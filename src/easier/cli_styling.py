import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich_pyfiglet import RichFiglet
from typer.main import get_command
from typer.rich_utils import (
    ALIGN_COMMANDS_PANEL,
    COMMANDS_PANEL_TITLE,
    STYLE_COMMANDS_PANEL_BORDER,
    STYLE_COMMANDS_TABLE_BORDER_STYLE,
    STYLE_COMMANDS_TABLE_BOX,
    STYLE_COMMANDS_TABLE_FIRST_COLUMN,
    STYLE_COMMANDS_TABLE_LEADING,
    STYLE_COMMANDS_TABLE_PAD_EDGE,
    STYLE_COMMANDS_TABLE_PADDING,
    STYLE_COMMANDS_TABLE_ROW_STYLES,
    STYLE_COMMANDS_TABLE_SHOW_LINES,
    _print_commands_panel,
    box,
)

from easier.config import CONVERSATION_SKILLS
from easier.utils import read_skill_description


def print_figlet() -> None:
    console = Console()
    rich_fig = RichFiglet(
        text="easier",
        font="ansi_shadow",
        colors=["white"],
    )
    console.print(rich_fig)


def print_start() -> None:
    console = Console()
    console.print(
        Panel(
            Text.from_markup(
                "To allow your agent to interact with the notebook, remember to run\n"
                "[bold]`/marimo-pair pair with me on notebook.py`[/bold]"
            ),
            title="Start the analysis",
            border_style="white",
            padding=(1, 1),
        ),
    )

def print_normal_help() -> None:
    from easier.cli import app

    group = get_command(app)
    ctx = click.Context(group, info_name=group.name or "easier")
    markup_mode = getattr(group, "rich_markup_mode", None) or "rich"

    commands = [
        command
        for name in group.list_commands(ctx)
        if (command := group.get_command(ctx, name)) is not None and not command.hidden
    ]
    if not commands:
        return

    cmd_len = max((len(command.name or "") for command in commands), default=0)
    _print_commands_panel(
        name=COMMANDS_PANEL_TITLE,
        commands=commands,
        markup_mode=markup_mode,
        console=Console(),
        cmd_len=cmd_len,
    )


def print_skills_help() -> None:
    """Print a Skills panel matching Typer's Commands help style."""
    console = Console()
    table_styles: dict = {
        "show_lines": STYLE_COMMANDS_TABLE_SHOW_LINES,
        "leading": STYLE_COMMANDS_TABLE_LEADING,
        "box": STYLE_COMMANDS_TABLE_BOX,
        "border_style": STYLE_COMMANDS_TABLE_BORDER_STYLE,
        "row_styles": STYLE_COMMANDS_TABLE_ROW_STYLES,
        "pad_edge": STYLE_COMMANDS_TABLE_PAD_EDGE,
        "padding": STYLE_COMMANDS_TABLE_PADDING,
    }
    box_style = getattr(box, table_styles.pop("box"), None)
    skills_table = Table(
        highlight=False,
        show_header=False,
        expand=True,
        box=box_style,
        **table_styles,
    )
    name_width = max((len(name) for name in CONVERSATION_SKILLS), default=0)
    skills_table.add_column(
        style=STYLE_COMMANDS_TABLE_FIRST_COLUMN,
        no_wrap=True,
        width=name_width,
    )
    skills_table.add_column("Description", justify="left", no_wrap=False, ratio=10)

    for skill_name in CONVERSATION_SKILLS:
        description = read_skill_description(skill_name) or ""
        skills_table.add_row(Text(skill_name), description)

    if skills_table.row_count:
        console.print(
            Panel(
                skills_table,
                border_style=STYLE_COMMANDS_PANEL_BORDER,
                title="Skills",
                title_align=ALIGN_COMMANDS_PANEL,
            )
        )
