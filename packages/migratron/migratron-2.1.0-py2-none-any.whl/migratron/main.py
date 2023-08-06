# -*- coding: utf-8 -*-

from migratron.parsers import create_command_line_parser
from migratron.command.initialize import InitializeCommand
from migratron.command.run_migration import RunMigrationCommand
from migratron.command.cleanup import CleanupCommand


def main(args=None):
    """ Entrypoint when you run `migratron` on the console
    """
    parser = create_command_line_parser()
    parsed_args = parser.parse_args(args=args)
    subparser_name = parsed_args.subparser_name
    if not subparser_name:
        parser.print_help()
        parser.exit(1)

    subparser_class = dict(
        initialize=InitializeCommand,
        migrate=RunMigrationCommand,
        cleanup=CleanupCommand,
    )
    klass = subparser_class[subparser_name]
    kwargs = vars(parsed_args)
    kwargs.pop("subparser_name")
    command = klass(**kwargs)
    command.run()


if __name__ == "__main__":
    main()
