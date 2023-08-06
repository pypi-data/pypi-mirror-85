import unittest

import sqlparse

from sqldiff.comp.syntax_analysis import is_select_statement


class TestSyntax(unittest.TestCase):

    def test1(self):
        q = "select * from a;" \
            "select * from b;"
        parsed = sqlparse.parse(q)
        a = 1

    def test_is_select_statement(self):
        q = "select * from a"
        a = is_select_statement(q)
        b = 1