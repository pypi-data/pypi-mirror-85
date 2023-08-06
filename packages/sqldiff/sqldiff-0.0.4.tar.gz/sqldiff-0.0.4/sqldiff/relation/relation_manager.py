from copy import deepcopy

import sqldiff.meta.dbsystem as dbsystem
from sqldiff.meta import ColumnDescription


from sqldiff.utils import make_tuple

ANY_DB = (dbsystem.POSTGRES, dbsystem.TERADATA)

# Dictionary which holds relation functions registered by dbmapping decorator
mappings = {}


def dbmapping(type_name, source_dbsystem, target_dbsystem=ANY_DB):
    """
    Decorator adds defined function to registry of dbsystems types mappings.
    :param type_name:
    :param source_dbsystem:
    :param target_dbsystem:
    :return:
    """

    def decorator(func):
        # make systems iterable - in case that single string, or other sequence type has been passed as an argument
        source_dbsystems = make_tuple(source_dbsystem)
        target_dbsystems = make_tuple(target_dbsystem)

        for src_db in source_dbsystems:
            for tgt_db in target_dbsystems:
                key = (type_name, src_db, tgt_db)
                mapping = mappings.setdefault(key, [])
                if func not in mapping:
                    mapping.append(func)
        return func
    return decorator


def relation_identity(src_col: ColumnDescription):
    res_col = deepcopy(src_col)
    return res_col


def get_relations_using_keys(type_name, source_dbsystem, target_dbsystem):
    if not all([isinstance(i, str) for i in (type_name, source_dbsystem, target_dbsystem)]):
        raise ValueError('Relation keys needs to be strings')
    return mappings.get((type_name, source_dbsystem, target_dbsystem), []) + [relation_identity]


def get_relations_using_columns(src_col: ColumnDescription, tgt_col: ColumnDescription):
    if not all([isinstance(i, ColumnDescription) for i in (src_col, tgt_col)]):
        raise ValueError('Parameters needs to be ColumnDescription type')
    return get_relations_using_keys(src_col.type_name, src_col.dbsystem, tgt_col.dbsystem)


def get_relations(**kwargs):
    """
    Returns all registered relations either for:
    str kwargs: ('type_name', 'source_dbsystem', 'target_dbsystem')
    or ColumnDescription kwargs: ('src_col', 'tgt_col')
    :param kwargs:
    :return:
    """
    if all(i in kwargs for i in ('src_col', 'tgt_col')):
        return get_relations_using_columns(**kwargs)
    if all(i in kwargs for i in ('type_name', 'source_dbsystem', 'target_dbsystem')):
        return get_relations_using_keys(**kwargs)
    raise KeyError('Invalid parameters')


# czy dany (typ, dbsystem) mapuje sie na (typ, dbsystem) ????