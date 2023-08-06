from sqldiff.meta.column_description import ColumnDescription
from sqldiff.meta.postgres_meta import get_meta
from sqldiff.meta.teradata_meta import get_meta

from sqldiff.comp.compare import compare, ColumnsComparisonResult, KeyColumnComparisonResult

from sqldiff.relation.relation_manager import get_relations

# launch relation registering
from sqldiff.relation import relation_register
