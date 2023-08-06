# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import hashlib
import psycopg2
import logging
import re

from six import moves
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import Terminal256Formatter

from migratron.consts import MIGRATIONS_TABLENAME, VALID_INPUT_VALUES


#: query used to get all the data of the already executed filenames
GET_EXISTING_MIGRATION_INFORMATION = """
SELECT
    filename,
    hashed_content,
    finished_execution_at
FROM {table}
ORDER BY filename
""".format(
    table=MIGRATIONS_TABLENAME
)

#: used to check if the migration table exists or not
CHECK_TABLE_EXISTS = """
SELECT 1
FROM information_schema.tables
WHERE
    table_name = %(table_name)s
"""

#: used to mark that there is a migration running
INSERT_MIGRATION_DATA = """
INSERT INTO {table} (
    executed_by, filename, hashed_content, started_execution_at, finished_execution_at, comment
)
VALUES
    (%(executed_by)s, %(filename)s, %(hashed_content)s, %(started_at)s, NULL, %(comment)s);
""".format(
    table=MIGRATIONS_TABLENAME
)


#: used to mark on the files as finished running successfully
UPDATE_MIGRATION_DATA = """
UPDATE {table}
SET
    finished_execution_at = %(finished_at)s
WHERE
    filename = %(filename)s;
""".format(
    table=MIGRATIONS_TABLENAME
)


#: the regex used to be sure that the filename is valid
FILENAME_VALIDATION_REGEX = re.compile("\d{8}_\d+_(pre|post)_.+")


class BaseCommand(object):
    """
    Base command from where all the other commands must extend

    :type folder_path: str
    :param folder_path: the absolute path where the rollback or
        execution files are

    :param extension str:
    :param str extension: the extension of the files to be considered
        migration files. This is used to take into account if there is
        a documentation file (README.rst, etc...)

    .. seealso: :func:`migratron.parsers.add_common_arguments` to get more
        information about the other parameters
    """

    def __init__(
        self,
        state_db_uri,
        use_colors,
        dry_run,
        batch_mode,
        color_style,
        logging_level,
        migrations_path,
        files_extension="sql",
    ):

        self.state_db_uri = state_db_uri
        self.use_colors = use_colors
        self.dry_run = dry_run
        self.batch_mode = batch_mode
        self.migrations_path = migrations_path
        self.files_extension = files_extension

        self.connection = self._create_connection()
        self.sql_lexer = SqlLexer()
        self.terminal_formatter = Terminal256Formatter(style=color_style)
        self._configure_logging(logging_level)

    def _create_connection(self):
        return psycopg2.connect(self.state_db_uri)

    def _configure_logging(self, logging_level):
        logging.basicConfig(level=getattr(logging, logging_level))

    def run(self):
        """
        This is the abstract method that should be implemented
        to add the logic of the command
        """
        raise NotImplementedError

    def validate_migration_table_exists(self):
        """
        Make sure that the migrations table exists before running
        the command. This should be used to make sure that the
        :class:`migratron.command.initialize.InitializeCommand` was executed
        """
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    CHECK_TABLE_EXISTS, dict(table_name=MIGRATIONS_TABLENAME)
                )
                exists = cursor.fetchall()
                if not exists:
                    raise Exception(
                        "The migration table does not exist "
                        "on the database so you must run the initialize "
                        "command"
                    )

    def get_executed_migrations(self, return_success=True):
        """
        Identify the list of executed migrations.

        :type return_success: bool
        :param return_success: if True, then it will return all the
            migrations that were successfully executed. If False, it
            will return all the migrations that don't have an finished_at
            value

        :rtype: list(tuple(str, str))
        :return: a dict of all the filenames (without any path),
            and the SHA1 of the file content

        :raise Exception: if asked for the successfull migrations but
            there was one that is still running or that it failed
        """
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(GET_EXISTING_MIGRATION_INFORMATION)
                rows = cursor.fetchall()
                failed_or_running = {row[0]: row[1] for row in rows if row[2] is None}
                if failed_or_running and return_success:
                    raise Exception(
                        "The following migration is already being "
                        'executed or failed: "%s", so you can not run the migration '
                        "system. If the migration failed then you must run the "
                        '"cleanup" subcommand' % next(iter(failed_or_running.keys()))
                    )

                if return_success:
                    return {row[0]: row[1] for row in rows}
                else:
                    return failed_or_running

    def get_filesystem_migrations(self):
        """
        Returns all the files on the filesystem that should be used as the
        migrations to be executed on the database

        :rtype: list(str)
        :return: a list with the names of the files to execute (without the path)
        """
        if not os.path.isdir(self.migrations_path):
            raise Exception(
                "The identified path '%s' where the migrations files "
                "should be doesn't exists" % self.migrations_path
            )

        extension = ".%s" % self.files_extension
        filenames = [
            name
            for name in os.listdir(self.migrations_path)
            if name.endswith(extension)
        ]
        # make sure that all the filenames are valid
        invalid_filenames = list(
            filter(
                lambda filename: FILENAME_VALIDATION_REGEX.match(filename) is None,
                filenames,
            )
        )
        if invalid_filenames:
            raise Exception(
                "The filename '%s' doesn't use the required "
                "filename format YYYYMMDD_index_pre/post_description."
                % invalid_filenames[0]
            )

        res = [os.path.join(self.migrations_path, name) for name in filenames]

        res.sort()
        return res

    def calculate_sha1(self, complete_filename):
        """
        Calculates the hash of the file that is going to be inserted
        on the table to mark the file as alreay executed

        :type complete_filename: str
        :param complete_filename: the path and name of the file to which
            calculate the has
        """
        with open(complete_filename, "rb") as migration_file:
            return hashlib.sha1(migration_file.read()).hexdigest()

    def print_sql(self, query):
        """
        Prints the SQL when using interactive or dry_run
        """
        if self.use_colors:
            print(highlight(query, self.sql_lexer, self.terminal_formatter))
        else:
            print(query)

    def execute_sql(self, cursor, query, **data):
        """
        Execute the query using the specified values

        :param cursor: the cursor used to execute the query
            against the database

        :type query: str
        :param query: the query information that should be used

        :type data: dict
        :param data: the data used to execute the query

        :returns: what ever the query returns
        """
        if self.dry_run:
            final_sql = query % data
            self.print_sql(final_sql)
        else:
            cursor.execute(query, data)

    def check_answer(self, question, valid_input_values):
        """
        Ask the question to the user and make sure that the response
        is valid. If not, it will ask it again

        :type question: str
        :param question: the YES/NO question to ask to the user, but without
            the the y/N

        :type valid_input_values: list(str)
        :param valid_input_values: the choices the user can select

        :rtype: str
        :return: the option that the user selected
        """
        question += " [" + "/".join(valid_input_values) + "] "
        current_input = moves.input(question)
        current_input = current_input.lower()
        while current_input not in valid_input_values:
            print("Invalid value. Choose %s" % "/".join(valid_input_values))
            current_input = moves.input(question)
            current_input = current_input.lower()

        return current_input

    def check_input(self, question):
        """
        Ask the question to the user and make sure that the response
        is valid. If not, it will ask it again

        :type question: str
        :param question: the YES/NO question to ask to the user, but without
            the the y/N

        :rtype: bool
        :return: True if the user anser YES, False if he answer NO
        """
        user_selection = self.check_answer(question, VALID_INPUT_VALUES)
        return user_selection == "yes"
