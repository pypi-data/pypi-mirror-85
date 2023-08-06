from operator import itemgetter, attrgetter
from typing import List

from sqldiff.comp.syntax_analysis import is_schema_dot_table_string, schema_table_name_to_query, is_select_statement
from sqldiff.meta.column_description import ColumnDescription
from sqldiff.meta.meta_connection_dispatcher import get_meta_provider
from sqldiff.relation.relation_manager import get_relations


KEYS_ORDER_TARGET = 'target'
KEYS_ORDER_SOURCE = 'source'
KEYS_ORDER_ZIP = 'zip'
KEY_ORDER_OPTIONS = (KEYS_ORDER_TARGET, KEYS_ORDER_SOURCE, KEYS_ORDER_ZIP)


def get_item_or_none(iterable, i):
    try:
        return iterable[i]
    except IndexError:
        return None


def compare_keys_zip(source_keys, target_keys):
    pos_factor = 0
    src_idx = 0
    tgt_idx = 0
    key_comp_list = []
    # set of common keys
    common_keys = source_keys.keys() & target_keys.keys()

    common_keys_upper = set([k.upper() for k in source_keys.keys()]) & set([k.upper() for k in target_keys.keys()])

    while src_idx < len(source_keys) or tgt_idx < len(target_keys):

        src_key = get_item_or_none(list(source_keys.keys()), src_idx)
        tgt_key = get_item_or_none(list(target_keys.keys()), tgt_idx)

        src_key_upper = src_key.upper() if src_key is not None else None
        tgt_key_upper = tgt_key.upper() if tgt_key is not None else None

        if src_key_upper in common_keys_upper and tgt_key_upper in common_keys_upper:
            comparison_dict = {
                'source': source_keys[src_key],
                'target': target_keys[tgt_key],
                'exists_on_source': True,
                'exists_on_target': True,
                'match': True,  # exists_on_source and exists_on_target
                'inserted_on_source': False,
                'inserted_on_target': False,
                'order_match': bool(src_idx + pos_factor==tgt_idx and src_key_upper==tgt_key_upper)
            }
            key_comp_list.append(comparison_dict)
            src_idx += 1
            tgt_idx += 1

        else:

            if tgt_key_upper not in common_keys_upper and tgt_key_upper is not None:
                comparison_dict = {
                    'source': None,
                    'target': target_keys[tgt_key],
                    'exists_on_source': False,
                    'exists_on_target': True,
                    'match': False,
                    'inserted_on_source': False,
                    'inserted_on_target': bool(src_idx + pos_factor==tgt_idx),
                    'order_match': bool(src_idx + pos_factor==tgt_idx)
                }
                key_comp_list.append(comparison_dict)
                tgt_idx += 1
                pos_factor += 1

            if src_key_upper not in common_keys_upper and src_key_upper is not None:
                comparison_dict = {
                    'source': source_keys[src_key],
                    'target': None,
                    'exists_on_source': True,
                    'exists_on_target': False,
                    'match': False,
                    'inserted_on_source': bool(src_idx + pos_factor==tgt_idx),
                    'inserted_on_target': False,
                    'order_match': bool(src_idx + pos_factor==tgt_idx)
                }
                key_comp_list.append(comparison_dict)
                src_idx += 1
                pos_factor -= 1

    return key_comp_list


class KeysComparisonResult:
    """Stores data about comparison result of 2 lists of keys"""

    def __init__(self, source, target, exists_on_source, exists_on_target, match, inserted_on_source,
                 inserted_on_target, order_match):
        self.source = source
        self.target = target
        self.exists_on_source = exists_on_source
        self.exists_on_target = exists_on_target
        self.match = match
        self.inserted_on_source = inserted_on_source
        self.inserted_on_target = inserted_on_target
        self.order_match = order_match

    def __repr__(self):
        return f'({self.source}, {self.target})'


def compare_keys(source, target, key=None) -> List[KeysComparisonResult]:
    getter = key if key is not None else lambda a: a
    # dict key insertion order
    source_keys = {getter(i): i for i in source}
    target_keys = {getter(i): i for i in target}

    res = compare_keys_zip(source_keys, target_keys)
    keys_comparison = [KeysComparisonResult(**r) for r in res]

    return keys_comparison


