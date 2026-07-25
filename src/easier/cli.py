from easier.scaffold import (
    create_project_scaffold, 
    start_analysis, 
    summarise_analysis, 
    plan_analysis,
)
import argparse
import sys
from easier.config import (
    VALID_NOTEBOOK_TYPES,
    VALID_PKG_MANAGERS,
    DEFAULT_NOTEBOOK_TYPE,
    DEFAULT_PKG_MANAGER,
)
from easier.errors import (
    InvalidAnalysisConfigError,
    PackageManagerNotFoundError,
    AnalysisConfigNotFoundError,
    AnalysisNotFoundError,
)

def create_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    create_parser = subparsers.add_parser(
        "create",
        help="Scaffold a folder inside the current project and add shared dependencies",
    )
    create_parser.add_argument(
        "analysis_name",
        type=str,
        help="Folder name for analysis to create inside the current project",
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
    return create_parser

def start_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    start_parser = subparsers.add_parser(
        "start",
        help="Start the analysis",
    )
    start_parser.add_argument(
        "analysis_name",
        type=str,
        help="Folder name for analysis to start in",
    )
    return start_parser

def plan_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    plan_parser = subparsers.add_parser(
        "plan",
        help="Plan the analysis",
    )
    plan_parser.add_argument(
        "analysis_name",
        type=str,
        help="Folder name for analysis to plan",
    )
    return plan_parser

def summarise_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    summarise_parser = subparsers.add_parser(
        "summarise",
        help="Summarise the analysis",
    )
    summarise_parser.add_argument(
        "analysis_name",
        type=str,
        help="Folder name for analysis to summarise",
    )
    return summarise_parser

def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser(subparsers)
    start_parser(subparsers)
    summarise_parser(subparsers)
    plan_parser(subparsers)

    args = parser.parse_args()
    if args.command == "create":
        try:
            create_project_scaffold(
            analysis_name=args.analysis_name,
            notebook_type=args.notebook_type,
            pkg_manager=args.pkg_manager,
        )
        except (PackageManagerNotFoundError, AnalysisNotFoundError, AnalysisConfigNotFoundError, InvalidAnalysisConfigError, ValueError) as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "start":
        try:
            start_analysis(analysis_name=args.analysis_name)
        except (AnalysisNotFoundError, AnalysisConfigNotFoundError, InvalidAnalysisConfigError, ValueError) as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)

    elif args.command == "summarise":
        try:
            summarise_analysis(analysis_name=args.analysis_name)
        except (AnalysisNotFoundError, AnalysisConfigNotFoundError, InvalidAnalysisConfigError, ValueError) as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)

    elif args.command == "plan":
        try:
            plan_analysis(analysis_name=args.analysis_name)
        except (AnalysisNotFoundError, AnalysisConfigNotFoundError, InvalidAnalysisConfigError, ValueError) as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
