import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich_pyfiglet import RichFiglet
from typer.core import TyperArgument, TyperOption
from typer.main import get_command
from typer.rich_utils import (
    ALIGN_COMMANDS_PANEL,
    ALIGN_OPTIONS_PANEL,
    COMMANDS_PANEL_TITLE,
    REQUIRED_SHORT_STRING,
    STYLE_COMMANDS_PANEL_BORDER,
    STYLE_COMMANDS_TABLE_BORDER_STYLE,
    STYLE_COMMANDS_TABLE_BOX,
    STYLE_COMMANDS_TABLE_FIRST_COLUMN,
    STYLE_COMMANDS_TABLE_LEADING,
    STYLE_COMMANDS_TABLE_PAD_EDGE,
    STYLE_COMMANDS_TABLE_PADDING,
    STYLE_COMMANDS_TABLE_ROW_STYLES,
    STYLE_COMMANDS_TABLE_SHOW_LINES,
    STYLE_OPTION,
    STYLE_OPTIONS_PANEL_BORDER,
    STYLE_OPTIONS_TABLE_BORDER_STYLE,
    STYLE_OPTIONS_TABLE_BOX,
    STYLE_OPTIONS_TABLE_LEADING,
    STYLE_OPTIONS_TABLE_PAD_EDGE,
    STYLE_OPTIONS_TABLE_PADDING,
    STYLE_OPTIONS_TABLE_ROW_STYLES,
    STYLE_OPTIONS_TABLE_SHOW_LINES,
    STYLE_REQUIRED_SHORT,
    STYLE_SWITCH,
    STYLE_TYPES,
    _get_parameter_help,
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


def _param_identity(param: TyperArgument | TyperOption, ctx: click.Context) -> Text:
    identity = Text(overflow="fold")
    if isinstance(param, TyperArgument):
        name = param.metavar if param.metavar is not None else (param.name or "")
        identity.append(name, style=STYLE_SWITCH)
        return identity

    long_opts = [opt for opt in param.opts if "--" in opt]
    short_opts = [opt for opt in param.opts if "--" not in opt]
    if long_opts:
        identity.append(",".join(long_opts), style=STYLE_OPTION)
    if short_opts:
        if long_opts:
            identity.append(" ")
        identity.append(",".join(short_opts), style=STYLE_SWITCH)
    return identity


def _param_type_text(param: TyperArgument | TyperOption, ctx: click.Context) -> Text:
    types_data = Text(style=STYLE_TYPES, overflow="fold")
    if isinstance(param, TyperOption):
        metavar_type = param.make_metavar(ctx=ctx)
    else:
        metavar_type = param.type.get_metavar(param=param, ctx=ctx)
        if metavar_type is None:
            metavar_type = f"<{param.type.name}>"
    if metavar_type and "bool" not in metavar_type.lower():
        types_data.append(metavar_type)
    return types_data


def _print_command_params_panel(
    *,
    command_name: str,
    params: list[TyperArgument | TyperOption],
    ctx: click.Context,
    markup_mode: str,
    console: Console,
) -> None:
    if not params:
        return

    table_styles: dict = {
        "show_lines": STYLE_OPTIONS_TABLE_SHOW_LINES,
        "leading": STYLE_OPTIONS_TABLE_LEADING,
        "box": STYLE_OPTIONS_TABLE_BOX,
        "border_style": STYLE_OPTIONS_TABLE_BORDER_STYLE,
        "row_styles": STYLE_OPTIONS_TABLE_ROW_STYLES,
        "pad_edge": STYLE_OPTIONS_TABLE_PAD_EDGE,
        "padding": STYLE_OPTIONS_TABLE_PADDING,
    }
    box_style = getattr(box, table_styles.pop("box"), None)
    params_table = Table(
        highlight=True,
        show_header=False,
        expand=True,
        box=box_style,
        **table_styles,
    )

    show_required = any(param.required for param in params)
    for param in params:
        kind = "arg" if isinstance(param, TyperArgument) else "option"
        required = (
            Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)
            if param.required
            else ""
        )
        row: list = []
        if show_required:
            row.append(required)
        row.extend(
            [
                Text(kind, style=STYLE_COMMANDS_TABLE_FIRST_COLUMN),
                _param_identity(param, ctx),
                _param_type_text(param, ctx),
                _get_parameter_help(param=param, ctx=ctx, markup_mode=markup_mode),
            ]
        )
        params_table.add_row(*row)

    console.print(
        Panel(
            params_table,
            border_style=STYLE_OPTIONS_PANEL_BORDER,
            title=command_name,
            title_align=ALIGN_OPTIONS_PANEL,
        )
    )


def print_normal_help() -> None:
    from easier.cli import app

    group = get_command(app)
    ctx = click.Context(group, info_name=group.name or "easier")
    markup_mode = getattr(group, "rich_markup_mode", None) or "rich"
    console = Console()

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
        console=console,
        cmd_len=cmd_len,
    )

    for command in commands:
        cmd_name = command.name or ""
        cmd_ctx = click.Context(command, info_name=cmd_name, parent=ctx)
        params: list[TyperArgument | TyperOption] = []
        for param in command.get_params(cmd_ctx):
            if getattr(param, "hidden", False):
                continue
            if isinstance(param, (TyperArgument, TyperOption)):
                params.append(param)

        _print_command_params_panel(
            command_name=cmd_name,
            params=params,
            ctx=cmd_ctx,
            markup_mode=markup_mode,
            console=console,
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
