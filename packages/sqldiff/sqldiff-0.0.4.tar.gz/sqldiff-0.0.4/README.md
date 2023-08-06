# sqldiff
Compare 2 database objects. Object might be a table, view, or SQL query.

## Installation:
```
pip install git+https://github.com/m-matelski/sqldiff.git
```

## Handled databases (drivers)
* `psycopg2`
* `tedatasql`

## Usage
#### Compare structures
```python
import psycopg2
import teradatasql

from sqldiff.comp.compare import compare

connection_params_postgres = {
    'host': 'localhost',
    'port': '5432',
    'user': 'admin',
    'password': 'admin',
    'database': 'test_db'
}

connection_params_teradata = {
    'host': '192.168.1.6',
    'user': 'dbc',
    'password': 'dbc',
    'database': 'test_db'
}

query_postgres = 'select * from all_datatypes'
query_teradata = 'select * from all_datatypes'


with psycopg2.connect(**connection_params_postgres) as postgres_connection, \
        teradatasql.connect(**connection_params_teradata) as teradata_connection:

    result = compare(
        source_connection=teradata_connection,
        source_query=query_teradata,
        target_connection=postgres_connection,
        target_query=query_postgres)

print(result)
```

`result` is `ColumnsComparisonResult` instance. 
* `match(self, order=True)` - Checks if target columns match source columns in terms of names, orders and columns attributes. Param order: Default True. Set to False if want to ommit order checking. 

`result` can be iterated, returning `KeyColumnComparisonResult` object on every iteration which represents one 2 fields comaprison. `KeyColumnComparisonResult` `kc' has following attributes:
* `kc.match`
* `kc.precision_match` 
* `kc.scale_match`
* `kc.type_name_match`
* `kc.key.match`
* `kc.key.order_match`