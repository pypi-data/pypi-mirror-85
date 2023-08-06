# -*- coding: utf-8 -*-

import os
import subprocess
import unittest

from .helper import BaseHelper, invalid_dbname
from migratron.command.initialize import CREATE_TABLE_SQL
from migratron.command.run_migration import RunMigrationCommand, ALL_MIGRATION_TYPES


class BaseRunMigration(BaseHelper):
    """ Abstract class used to test the migrate command with different dbs
    """

    @classmethod
    def setUpClass(cls):
        if cls is BaseRunMigration:
            raise unittest.SkipTest("Abstract class")
        super(BaseRunMigration, cls).setUpClass()

    def setUp(self):
        super(BaseRunMigration, self).setUp()
        self.command = self.create_command()

        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLE_SQL)

    def create_command(self):
        pass

    def _test_no_migrations(self):
        self.command.run()
        self.assertEqual(self._get_executed_migrations(), [])

    def test_run_new_migrations(self):
        self._create_migration_files()
        self.command.run()
        self.assertEqual(self._get_executed_migrations(), self.valid_filenames)
        for table_name in ["t0", "t1"]:
            self.assertTrue(self._check_table_exist(table_name))

    def test_run_missing_migrations(self):
        self._create_migration_files()
        self._insert_migration_data(self.valid_filenames[0])
        self.command.run()
        self.assertEqual(self._get_executed_migrations(), self.valid_filenames)
        self.assertTrue(self._check_table_exist("t1"))
        self.assertFalse(self._check_table_exist("t0"))

    def test_run_failed_migration(self):
        self._create_migration_files()
        file_path = os.path.join(self.migrations_path, self.valid_filenames[0])
        with open(file_path, "w") as f:
            f.write("SELECT * FROM foobar2; \n")

        with self.assertRaises(Exception):
            self.command.run()

        executed_filenames = self._get_executed_migrations()
        self.assertEqual(executed_filenames, [self.valid_filenames[0]])

        with self.assertRaises(Exception) as cm:
            self.command.run()
        self.assertNotIsInstance(cm.exception, TypeError)
        self.assertIn("cleanup", str(cm.exception))

    def test_filter_migration_type(self):
        self._create_migration_files()
        self.command.migration_type = "pre"
        self.command.run()
        self.assertEqual(self._get_executed_migrations(), [self.valid_filenames[0]])
        self.assertFalse(self._check_table_exist("t1"))
        self.assertTrue(self._check_table_exist("t0"))


class PostgresRunMigrationTest(BaseRunMigration):

    def create_command(self):
        command = RunMigrationCommand(
            migration_type=ALL_MIGRATION_TYPES,
            just_list_files=False,
            additional_options=None,
            db_type="postgresql",
            db_uri=None,
            **self.BASE_ARGS
        )
        command.db_uri = command.state_db_uri
        return command

    def _check_table_exist(self, table_name):
        return super(PostgresRunMigrationTest, self)._check_table_exist(table_name)


@unittest.skipIf(
    invalid_dbname("MIGRATIONS_HIVE_TESTS"),
    "Skip because not using hive test database"
)
class HiveRunMigrationTest(BaseRunMigration):

    def create_command(self):
        command = RunMigrationCommand(
            migration_type=ALL_MIGRATION_TYPES,
            just_list_files=False,
            additional_options=None,
            db_type="hive",
            db_uri=os.getenv("MIGRATIONS_HIVE_TESTS"),
            **self.BASE_ARGS
        )
        return command

    def _check_table_exist(self, table_name):
        command = [
            "beeline",
            "-u",
            self.command.database_uri,
            "-e",
            "SHOW TABLES LIKE '%s'" % table_name
        ]
        output = subprocess.check_output(command)
        return table_name in output.decode('utf-8')

    def _drop_tables(self):
        for table_name in ['t0', 't1']:
            command = [
                "beeline",
                "-u",
                self.command.database_uri,
                "-e",
                "DROP TABLE IF EXISTS %s" % table_name
            ]
            subprocess.check_call(command)
