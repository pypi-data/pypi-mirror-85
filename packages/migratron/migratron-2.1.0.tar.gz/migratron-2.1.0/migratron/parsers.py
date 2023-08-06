# -*- coding: utf-8 -*-

import os
import argparse
from pygments.styles import get_all_styles

from migratron import __version__
from migratron.consts import (
    MAIN_PARSER_DESCRIPTION,
    INITIALIZE_PARSER_DESCRIPTION,
    MIGRATE_PARSER_DESCRIPTION,
    CLEANUP_PARSER_DESCRIPTION,
)
from migratron.command.run_migration import ALL_MIGRATION_TYPES


def create_command_line_parser():
    """
    Creates the parser used by the 3 differents subcommands
    """
    parser = create_main_parser()
    subparser = parser.add_subparsers(dest="subparser_name")
    create_initialize_parser(subparser)
    create_run_migration_parser(subparser)
    create_cleanup(subparser)
    return parser


def create_main_parser():
    """
    Creates the main parser with the common options for all the other
    parsers
    """
    parser = argparse.ArgumentParser(
        description=MAIN_PARSER_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="version", version=__version__)
    return parser


def create_initialize_parser(subparser):
    """
    Creates the command to initialize the database
    """
    initialize_parser = subparser.add_parser(
        "initialize",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Initialize the internal database",
        description=INITIALIZE_PARSER_DESCRIPTION,
    )
    initialize_parser.add_argument(
        "--just-base-schema",
        action="store_true",
        help=(
            "Indicate that it should only create the migration "
            "database table but not mark the migrations that are already "
            "updated on the system as executed. If this value is not "
            "used then it will mark all the migrations as executed"
        ),
    )
    add_common_arguments(initialize_parser)


def create_run_migration_parser(subparser):
    """
    Creates the parser that is going to be used to mark the
    currrent migration as executed
    """
    migrate_parser = subparser.add_parser(
        "migrate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Run the missing migrations",
        description=MIGRATE_PARSER_DESCRIPTION,
    )

    migrate_parser.add_argument(
        "--migration-type",
        choices=(ALL_MIGRATION_TYPES, "pre", "post"),
        required=True,
        help=(
            "Inidicate the type of migrations that should be executed. "
            "The any choice will execute PRE and POST migrations"
        ),
    )
    migrate_parser.add_argument(
        "--db-type",
        choices=("postgresql", "hive", "presto"),
        required=False,
        default="postgresql",
        help=(
            "Inidicate the type of database on which the migration should be executed."
        ),
    )
    migrate_parser.add_argument(
        "--db-uri",
        required=False,
        help=(
            "The URL of the database on which the migrations are going to be executed. "
            "As with the ``state-db-uri``, when using Postgres it supports the "
            "Postgres environment variables. But for the other databases this value "
            "is required"
        ),
    )
    migrate_parser.add_argument(
        "--just-list-files",
        action="store_true",
        help=(
            "Just list the files that are missing and that should be "
            "migrated. This will not print the content of the files"
        ),
    )
    migrate_parser.add_argument(
        "--additional-options",
        required=False,
        nargs="*",
        help=(
            "When running the psql, beeline or presto-cli to run the command, the additional "
            "options that should be used on the command (with the --). "
            '--additional-options "--single-step single-transaction" or'
            '--additional-options "--catalog hive --schema foobar --user foo"'
        ),
    )
    add_common_arguments(migrate_parser)


def create_cleanup(subparser):
    """
    Creates the option for the cleanup parser
    """
    cleanup_parser = subparser.add_parser(
        "cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Cleanup a failed migration",
        description=CLEANUP_PARSER_DESCRIPTION,
    )
    add_common_arguments(cleanup_parser)


def add_common_arguments(parser):
    """
    Add the common parameters to the parser
    """
    parser.add_argument(
        "--state-db-uri",
        required=False,
        default="",
        help=(
            "The URI used to connect to the postgres database. It must be  "
            "of the format: postgres://username:password@host:port/dbname. If "
            "not used then it will use the environment variables to "
            "connect to the database ( "
            "https://www.postgresql.org/docs/current/static/libpq-envars.html). "
            "This is the database that has the status of the executed migrations "
        ),
    )
    parser.add_argument(
        "--batch-mode",
        action="store_true",
        help=(
            "If used this option, then the migration system will run "
            "wihtout asking for any confirmation. By default, before "
            "running any migration, it will ask for the user to "
            "confirm the action"
        ),
    )
    parser.add_argument(
        "--use-colors",
        action="store_true",
        help=(
            "If used this option, then when confirming the action, the "
            "output will be colored"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Don't update the schema of the database. Just print the "
            "SQL that is going to be executed"
        ),
    )
    parser.add_argument(
        "--color-style",
        choices=[x for x in get_all_styles()],
        default="vim",
        help=("When using the color output, then this is the color" "style to use"),
    )
    parser.add_argument(
        "--logging-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="DEBUG",
        help="The logging level to use",
    )
    migrations_path = os.environ.get("DB_UTILS_MIGRATIONS_PATH")
    parser.add_argument(
        "--migrations-path",
        help="The path where the different migrations files can be found",
        required=migrations_path is None,
        default=migrations_path,
    )
