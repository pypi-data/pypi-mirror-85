# -*- coding: utf-8 -*-

from __future__ import print_function

from logging import getLogger
import os

from migratron.consts import MIGRATIONS_TABLENAME
from migratron.command.base import BaseCommand

#: query used to get all the data of the already executed filenames
DELETE_FAILED_MIGRATION = """
DELETE FROM {table} WHERE filename = %(filename)s
""".format(
    table=MIGRATIONS_TABLENAME
)

#: query used to update the invalid hash of the file when it
#: was executed manually and the file was edited later on
UPDATE_HASH = """
UPDATE {table} SET hashed_content = %(hashed_content)s WHERE filename = %(filename)s
""".format(
    table=MIGRATIONS_TABLENAME
)


logger = getLogger(__name__)


class CleanupCommand(BaseCommand):
    """
    Used to delete any failed migration and/or update the hash
    of any executed migration
    """

    def run(self):
        self._remove_failed()
        self._update_hash()

    def _remove_failed(self):
        self.validate_migration_table_exists()
        failed_to_run = self.get_executed_migrations(return_success=False)
        if not failed_to_run:
            logger.warning("There was no failed migration to cleanup")
            return

        for filename in failed_to_run.keys():
            logger.debug("Found the following filename to cleanup: %s", filename)

            if not self.batch_mode and not self.dry_run:
                should_continue = self.check_input(
                    "Should it delete the row for the migration: %s?" % filename
                )
                if not should_continue:
                    print("You chose not to delete the migration")
                    return

            with self.connection:
                with self.connection.cursor() as cursor:
                    self.execute_sql(cursor, DELETE_FAILED_MIGRATION, filename=filename)
        logger.info("Finish cleanup of failed migrations")

    def _update_hash(self):
        """
        Updates the hash of any executed migration with the one of
        the filesystem

        This SHOULD NOT happen but it is intended for very special cases,
        where the migration was executed manually and marked as
        executed, and then the migration file was changed.
        """
        executed_migrations = dict(self.get_executed_migrations())
        filesystem_migrations = self.get_filesystem_migrations()
        for complete_filename in filesystem_migrations:
            filename = os.path.basename(complete_filename)
            database_hash = executed_migrations.get(filename)
            filesystem_hash = self.calculate_sha1(complete_filename)

            if database_hash is None:
                # this migration wasn't executed
                logger.debug("Found the filename %s that was not executed", filename)
                continue

            if filesystem_hash == database_hash:
                # the migration was executed and the file wasn't updated
                logger.debug("Found the filename %s ok", filename)
                continue

            logger.warning("Found the filename: %s with different hash", filename)
            if not (self.batch_mode or self.dry_run):
                should_cleanup = self.check_input(
                    "Found the filename %s with invalid hash. Cleanup?" % filename
                )
                if not should_cleanup:
                    print("Skip the hash update for file: %s" % filename)
                    continue

            with self.connection:
                with self.connection.cursor() as cursor:
                    self.execute_sql(
                        cursor,
                        UPDATE_HASH,
                        filename=filename,
                        hashed_content=filesystem_hash,
                    )
