# TODO DEFINE RELATIONS
from copy import deepcopy

from sqldiff.meta import dbsystem
from sqldiff.comp.compare import ColumnDescription
from sqldiff.relation.relation_manager import dbmapping


@dbmapping('DECIMAL', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'NUMERIC'
    return tgt_col


@dbmapping('TIMESTAMP WITH TIME ZONE', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'TIMESTAMPTZ'
    tgt_col.precision = None
    tgt_col.scale = None
    return tgt_col


@dbmapping('TIME WITH TIME ZONE', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'TIMESTZ'
    tgt_col.precision = None
    tgt_col.scale = None
    return tgt_col


@dbmapping('CHAR', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    return tgt_col


@dbmapping('CHAR', dbsystem.TERADATA, (dbsystem.POSTGRES,))
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'BPCHAR'
    return tgt_col


@dbmapping('LONG VARCHAR', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    tgt_col.precision = 64000
    return tgt_col


@dbmapping('LONG VARCHAR', dbsystem.TERADATA, (dbsystem.POSTGRES,))
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    tgt_col.precision = -1
    return tgt_col


@dbmapping('VARCHAR', dbsystem.TERADATA, (dbsystem.POSTGRES,))
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    tgt_col.precision = -1
    return tgt_col


@dbmapping('CHAR', dbsystem.TERADATA, (dbsystem.POSTGRES,))
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    tgt_col.precision = -1
    return tgt_col


