import unittest

from sqldiff.meta.column_description import ColumnDescription
from sqldiff.relation.relation_manager import dbmapping, mappings, get_relations_using_keys, get_relations_using_columns


class TestRelationManagerDbmappingDecorator(unittest.TestCase):
    """
    Test if @dbmapping decorator stores mapping fuions properly.
    Mapping registration shouldn't be imported into current module, so mapping dictionary is empty.
    """

    def test_single_dbsystem_string_registering(self):
        """Test if dbmapping decorator handles single dbsystems values"""

        type_name = 'type_name'
        src_dbsystem = 'src_dbsystem'
        tgt_dbsystem = 'tgt_dbsystem'

        @dbmapping(type_name, src_dbsystem, tgt_dbsystem)
        def test_function():
            pass

        self.assertIn(test_function, mappings[(type_name, src_dbsystem, tgt_dbsystem)])

    def test_multiple_dbsystem_string_registering(self):
        """Test if decorator handles dbsystems values as sequences"""

        type_name = 'type_name'
        src_dbsystems = ('src_dbsystem1', 'src_dbsystem2')
        tgt_dbsystems = ('tgt_dbsystem1', 'tgt_dbsystem2')

        @dbmapping(type_name, src_dbsystems, tgt_dbsystems)
        def test_function():
            pass

        for src_dbsystem in src_dbsystems:
            for tgt_dbsystem in tgt_dbsystems:
                self.assertIn(test_function, mappings[(type_name, src_dbsystem, tgt_dbsystem)])

    def test_get_relations_using_keys(self):
        """Test if getting relations by keys works, and returns additional idety relation function"""

        type_name = 'type_name'
        src_dbsystem = 'src_dbsystem'
        tgt_dbsystem = 'tgt_dbsystem'

        @dbmapping(type_name, src_dbsystem, tgt_dbsystem)
        def test_function():
            pass

        rel = get_relations_using_keys(type_name, src_dbsystem, tgt_dbsystem)

        self.assertEqual(len(rel), 2)


    def test_get_relations_using_keys(self):
        """Test if getting relations by ColumnDescription, and returns additional idety relation function"""

        src_col = ColumnDescription(
            name='src',
            type_code=None,
            display_size=None,
            internal_size=None,
            precision=None,
            scale=None,
            null_ok=None,
            type_name='some type',
            position=None,
            dbsystem='some db system'
        )
        tgt_col = ColumnDescription(
            name='tgt',
            type_code=None,
            display_size=None,
            internal_size=None,
            precision=None,
            scale=None,
            null_ok=None,
            type_name='some type',
            position=None,
            dbsystem='some db system2'
        )

        type_name = 'type_name'
        src_dbsystem = 'src_dbsystem'
        tgt_dbsystem = 'tgt_dbsystem'

        @dbmapping(src_col.type_name, src_col.dbsystem, tgt_col.dbsystem)
        def test_function():
            pass

        rel = get_relations_using_columns(src_col, tgt_col)

        self.assertEqual(len(rel), 2)







