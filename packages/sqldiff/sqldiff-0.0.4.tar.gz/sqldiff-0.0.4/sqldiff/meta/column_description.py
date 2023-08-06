import functools


class ColumnDescription:
    """
    PEP 249 - https://www.python.org/dev/peps/pep-0249/
    DB API Cursor description provides sequence of 7 items describing one result column:
    name, type_code, display_size, internal_size, precision, scale, null_ok
    The first two items (name and type_code) are mandatory,
    the other five are optional and are set to None if no meaningful values can be provided.

    Thi class contains additional fields such as:
    source database type (dbsystem),
    type_name (not provided in cursor desciption),
    position
    """

    def __init__(self, name, type_code, display_size, internal_size,
                 precision, scale, null_ok, type_name, position, dbsystem):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok
        self.type_name = type_name
        self.position = position
        self.dbsystem = dbsystem

    def __repr__(self):
        column_desc = f"ColumnDescription({self.position=}, {self.dbsystem=}, {self.name=}, {self.type_name=}, " \
                      f"{self.precision=}, {self.scale=}, {self.internal_size=}, " \
                      f"{self.null_ok=}, {self.display_size=}, {self.type_code=})"
        column_desc = column_desc.replace('self.', '')
        return column_desc

    def __str__(self):
        s_prec = str(self.precision) if self.precision is not None else ''
        s_scale = str(self.scale) if self.scale is not None else ''
        s = f'{self.name} {self.type_name}({", ".join(filter(None, (s_prec, s_scale)))})'.replace('()', '')
        return s

    @functools.cached_property
    def dict(self):
        return {
            self.name: self
        }