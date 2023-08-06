# -*- coding: utf-8 -*-

from .helper import BaseHelper, DB_URI, BASE_PATH
from migratron import consts
from migratron.main import main
from migratron.command import base


class CommandWorkflowTest(BaseHelper):
    """
    An integration test that will run the commands to make sure
    that parsers are working ok
    """

    def setUp(self):
        super(CommandWorkflowTest, self).setUp()
        self.command = base.BaseCommand(**self.BASE_ARGS)
        self._create_migration_files()

    def test_workflow(self):
        # initialize the database
        main(
            [
                "initialize",
                "--state-db-uri",
                DB_URI,
                "--just-base-schema",
                "--batch-mode",
                "--migrations-path",
                BASE_PATH,
            ]
        )

        # check that only the db_migrations table was created
        # and that the table is empty
        self.assertTrue(self._check_table_exist(consts.MIGRATIONS_TABLENAME))
        self.assertFalse(self._check_table_exist("t0"))
        self.assertFalse(self._check_table_exist("t1"))

        # run the migrations
        main(
            [
                "migrate",
                "--state-db-uri",
                DB_URI,
                "--db-uri",
                DB_URI,
                "--migration-type",
                "any",
                "--batch-mode",
                "--migrations-path",
                BASE_PATH,
            ]
        )

        self.assertTrue(self._check_table_exist("t0"))
        self.assertTrue(self._check_table_exist("t1"))
        self.assertEqual(self._get_executed_migrations(), self.valid_filenames)

    def test_cleanup(self):
        main(
            [
                "initialize",
                "--state-db-uri",
                DB_URI,
                "--batch-mode",
                "--migrations-path",
                BASE_PATH,
            ]
        )

        # change the sha1 of the first migration and make sure
        # that the second one is mark as failed
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE db_migrations SET hashed_content = %s WHERE filename = %s",
                    ("123123131231", self.valid_filenames[0]),
                )
                cursor.execute(
                    "UPDATE db_migrations SET finished_execution_at = NULL WHERE filename = %s",
                    (self.valid_filenames[1],),
                )

        with self.assertRaises(Exception):
            main(
                [
                    "migrate",
                    "--state-db-uri",
                    DB_URI,
                    "--db-uri",
                    DB_URI,
                    "--migration-type",
                    "any",
                    "--batch-mode",
                    "--migrations-path",
                    BASE_PATH,
                ]
            )

        main(
            [
                "cleanup",
                "--state-db-uri",
                DB_URI,
                "--batch-mode",
                "--migrations-path",
                BASE_PATH,
            ]
        )

        main(
            [
                "migrate",
                "--state-db-uri",
                DB_URI,
                "--db-uri",
                DB_URI,
                "--migration-type",
                "any",
                "--batch-mode",
                "--migrations-path",
                BASE_PATH,
            ]
        )
