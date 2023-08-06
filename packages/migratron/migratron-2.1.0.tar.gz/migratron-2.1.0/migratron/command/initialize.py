# -*- coding: utf-8 -*-

import os
import getpass
from datetime import datetime

from migratron.consts import MIGRATIONS_TABLENAME
from migratron.command.base import (
    BaseCommand,
    INSERT_MIGRATION_DATA,
    UPDATE_MIGRATION_DATA,
)

#: The SQL instruction that is going to be used to create the table
#: with the information to be able to create the db_migrations table
CREATE_TABLE_SQL = """
CREATE TABLE {table} (
    filename VARCHAR(1024) NOT NULL PRIMARY KEY,
    executed_by VARCHAR(1024) NOT NULL,
    hashed_content VARCHAR(40) NOT NULL,
    started_execution_at TIMESTAMP NOT NULL,
    finished_execution_at TIMESTAMP,
    comment TEXT
);

COMMENT ON TABLE {table} IS 'Has the information about the different migrations';

COMMENT ON COLUMN {table}.executed_by IS 'The user that run the migrations.';

COMMENT ON COLUMN {table}.filename IS '
The filename (and its extension) of the migrated table. This won''t
have the path, just the filename to take into account that the path might
change taking into account who executed the command

Since the file can only be executed once, it is the primary key
of the table. When doing a rollback of an already executed migration,
it will delete the row in this table
';

COMMENT ON COLUMN {table}.hashed_content IS '
The hashed content of the file to identify if it was updated or not.

Again, on production environment the file should only be executed once,
but during development the file could be executed more than once because
it has changed so this is used to identify those cases.

Also, this is going to be used to identify the files that changed their
name (added a new prefix, etc...)
';

COMMENT ON COLUMN {table}.started_execution_at IS 'The time when the migration started running';

COMMENT ON COLUMN {table}.finished_execution_at IS '
The time when the migration finished. It will be None, until
the migration finishes running successfully. ';

COMMENT ON COLUMN {table}.comment IS '
Any additional comment the user wanted to add when the migration was executed
for future reference
';

""".format(
    table=MIGRATIONS_TABLENAME
)


class InitializeCommand(BaseCommand):
    """
    Used to initialize the database and mark all the existing migrations
    as already executed. This must only be executed once
    """

    def __init__(self, just_base_schema, **kwargs):
        super(InitializeCommand, self).__init__(**kwargs)
        self.just_base_schema = just_base_schema

    def run(self):
        try:
            self.validate_migration_table_exists()
            raise Exception(
                "The migration table already exists so no initialization is required"
            )
        except Exception as e:
            message = getattr(e, "message", e.args[0])
            if "The migration table does not exist" not in message:
                raise

        existing_filenames = self.get_filesystem_migrations()
        self.initialize(existing_filenames)

    def initialize(self, existing_filenames):
        """
        Creates the migration table, and it will mark all the files
        as already executed.

        :type existinf_filenames: list(str)
        :param existing_filenames: all the list of the existing migrations
            that have already been executed
        """
        username = getpass.getuser()
        # Make sure that all the opreations are executed on the
        # same transaction because the initialization data will
        # be used
        with self.connection:
            with self.connection.cursor() as cursor:
                self.execute_sql(cursor, CREATE_TABLE_SQL)
                if self.just_base_schema:
                    return

                for complete_filename in existing_filenames:
                    filename = os.path.basename(complete_filename)
                    sha1 = self.calculate_sha1(complete_filename)

                    started_at = datetime.now()
                    filename = os.path.basename(complete_filename)
                    self.execute_sql(
                        cursor,
                        INSERT_MIGRATION_DATA,
                        filename=filename,
                        executed_by=username,
                        hashed_content=sha1,
                        started_at=started_at,
                        comment="System initialization",
                    )
                    self.execute_sql(
                        cursor,
                        UPDATE_MIGRATION_DATA,
                        finished_at=started_at,
                        filename=filename,
                    )
