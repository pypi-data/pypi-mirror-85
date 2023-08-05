#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import io
import sys
import things3.things3_cli as things3_cli


class Things3CLICase(unittest.TestCase):
    """Class documentation goes here."""

    things3_cli = things3_cli.Things3CLI(database='resources/demo.sqlite3')

    def test_methods(self):
        """Invoke all commands."""
        parser = self.things3_cli.get_parser()
        for command in parser._subparsers._actions[1].choices:  # noqa # pylint: disable=protected-access
            if command != "feedback":
                args = parser.parse_args([command])
                new_out = io.StringIO()
                old_out = sys.stdout
                try:
                    sys.stdout = new_out
                    self.things3_cli.main(args)
                finally:
                    sys.stdout = old_out
                self.assertIn(" ", new_out.getvalue())

    def test_today(self):
        """Test Today."""
        args = self.things3_cli.get_parser().parse_args(['today'])
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            self.things3_cli.main(args)
        finally:
            sys.stdout = old_out
        self.assertIn("Today MIT", new_out.getvalue())

    def test_csv(self):
        """Test Next via CSV."""
        args = self.things3_cli.get_parser().parse_args(['-c', 'next'])
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            self.things3_cli.main(args)
        finally:
            sys.stdout = old_out
        self.assertIn("FBBB5D059751", new_out.getvalue())

    def test_json(self):
        """Test Upcoming via JSON."""
        args = self.things3_cli.get_parser().parse_args(['-j', 'upcoming'])
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            self.things3_cli.main(args)
        finally:
            sys.stdout = old_out
        self.assertIn("4F7006C4ADF7", new_out.getvalue())


if __name__ == '__main__':
    unittest.main()
