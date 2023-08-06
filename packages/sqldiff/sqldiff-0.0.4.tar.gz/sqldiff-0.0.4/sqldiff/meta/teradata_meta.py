import json
from typing import List

from sqldiff.meta.dbsystem import TERADATA
from sqldiff.meta.column_description import ColumnDescription
from sqldiff.meta.meta_connection_dispatcher import dbmeta


def get_raw_meta(connection, query):
    # based on: https://github.com/Teradata/python-driver/blob/master/samples/MetadataFromPrepare.py
    with connection.cursor() as cursor:
        metadata_query = '{fn teradata_rpo(S)}{fn teradata_fake_result_sets}' + query
        cursor.execute(metadata_query)
        row = cursor.fetchone()
        return json.loads(row[7])


@dbmeta('teradatasql')
def get_meta(connection, query):
    raw_meta = get_raw_meta(connection, query)
    metadata: List[ColumnDescription] = []
    for column in raw_meta:
        type_name = column['TypeName'].upper()

        if 'CHAR' in type_name:
            precision = column['MaxCharacterCount']
            scale = None
        elif 'DECIMAL' == type_name:
            precision = column['Precision']
            scale = column['Scale']
        elif any(i in type_name for i in ('TIME', 'INTERVAL')):
            precision = None
            scale = column['Scale']
        else:
            precision = scale = None

        column_description = {
            'name': column['Title'].lower(),
            'type_code': column['RawDataType'],
            'display_size': None,
            'internal_size': column['ByteCount'],
            'precision': precision,
            'scale': scale,
            'null_ok': column['MayBeNull'],
            'type_name': type_name,
            'position': column['Position'],
            'dbsystem': TERADATA
        }
        metadata.append(ColumnDescription(**column_description))
    return metadata