class AttributesComparisonResult:
    COMPARISON_RESULT_SCORECARD = {
        'precision_match': lambda x: (not x) * 5,
        'precision_higher_on_target': lambda x: x * 1,
        'precision_higher_on_source': lambda x: x * 2,
        'scale_match': lambda x: (not x) * 5,
        'scale_higher_on_target': lambda x: x * 1,
        'scale_higher_on_source': lambda x: x * 2,
        'type_name_match': lambda x: (not x) * 50
    }

    def __init__(self, source: ColumnDescription, target: ColumnDescription, relation=None):
        self.relation = relation
        self.source = source
        self.target = target

        # calculate comparison result flags
        precision_is_comparable = source.precision is not None and target.precision is not None
        scale_is_comparable = source.scale is not None and target.scale is not None
        self.precision_match = source.precision==target.precision if precision_is_comparable else True
        self.precision_higher_on_target = source.precision < target.precision if precision_is_comparable else False
        self.precision_higher_on_source = source.precision > target.precision if precision_is_comparable else False
        self.scale_match = source.scale==target.scale if scale_is_comparable else True
        self.scale_higher_on_target = source.scale < target.scale if scale_is_comparable else False
        self.scale_higher_on_source = source.scale > target.scale if scale_is_comparable else False
        self.type_name_match = source.type_name==target.type_name

        self.scale_factor = target.scale - source.scale if scale_is_comparable else 0
        self.precision_factor = target.precision - source.precision if precision_is_comparable else 0

        # count comparison score
        self.scorecard = self.COMPARISON_RESULT_SCORECARD
        self.score = self.calculate_score()

        self.match = self.score==0

    def calculate_score(self):
        score = sum([self.scorecard[k](v) for k, v in vars(self).items() if k in self.scorecard])
        return score

    def set_score(self):
        self.score = self.calculate_score()

    def __repr__(self):
        return f'({self.match=}, {self.type_name_match=}, {self.scale_match=}, {self.precision_match=})'


class ColumnComparisonResult:

    def __init__(self, source: ColumnDescription, target: ColumnDescription):
        # store source and tet columns data
        self.source = source
        self.target = target

        # Get all mapping functions for source column to target database system
        relations = get_relations(src_col=source, tgt_col=target)
        # Map source column using every returned relation
        mapped_source_columns = [rel(source) for rel in relations]
        # Compare mapped fields with target field
        self.attr_comp_results = [
            AttributesComparisonResult(src_mapped_column, target)
            for src_mapped_column, relation in zip(mapped_source_columns, relations)
        ]
        self.attr_comp_results.sort(key=attrgetter('score'))

        self.match = self.attr_comp_results[0].match

    def best_result(self) -> AttributesComparisonResult:
        return self.attr_comp_results[0]

    def __repr__(self):
        if self.attr_comp_results:
            return repr(self.best_result())
        return 'N/A'


class KeyColumnComparisonResult:
    def __init__(self, key: KeysComparisonResult, col: ColumnComparisonResult):
        self.key = key
        self.col = col
        self.match = key.match and col.match

        attr = self.col.best_result() if self.col is not None else None

        self.precision_match = attr.precision_match if attr is not None else None
        self.sacle_match = attr.scale_match if attr is not None else None
        self.type_name_match = attr.type_name_match if attr is not None else None
        self.precision_factor = attr.precision_factor if attr is not None else None
        self.scale_factor = attr.scale_factor if attr is not None else None

    def __repr__(self):
        return f'{repr(self.key)} - {repr(self.col)}'


