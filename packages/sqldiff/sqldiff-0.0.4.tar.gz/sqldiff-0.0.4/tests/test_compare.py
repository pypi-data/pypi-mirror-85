import unittest
from copy import deepcopy
from operator import itemgetter

from sqldiff.comp.compare import compare_keys, ColumnsComparisonResult, AttributesComparisonResult, \
    ColumnComparisonResult
from sqldiff.meta.column_description import ColumnDescription
from sqldiff.relation.relation_manager import dbmapping, mappings


def create_column(dbsystem, field_name, type_name, precision=None, scale=None):
    """Shortcut function creating ColumnDescription instances for testing purposes"""
    col = ColumnDescription(
        name=field_name,
        type_code=None,
        display_size=None,
        internal_size=None,
        precision=precision,
        scale=scale,
        null_ok=None,
        type_name=type_name,
        position=None,
        dbsystem=dbsystem
    )
    return col


class TestColumnDescriptionStringRepresentation(unittest.TestCase):
    """Test if ColumnDescription __str__ method generates per SQL representation of field"""
    def test_str_column_no_attributes(self):
        col = create_column('dbsystem', 'field_name', 'INT')
        self.assertEqual(str(col), 'field_name INT')

    def test_str_column_precision_only(self):
        col = create_column('dbsystem', 'field_name', 'VARCHAR', 50)
        self.assertEqual(str(col), 'field_name VARCHAR(50)')

    def test_str_column_precision_and_scale(self):
        col = create_column('dbsystem', 'field_name', 'DECIMAL', 19, 5)
        self.assertEqual(str(col), 'field_name DECIMAL(19, 5)')


class TestCompareKeys(unittest.TestCase):
    """Test keys (field names) comparison"""

    def test_compare_keys_unequal_field_lists(self):
        """Test if _compare_keys_zip functions handles unequal fields number"""
        src_fields = ['f1', 'f2', 'f3', 'f5', 'f6']
        tgt_fields = ['f1', 'f3', 'f2', 'f4', 'f5', 'f6']

        result = compare_keys(src_fields, tgt_fields)
        result_fields = [(i.source, i.target) for i in result]
        expected_fields = [
            ('f1', 'f1'),
            ('f2', 'f3'),
            ('f3', 'f2'),
            (None, 'f4'),
            ('f5', 'f5'),
            ('f6', 'f6')
        ]

        self.assertEqual(result_fields, expected_fields)

    def test_compare_keys_unequal_field_lists_different_character_case(self):
        """Test if _compare_keys_zip functions handles unequal fields number"""
        src_fields = ['f1', 'f2', 'f3', 'F5', 'F6']
        tgt_fields = ['f1', 'F3', 'f2', 'f4', 'F5', 'f6']

        result = compare_keys(src_fields, tgt_fields)
        result_fields = [(i.source, i.target) for i in result]
        expected_fields = [
            ('f1', 'f1'),
            ('f2', 'F3'),
            ('f3', 'f2'),
            (None, 'f4'),
            ('F5', 'F5'),
            ('F6', 'f6')
        ]

        self.assertEqual(result_fields, expected_fields)

    def test_compare_keys_order_order_flag(self):
        """Test if compare keys result order flag is set correctly"""
        src_fields = ['f1', 'f2', 'f3', 'f5', 'f6']
        tgt_fields = ['f1', 'f3', 'f2', 'f4', 'f5', 'f6']

        result = compare_keys(src_fields, tgt_fields)
        result_fields = [(i.source, i.target, i.order_match) for i in result]
        expected_fields = [
            ('f1', 'f1', True),
            ('f2', 'f3', False),
            ('f3', 'f2', False),
            (None, 'f4', True),
            ('f5', 'f5', True),
            ('f6', 'f6', True)
        ]

        self.assertEqual(result_fields, expected_fields)

    def test_compare_ks_using_custom_attrgetter(self):
        """Test compare keys on complex structure using optional 'key' argument to pass attrgetter"""
        src_fields = [
            {
                'field_name': 'f1',
                'type_name': 'some_type'
            },
            {
                'field_name': 'f2',
                'type_name': 'some_type'
            },
            {
                'field_name': 'f3',
                'type_name': 'some_type'
            }
        ]
        tgt_fields = [
            {
                'field_name': 'f1',
                'type_name': 'some_type'
            },
            {
                'field_name': 'f3',
                'type_name': 'some_type'
            }
        ]

        getter = itemgetter('field_name')
        result = compare_keys(src_fields, tgt_fields, key=getter)

        result_fields = [
            (
                getter(i.source) if i.source is not None else None,
                getter(i.target) if i.target is not None else None
            ) for i in result
        ]
        expected_fields = [
            ('f1', 'f1'),
            ('f2', None),
            ('f3', 'f3'),
        ]

        self.assertEqual(result_fields, expected_fields)


