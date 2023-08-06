# -*- coding: utf-8 -*-


from .helper import BaseHelper
from migratron.consts import MIGRATIONS_TABLENAME
from migratron.command.base import CHECK_TABLE_EXISTS
from migratron.command.initialize import InitializeCommand


class InitializeCommandTest(BaseHelper):
    def setUp(self):
        super(InitializeCommandTest, self).setUp()
        self.command = InitializeCommand(just_base_schema=False, **self.BASE_ARGS)

    def tearDown(self):
        super(InitializeCommandTest, self).tearDown()
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS %s" % MIGRATIONS_TABLENAME)
                cursor.execute("DROP TABLE IF EXISTS t0")
                cursor.execute("DROP TABLE IF EXISTS t1")

    def test_initialize_no_files(self):
        self.command.run()
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM %s" % MIGRATIONS_TABLENAME)
                data = cursor.fetchall()
                self.assertEqual(data, [])

    def test_initialize_some_files(self):
        self._create_migration_files()

        self.command.run()
        with self.command.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT filename FROM %s ORDER BY filename" % MIGRATIONS_TABLENAME
                )
                data = cursor.fetchall()
                self.assertEqual([x[0] for x in data], self.valid_filenames)
                # the tables shouldn't exist because we are doing a database
                # initialization
                for table_name in ["t1", "t2"]:
                    cursor.execute(CHECK_TABLE_EXISTS, dict(table_name=table_name))
                    existing = cursor.fetchall()
                    self.assertEqual(existing, [])