class ColumnsComparisonResult:
    """
    This class stores compare_column_lists result [Dict] and provides some methods for analyzing comparison result.
    """

    def __init__(self, source_columns: List[ColumnDescription], target_columns: List[ColumnDescription]):
        self.source_columns = source_columns
        self.target_columns = target_columns

        self.src_cols_dict = {col_desc.name: col_desc for col_desc in source_columns}
        self.tgt_cols_dict = {col_desc.name: col_desc for col_desc in target_columns}

        self.keys_comparison = compare_keys(source_columns, target_columns, key=attrgetter('name'))

        # columns comparison - using target column for comparing attributes for matching columns
        self.columns_comparison = [
            ColumnComparisonResult(self.src_cols_dict[kc.target.name], self.tgt_cols_dict[kc.target.name])
            if kc.match else None
            for kc in self.keys_comparison
        ]

        self.kc_result = [
            KeyColumnComparisonResult(k, c)
            for k, c in zip(self.keys_comparison, self.columns_comparison)]

    def __iter__(self):
        return iter(self.kc_result)

    def __len__(self):
        return len(self.keys_comparison)

    def __str__(self):
        max_src = self.get_column_str_max_len('source')
        max_tgt = self.get_column_str_max_len('target')

        header = 'SOURCE TARGET MATCH ORDER_MATCH TYPE_MATCH ATTR_MATCH'.split()
        row_format = '{:>' + str(max_src + 3) + '} | {:' + str(max_tgt + 3) + '} - {:^20}|{:^20}|{:^20}|{:^20}|'
        rows = []
        for kc in self:
            key = kc.key
            source = key.source  # if key is not None else None
            target = key.target  # if key is not None else None
            match = kc.match
            order_match = key.order_match
            type_match = kc.type_name_match
            attr_match = kc.precision_match and kc.sacle_match

            r = map(str, [source, target, match, order_match, type_match, attr_match])

            rows.append(r)
        output_rows = [row_format.format(*header)] + [row_format.format(*r) for r in rows]
        output_string = '\n'.join(output_rows)
        # [row_format.format(header)]# +
        return output_string

    def __repr__(self):
        return str([repr(kc) for kc in self])


    def get_column(self, col_name, col_source='target'):
        """
        Search and return specified column from comparison_result.

        :param col_name: Column name to look for.
        :param col_source: Specify if column will be looked for in 'source' or 'target' columns.
        :return: comparison_result row with specified column.
        """

        try:
            for c in self.comparison_result:
                if c[col_source].name==col_name:
                    return c
        except KeyError:
            raise KeyError("col_source must have value of 'source' or 'target'.")

    def match(self, order=True):
        """
        Checks if target columns match source columns in terms of names, orders and columns attributes.
        :param order: Default True. Set to False if want to ommit order checking.
        :return: True/False
        """
        # Catching KeyError when 'attributes_comparison_results' doesn't exist (no matching field on source/target)
        try:
            for kc in self:
                if not (kc.key.match and (kc.key.order_match or not order) and kc.col.match):
                    return False
        except KeyError:
            return False
        return True

    def get_column_str_max_len(self, col_source='target'):
        """
        Gets longest column string representation on 'source' or 'target'
        :param col_source: 'source' or 'target'
        :return: length of longest column string representation
        """
        if col_source=='target':
            col_list = self.target_columns
        elif col_source=='source':
            col_list = self.source_columns
        else:
            raise KeyError("col_source must have value of 'source' or 'target'.")
        return max([len(str(c)) for c in col_list])

    def order_by_source(self):
        """
        Returns new object with soruce and target fields ordered by source fields
        :return:
        """
        inf = len(self.source_columns) + len(self.target_columns)
        source_order = {c.name: i for i, c in enumerate(self.source_columns)}
        target_order = {c.name: source_order.get(c.name, inf+i) for i, c in enumerate(self.target_columns)}
        target_columns_ordered_by_source = sorted(self.target_columns, key=lambda x:target_order[x.name])
        return ColumnsComparisonResult(self.source_columns, target_columns_ordered_by_source)

    def order_by_target(self):
        """
        Returns new object with soruce and target fields ordered by target fields
        :return:
        """
        inf = len(self.source_columns) + len(self.target_columns)
        target_order = {c.name: i for i, c in enumerate(self.target_columns)}
        source_order = {c.name: target_order.get(c.name, inf+i) for i, c in enumerate(self.source_columns)}
        source_columns_ordered_by_target = sorted(self.source_columns, key=lambda x:source_order[x.name])
        return ColumnsComparisonResult(source_columns_ordered_by_target, self.target_columns)


# TODO change compare source / target functions to "order" funcns
# zip will be the basic for sorting
# for sorting keygetter will be used to get zip string, and string with field name will be mapped to position on source/target


# def _compare_keys_source(source_keys, target_keys):
#     l1 = [(src_key, src_key if src_key in target_keys else None) for src_key in source_keys.keys()]
#     l2 = [(None, tgt_key) for tgt_key in target_keys if tgt_key not in source_keys]
#     l3 = l1 + l2
#     a = 1


def validate_compare_query(query):
    if is_schema_dot_table_string(query):
        return schema_table_name_to_query(query)
    if is_select_statement(query):
        return query
    else:
        raise ValueError('Invalid statement. Must be schema.table or SELECT statement.')


def compare(source_connection, source_query, target_connection, target_query,
            source_get_meta=None, target_get_meta=None):
    # TODO - metadata provider dispatching based on connection object
    # validsate query - check if it is quyery or schema.table, check if theres only one query, chec if it is select query.
    src_sql = validate_compare_query(source_query)
    tgt_sql = validate_compare_query(target_query)

    source_meta_func = source_get_meta if source_get_meta is not None else get_meta_provider(source_connection)
    target_meta_func = target_get_meta if target_get_meta is not None else get_meta_provider(target_connection)

    src_cols = source_meta_func(source_connection, src_sql)
    tgt_cols = target_meta_func(target_connection, tgt_sql)

    result = ColumnsComparisonResult(src_cols, tgt_cols)
    return result