class TestCompareColumnsAttributes(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_compare_column_attributes(self):
        """Test compare columntributes"""
        src_col = create_column('dbsystem1', 'field_name', 'DECIMAL', 19, 9)
        tgt_col = create_column('dbsystem2', 'field_name', 'DECIMAL', 19, 5)

        result = AttributesComparisonResult(src_col, tgt_col)

        self.assertTrue(result.precision_match)
        self.assertFalse(result.precision_higher_on_target)
        self.assertFalse(result.precision_higher_on_source)
        self.assertFalse(result.scale_match)
        self.assertFalse(result.scale_higher_on_target)
        self.assertTrue(result.scale_higher_on_source)
        self.assertTrue(result.type_name_match)

    def test_comparison_result_score_calculation(self):
        """Test comparisonm result score calculation"""

        src_col = create_column('dbsystem1', 'field_name', 'DECIMAL', 19, 9)
        tgt_col = create_column('dbsystem2', 'field_name', 'DECIMAL', 19, 5)

        attr = AttributesComparisonResult(src_col, tgt_col)

        attr.precision_match = True
        attr.precision_higher_on_target = False
        attr.precision_higher_on_source = False
        attr.scale_match = False
        attr.scale_higher_on_target = False
        attr.scale_higher_on_source = True
        attr.type_name_match = True

        attr.scorecard = {
            'precision_match': lambda x: (not x) * 5,
            'precision_higher_on_target': lambda x: x * 1,
            'precision_higher_on_source': lambda x: x * 2,
            'scale_match': lambda x: (not x) * 5,
            'scale_higher_on_target': lambda x: x * 1,
            'scale_higher_on_source': lambda x: x * 2,
            'type_name_match': lambda x: (not x) * 50
        }

        score_result = attr.calculate_score()
        self.assertEqual(score_result, 7)


class TestCompareColumnsWithoutMappings(unittest.TestCase):

    def setUp(self) -> None:
        # set up dbmappings
        # setup columns
        pass

    def test_compare_the_same_columns(self):
        """Test if comparing the same columns returns perfect match"""
        src_col = create_column('dbsystem1', 'field_name', 'DECIMAL', 19, 5)
        tgt_col = create_column('dbsystem1', 'field_name', 'DECIMAL', 19, 5)

        result = ColumnComparisonResult(src_col, tgt_col)
        # result.kc_result.

        self.assertTrue(result.best_result().precision_match)
        self.assertTrue(result.best_result().scale_match)
        self.assertTrue(result.best_result().type_name_match)

    def test_compare_different_unmapped_types(self):
        """Test if comparing the same columns returns perfect match"""
        src_col = create_column('dbsystem1', 'field_name', 'DECIMAL', 19, 5)
        tgt_col = create_column('dbsystem1', 'field_name', 'VARCHAR', 50)

        result = ColumnComparisonResult(src_col, tgt_col)

        self.assertFalse(result.best_result().precision_match)
        # scale is not comparable
        self.assertTrue(result.best_result().scale_match)
        self.assertFalse(result.best_result().type_name_match)


class CompareColumnsWithCustomMappings(unittest.TestCase):
    """Test compare_columns function with custom dbmappings registered"""

    def setUp(self) -> None:
        # TODO fix dbmapping duplication on multiple tup call
        @dbmapping('LONG VARCHAR', 'teradata')
        def teradata_long_varchar_varchar_mapping(src_col: ColumnDescription):
            ret_col = deepcopy(src_col)
            ret_col.type_name = 'VARCHAR'
            ret_col.precision = 64000
            return ret_col

        @dbmapping('LONG VARCHAR', 'teradata', 'postgres')
        def teradata_long_varchar_text_postgres_mapping(src_col: ColumnDescription):
            ret_col = deepcopy(src_col)
            ret_col.type_name = 'TEXT'
            ret_col.precision = None
            ret_col.scale = None
            return ret_col

    def test_compare_columns_matching_mapping(self):
        src_col = create_column('teradata', 'field_name', 'LONG VARCHAR')

        tgt_col = create_column('postgres', 'field_name', 'VARCHAR', 64000)
        result = ColumnComparisonResult(src_col, tgt_col)
        self.assertEqual(result.best_result().score, 0)

        tgt_col = create_column('postgres', 'field_name', 'TEXT')
        result = ColumnComparisonResult(src_col, tgt_col)
        self.assertEqual(result.best_result().score, 0)

    def test_compare_columns_not_matching_mapping(self):
        m = mappings
        src_col = create_column('teradata', 'field_name', 'LONG VARCHAR')
        tgt_col = create_column('postgres', 'field_name', 'DECIMAL', 19, 5)
        result = ColumnComparisonResult(src_col, tgt_col)
        self.assertNotEqual(result.best_result().score, 0)


class TestCompareColumnLists(unittest.TestCase):

    def test_compare_column_lists_matching_with_order(self):
        src_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f2', 'VARCHAR', 500),
            create_column('teradata', 'f3', 'DATE')
        ]

        tgt_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f2', 'VARCHAR', 500),
            create_column('teradata', 'f3', 'DATE')
        ]
        # Matching type but not the same
        result = ColumnsComparisonResult(src_cols, tgt_cols)

        self.assertTrue(result.match())
        self.assertTrue(result.match(order=False))

    def test_compare_column_lists_matching_wrong_column_order(self):
        src_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f2', 'VARCHAR', 500),
            create_column('teradata', 'f3', 'DATE')
        ]

        tgt_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f3', 'DATE'),
            create_column('teradata', 'f2', 'VARCHAR', 500)
        ]
        # Matching type but not the same
        result = ColumnsComparisonResult(src_cols, tgt_cols)

        self.assertFalse(result.match())
        self.assertTrue(result.match(order=False))

    def test_compare_not_matching_column_lists(self):
        src_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f2', 'VARCHAR', 500),
            create_column('teradata', 'f3', 'DATE'),
            create_column('teradata', 'f5', 'VARCHAR', 50),
            create_column('teradata', 'f6', 'DATE'),
            create_column('teradata', 'f7', 'VARCHAR', 100),

        ]

        tgt_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 9),
            create_column('teradata', 'f3', 'DATE'),
            create_column('teradata', 'f2', 'VARCHAR', 100),
            create_column('teradata', 'f5', 'VARCHAR', 50),
            create_column('teradata', 'f9', 'INT'),
            create_column('teradata', 'f6', 'TIMESTAMP'),
            create_column('teradata', 'f4', 'INT'),

        ]
        result = ColumnsComparisonResult(src_cols, tgt_cols)

        # Todo some more specific tests on comparison attributes
        print(result)
        self.assertFalse(result.match())

    def test_ordered_comparison_result(self):
        """Test source ordered comparison"""
        src_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 5),
            create_column('teradata', 'f2', 'VARCHAR', 500),
            create_column('teradata', 'f3', 'DATE'),
            create_column('teradata', 'f5', 'VARCHAR', 50),
            create_column('teradata', 'f6', 'DATE'),
            create_column('teradata', 'f7', 'VARCHAR', 100),

        ]

        tgt_cols = [
            create_column('teradata', 'f1', 'DECIMAL', 19, 9),
            create_column('teradata', 'f3', 'DATE'),
            create_column('teradata', 'f2', 'VARCHAR', 100),
            create_column('teradata', 'f5', 'VARCHAR', 50),
            create_column('teradata', 'f9', 'INT'),
            create_column('teradata', 'f6', 'TIMESTAMP'),
            create_column('teradata', 'f4', 'INT'),

        ]
        result = ColumnsComparisonResult(src_cols, tgt_cols)

        source_ordered = result.order_by_source()
        target_ordered = result.order_by_target()
        a = 1
