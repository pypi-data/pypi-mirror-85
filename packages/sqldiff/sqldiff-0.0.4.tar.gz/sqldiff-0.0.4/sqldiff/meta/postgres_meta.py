from typing import List

from sqldiff.meta.dbsystem import POSTGRES
from sqldiff.meta.column_description import ColumnDescription
from sqldiff.meta.meta_connection_dispatcher import dbmeta

LIMIT_0 = ' limit 0'
NUMERIC_MAX_PRECISION = 65535
NUMERIC_MAX_SCALE = 65535

ALIASES = (
    ('SMALLINT', 'INT2'),
    ('INTEGER', 'INT4', 'INT'),
    ('BIGINT', 'INT8'),
    ('NUMERIC', 'DECIMAL'),
    ('REAL', 'FLOAT4'),
    ('DOUBLE', 'DOUBLE PRECISION', 'FLOAT8'),
    ('SMALLSERIAL', 'SERIAL2'),
    ('SERIAL', 'SERIAL4'),
    ('BIGSERIAL', 'SERIAL8'),
    ('VARCHAR', 'CHARACTER VARYING'),
    ('CHAR', 'CHARACTER', 'BPCHAR'),
    ('TIMESTAMP WITHOUT TIME ZONE', 'TIMESTAMP'),
    ('TIMESTAMP WITH TIME ZONE', 'TIMESTAMPTZ'),
    ('TIME WITHOUT TIME ZONE', 'TIME'),
    ('TIME WITH TIME ZONE', 'TIMETZ'),
    ('BOOLEAN', 'BOOL')
)


def get_type_code_name_mapping(connection):
    with connection.cursor() as cursor:
        query = """
        SELECT
        t.oid,
        t.typname
        FROM pg_catalog.pg_type t
        WHERE
        (
            t.typrelid = 0
            OR (
                SELECT c.relkind = 'c'
                FROM pg_catalog.pg_class c
                WHERE c.oid = t.typrelid
            )
        )
        AND NOT EXISTS (SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem AND el.typarray = t.oid)
        AND pg_catalog.pg_type_is_visible(t.oid)
        ORDER BY t.oid
        """
        cursor.execute(query)
        records = cursor.fetchall()
        oid_types_dict = {r[0]: r[1] for r in records}
        return oid_types_dict


@dbmeta('psycopg2')
def get_meta(connection, query, predefined_type_mapping=None):
    if predefined_type_mapping is None:
        type_mapping = get_type_code_name_mapping(connection)
    else:
        type_mapping = predefined_type_mapping

    limit_query = query + LIMIT_0 if not query.strip().endswith(LIMIT_0) else query
    with connection.cursor() as cursor:
        cursor.execute(limit_query)
        metadata: List[ColumnDescription] = []
        position_index = 1
        for column in cursor.description:
            type_name = type_mapping[column.type_code].upper()

            if 'CHAR' in type_name:
                precision = column.internal_size
                scale = None
            else:
                precision = column.precision
                scale = column.scale
            column_description = {
                'name': column.name.lower(),
                'type_code': column.type_code,
                'display_size': column.display_size,
                'internal_size': column.internal_size,
                'precision': precision,
                'scale': scale,
                'null_ok': column.null_ok,
                'type_name': type_name,
                'position': position_index,
                'dbsystem': POSTGRES
            }
            metadata.append(ColumnDescription(**column_description))
            position_index += 1
        return metadata
