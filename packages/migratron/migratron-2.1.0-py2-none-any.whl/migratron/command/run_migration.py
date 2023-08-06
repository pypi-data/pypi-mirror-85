# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import getpass
import subprocess
import shlex
from logging import getLogger
from datetime import datetime

from migratron.command.base import (
    BaseCommand,
    INSERT_MIGRATION_DATA,
    UPDATE_MIGRATION_DATA,
)


logger = getLogger(__name__)


MANUALLY_EXECUTION = "manually"
ALL_MIGRATION_TYPES = "any"


class RunMigrationCommand(BaseCommand):
    """
    Run the missing SQL files to update the schema of the
    database.

    :seealso: Check :mod:`migratron.parsers` to get additional information
        about the other parameters
    """

    def __init__(
        self, migration_type, db_type, db_uri, just_list_files, additional_options, *args, **kwargs
    ):
        super(RunMigrationCommand, self).__init__(*args, **kwargs)
        self.migration_type = migration_type
        self.additional_options = additional_options
        self.just_list_files = just_list_files
        self.db_uri = db_uri
        self.db_type = db_type

    def run(self):
        self.validate_migration_table_exists()
        if self.db_type in ("hive", "presto"):
            if not self.db_uri:
                raise Exception("You must specify the database uri")

        existing_filenames = self.get_filesystem_migrations()
        already_executed_data = self.get_executed_migrations()
        files_to_execute = []

        files_to_execute = self.find_missing_migrations(
            existing_filenames, already_executed_data
        )
        if not files_to_execute:
            logger.info("No migration is missing")
            return

        if self.just_list_files:
            for (complete_filename, sha1) in files_to_execute:
                print(complete_filename)
        else:
            self.execute_missing(files_to_execute)

    def find_missing_migrations(self, existing_filenames, already_executed_data):
        """
        Find the new files that should be executed on the database, or the
        ones that have been renamed and should be inserted on the migration table

        :type existing_filenames: list(str)
        :param existing_filenames: all the name of the files found on the
            filesystem to be executed. This includes the local path of the files

        :type already_executed_data: dict(filename, sha1)
        :param already_executed_data: the filenames and theirs hash that already
            exists on the migration's table

        :rtype: list(str)
        :return: the list of the files that are missing to be executed
        """
        files_to_execute = []

        # need to rever the already_executed_data to take into account
        # that the sha1 should be unique
        sha1_filename = {
            sha1: filename for filename, sha1 in already_executed_data.items()
        }

        for complete_filename in existing_filenames:

            filename = os.path.basename(complete_filename)
            migration_type = filename.split("_")[2]
            if (
                self.migration_type != ALL_MIGRATION_TYPES
                and migration_type != self.migration_type
            ):
                continue

            hashed_content = self.calculate_sha1(complete_filename)

            # get the hashed content on the database for that filename
            existing_hash = already_executed_data.get(filename)

            if existing_hash is not None and existing_hash == hashed_content:
                # in this case the file aready exists on the database so we can
                # continue to the next file
                logger.debug("The file '%s' was already executed", complete_filename)
                continue

            if existing_hash is not None:
                raise Exception(
                    'A file with the name "%s" already exists on the '
                    "database but it has a different hash. You forgot to run "
                    "the rollback?" % filename
                )

            if sha1_filename.get(hashed_content):
                if self.batch_mode:
                    logger.warning(
                        'A file with the same hash as "%s" already '
                        "exists on the database. Maybe you renamed the file and "
                        "forgot to run the rollback?",
                        filename,
                    )
                else:
                    should_continue = self.check_input(
                        'A file with the same hash as "%s" already '
                        "exists on the database. Continue?" % filename
                    )
                    if not should_continue:
                        raise Exception("You chose not to run the migration")

            else:
                logger.debug("Found new migration file: '%s'", complete_filename)
                files_to_execute.append((complete_filename, hashed_content))

        return files_to_execute

    def execute_missing(self, files_to_execute):
        """
        Executes the missing files on the database

        :type files_to_execute: list(tuple(str, str))
        :param files_to_execute: the path of the files and the SHA1 of the content
            of the file
        """
        username = getpass.getuser()
        for (index, (complete_filename, sha1)) in enumerate(files_to_execute):
            filename = os.path.basename(complete_filename)

            with open(complete_filename) as file:
                file_content = file.read()

            if not self.batch_mode and not self.dry_run:
                self.print_sql(file_content)

                execution_type = self.check_answer(
                    "Should it execute the migration: %s?" % filename,
                    valid_input_values=["yes", "no", MANUALLY_EXECUTION],
                )
                if execution_type == "no":
                    print("You chose not to run the migration. Exit")
                    break
            else:
                execution_type = ""

            self.connection.autocommit = True
            self.file_content_splited = False
            started_at = datetime.now()
            if execution_type != MANUALLY_EXECUTION:
                logger.info(
                    "Running file: %s (%s out of %s)",
                    filename,
                    index + 1,
                    len(files_to_execute),
                )
            else:
                logger.info("Marking the migration: %s as executed", filename)

            with self.connection:
                with self.connection.cursor() as cursor:
                    self.execute_sql(
                        cursor,
                        INSERT_MIGRATION_DATA,
                        filename=filename,
                        executed_by=username,
                        hashed_content=sha1,
                        started_at=started_at,
                        finished_at=None,
                        comment=None,
                    )
                    if execution_type != MANUALLY_EXECUTION:
                        self._execute_filename(file_content, complete_filename)
                    self.execute_sql(
                        cursor,
                        UPDATE_MIGRATION_DATA,
                        finished_at=datetime.now(),
                        filename=filename,
                    )

    def _execute_filename(self, file_content, complete_filename):
        if self.dry_run:
            self.print_sql(file_content)
            return

        command = None
        if self.db_type == "postgresql":
            command = [
                "psql",
                "--quiet",
                "--no-psqlrc",
                "-v",
                "ON_ERROR_STOP=1",
                "-f",
                complete_filename,
            ]
            if self.db_uri:
                command += [self.db_uri]
        elif self.db_type == "hive":
            command = [
                "beeline",
                "-u",
                self.db_uri,
                "-f",
                complete_filename
            ]

        elif self.db_type == "presto":
            command = [
                "presto-cli",
                "--server",
                self.db_uri,
                "-f",
                complete_filename
            ]
        else:
            raise ValueError("Invalid database type")

        if self.additional_options:
            parsed_additional_options = shlex.split(self.additional_options)
            for option, value in parsed_additional_options.items():
                if isinstance(value, bool):
                    # in this case it was just a flag (-h for example)
                    command += [option]
                else:
                    command += [option, value]

        try:
            subprocess.check_call(command)
        except Exception:
            logger.exception("Error while running the migration: %s", complete_filename)
            raise
