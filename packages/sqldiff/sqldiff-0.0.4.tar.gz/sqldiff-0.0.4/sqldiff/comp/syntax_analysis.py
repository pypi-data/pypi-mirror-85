"""
This modules uses https://github.com/andialbrecht/sqlparse for parsing and analyzing sql statements.

"""

import re
from functools import wraps

import sqlparse as sqlparse


def is_schema_dot_table_string(db_object_string: str):
    pattern = re.compile('^(\w+\.\w+|\w+)$')
    return bool(pattern.match(db_object_string))


def schema_table_name_to_query(tab_name):
    if is_schema_dot_table_string(tab_name):
        return f'select * from {tab_name};'
    raise ValueError("Provided value must be in format 'schema.table'")


# Any function using this decorator assumes that it'll get a sql string or parsed query as parameter
# If many_Statements_allowed == False, then function expects parsed statement instead of a tuple of parsed statements
def parse_sql(many_statements_allowed=False):
    """
    Parse sql statement using sqlparser if str is provided as function parameter.
    :param many_statements_allowed: Default False.
    If False - raises exception when parsed query has more than one statement.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(sql):
            if isinstance(sql, str):
                parsed = sqlparse.parse(sql)
            else:
                parsed = sql
            if len(parsed) > 1 and not many_statements_allowed:
                raise ValueError('Sql string or parsed query is not allowed to have more than one sql statement.')
            elif len(parsed) > 1 and many_statements_allowed:
                return func(parsed)
            elif len(parsed) == 1 and not many_statements_allowed:
                return func(parsed[0])
            else:
                return func(parsed)
        return wrapper
    return decorator

# Todo fix parser (dont work when parsed is empty string)
@parse_sql()
def is_select_statement(parsed):
    return parsed.get_type() == 'SELECT'


