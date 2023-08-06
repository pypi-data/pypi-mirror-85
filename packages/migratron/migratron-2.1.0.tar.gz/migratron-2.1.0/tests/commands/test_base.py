# -*- coding: utf-8 -*-

import os
import sys

from .helper import BaseHelper
from migratron.command.base import BaseCommand

from contextlib import contextmanager

try:
    from StringIO import StringIO
except ImportError:
    # do not use io for Python2 because there is some error
    # on str/unicode
    from io import StringIO


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class BaseCommandTest(BaseHelper):
    def setUp(self):
        super(BaseCommandTest, self).setUp()
        self.command = BaseCommand(**self.BASE_ARGS)

    def test_not_initializated(self):
        with self.assertRaises(Exception) as cm:
            self.command.validate_migration_table_exists()

        self.assertEqual(
            getattr(cm.exception, "message", cm.exception.args[0]),
            "The migration table does not exist on the database so you must run the initialize command",
        )

    def test_empty_migrations(self):
        filenames = self.command.get_filesystem_migrations()
        self.assertEqual(filenames, [])

    def test_remove_files_by_extensions(self):
        for filename in ["20160101_0_pre_a.sql", "20160202_0_post_b.sql", "README.md"]:
            open(os.path.join(self.migrations_path, filename), "w").write("SELECT 1;")

        filenames = self.command.get_filesystem_migrations()
        self.assertEqual(
            filenames,
            [
                os.path.join(self.migrations_path, filename)
                for filename in ["20160101_0_pre_a.sql", "20160202_0_post_b.sql"]
            ],
        )

    def test_invalid_filename(self):
        for filename in ["README.sql", "20160101.sql", "asd.sql"]:
            open(os.path.join(self.migrations_path, filename), "w").write("SELECT 1;")
            with self.assertRaises(Exception) as cm:
                self.command.get_filesystem_migrations()

            self.assertEqual(
                getattr(cm.exception, "message", cm.exception.args[0]),
                "The filename '%s' doesn't use the required filename format YYYYMMDD_index_pre/post_description."
                % filename,
            )

            os.remove(os.path.join(self.migrations_path, filename))

    def test_check_dry_run(self):
        with captured_output() as (out, err):
            cursor = self.command.connection.cursor()
            self.command.dry_run = True
            self.command.execute_sql(cursor, "DROP TABLE foobar")

            output = out.getvalue().strip()
            self.assertEqual(output, "DROP TABLE foobar")
