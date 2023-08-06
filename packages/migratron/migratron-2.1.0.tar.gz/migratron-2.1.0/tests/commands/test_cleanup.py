# -*- coding: utf-8 -*-

import os

from .helper import BaseHelper
from migratron.command.cleanup import CleanupCommand
from migratron.command.initialize import CREATE_TABLE_SQL


class CleanupCommandTest(BaseHelper):
    def setUp(self):
        super(CleanupCommandTest, self).setUp()
        self.command = CleanupCommand(**self.BASE_ARGS)
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLE_SQL)

    def test_no_failed_migration(self):
        # if there is no migration to cleanup then it will run correctly
        self.command.run()

    def test_rollback_failed(self):
        self._create_migration_files()
        self._insert_migration_data(self.valid_filenames[0], run_ok=True)
        self._insert_migration_data(self.valid_filenames[1], run_ok=False)

        self.command.run()

        executed = self._get_executed_migrations()
        self.assertEqual(executed, [self.valid_filenames[0]])

    def test_correct_invalid_hash(self):
        self._create_migration_files()
        self._insert_migration_data(self.valid_filenames[0])
        self._insert_migration_data(self.valid_filenames[1])

        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE db_migrations SET hashed_content = %s WHERE filename = %s",
                    ("123123123", self.valid_filenames[1]),
                )

        self.command.run()
        data = self.command.get_executed_migrations()
        expected_data = {
            filename: self.command.calculate_sha1(
                os.path.join(self.migrations_path, filename)
            )
            for filename in self.valid_filenames
        }
        self.assertEqual(data, expected_data)
