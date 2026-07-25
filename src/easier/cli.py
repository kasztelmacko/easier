from easier.scaffold import create_project_scaffold
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser(
        "create",
        help="Scaffold a folder inside the current project and add shared dependencies",
    )
    create_parser.add_argument(
        "project_name",
        type=str,
        help="Folder name to create inside the current project",
    )
    create_parser.add_argument(
        "--notebook-type",
        type=str.lower,
        choices=["marimo", "jupyter"],
        help="The type of notebook to create",
        default="marimo",
    )
    create_parser.add_argument(
        "--pkg-manager",
        type=str.lower,
        choices=["poetry", "uv"],
        help="The package manager to use",
        default="poetry",
    )

    args = parser.parse_args()

    if args.command == "create":
        create_project_scaffold(
            project_name=args.project_name,
            notebook_type=args.notebook_type,
            pkg_manager=args.pkg_manager,
        )
