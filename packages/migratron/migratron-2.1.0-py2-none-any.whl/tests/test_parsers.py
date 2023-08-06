# -*- coding: utf-8 -*-

import os
import unittest

from migratron.parsers import create_command_line_parser


class ParsersTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop("DB_UTILS_MIGRATIONS_PATH", None)

    def _check_migrations_parser(self, additional_args=None):
        parser = create_command_line_parser()
        args = ["migrate", "--migration-type", "any"]
        if additional_args:
            args.extend(additional_args)
        parsed_data = parser.parse_args(args)
        return parsed_data

    def test_parse_path_from_environ(self):
        os.environ["DB_UTILS_MIGRATIONS_PATH"] = "/tmp"
        parsed_data = self._check_migrations_parser()
        self.assertEqual(parsed_data.migrations_path, "/tmp")

    def test_parse_path_from_args(self):
        parsed_data = self._check_migrations_parser(["--migrations-path", "/tmp2"])
        self.assertEqual(parsed_data.migrations_path, "/tmp2")

    def test_args_has_priority(self):
        os.environ["DB_UTILS_MIGRATIONS_PATH"] = "/tmp"
        parsed_data = self._check_migrations_parser(["--migrations-path", "/tmp2"])
        self.assertEqual(parsed_data.migrations_path, "/tmp2")
