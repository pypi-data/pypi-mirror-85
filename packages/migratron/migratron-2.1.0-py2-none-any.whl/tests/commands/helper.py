# -*- coding: utf-8 -*-

import os
import shutil
import unittest
from datetime import datetime

from migratron.consts import MIGRATIONS_TABLENAME
from migratron.command.base import (
    INSERT_MIGRATION_DATA,
    UPDATE_MIGRATION_DATA,
    CHECK_TABLE_EXISTS,
)

#: the path where the migrations files are going to be created
BASE_PATH = "/tmp/testing-dbutils"

#: the URI used to be used to run the tests
DB_URI = os.getenv("MIGRATIONS_DB_TESTS")


def invalid_dbname(environ_key):
    environ_value = os.getenv(environ_key)
    if not environ_value:
        return True

    db_name = environ_value.split("/")[-1]
    if "test" in db_name:
        return False

    return True


@unittest.skipIf(invalid_dbname("MIGRATIONS_DB_TESTS"), "Skip because not using test database")
class BaseHelper(unittest.TestCase):
    """
    Base helper that is going to have some common functions for all
    the integration tests that connect to Postgres

    The result of the connection if the object connection mock returned
    before
    """

    BASE_ARGS = dict(
        migrations_path=BASE_PATH,
        state_db_uri=DB_URI,
        use_colors=False,
        dry_run=False,
        batch_mode=True,
        color_style="vim",
        logging_level="DEBUG",
    )

    def setUp(self):
        self.command = None
        self.migrations_path = BASE_PATH
        self.valid_filenames = ["20160101_0_pre_asd.sql", "20160202_0_post_asd.sql"]
        self.addCleanup(self._remove_path)
        os.makedirs(self.migrations_path)

    def tearDown(self):
        if self.command is None:
            return
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS %s" % MIGRATIONS_TABLENAME)

        self._drop_tables()

    def _drop_tables(self):
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS t0")
                cursor.execute("DROP TABLE IF EXISTS t1")

    def _remove_path(self):
        shutil.rmtree(BASE_PATH)

    def _create_migration_files(self):
        for index, filename in enumerate(self.valid_filenames):
            file_path = os.path.join(self.migrations_path, filename)
            with open(file_path, "w") as f:
                f.write("CREATE TABLE t%s (id INTEGER);\n" % index)

    def _check_table_exist(self, table_name):
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(CHECK_TABLE_EXISTS, dict(table_name=table_name))
                return cursor.fetchall()

    def _get_executed_migrations(self):
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT filename FROM %s ORDER BY filename" % MIGRATIONS_TABLENAME
                )
                res = [row[0] for row in cursor]
                return res

    def _insert_migration_data(self, filename, run_ok=True):
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    INSERT_MIGRATION_DATA,
                    dict(
                        filename=filename,
                        executed_by="test",
                        hashed_content=self.command.calculate_sha1(
                            os.path.join(self.migrations_path, filename)
                        ),
                        started_at=datetime.now(),
                        finished_at=None,
                        comment=None,
                    ),
                )
                if run_ok:
                    cursor.execute(
                        UPDATE_MIGRATION_DATA,
                        dict(filename=filename, finished_at=datetime.now()),
                    )
