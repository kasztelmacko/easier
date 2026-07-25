from easier.scaffold import create_project_scaffold
import argparse
import sys
from easier.config import (
    VALID_NOTEBOOK_TYPES, 
    VALID_PKG_MANAGERS, 
    DEFAULT_NOTEBOOK_TYPE, 
    DEFAULT_PKG_MANAGER
)
from easier.errors import PackageManagerNotFoundError


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
        choices=VALID_NOTEBOOK_TYPES,
        help="The type of notebook to create",
        default=DEFAULT_NOTEBOOK_TYPE,
    )
    create_parser.add_argument(
        "--pkg-manager",
        type=str.lower,
        choices=VALID_PKG_MANAGERS,
        help="The package manager to use",
        default=DEFAULT_PKG_MANAGER,
    )

    args = parser.parse_args()

    if args.command == "create":
        try:
            create_project_scaffold(
                project_name=args.project_name,
                notebook_type=args.notebook_type,
                pkg_manager=args.pkg_manager,
            )
        except PackageManagerNotFoundError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
