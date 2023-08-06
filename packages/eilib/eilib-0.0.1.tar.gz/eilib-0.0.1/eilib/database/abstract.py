import logging
import math
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Generic, Iterator, TypeVar

from . import schemas
from .basic_types import BasicList, BasicType
from .helpers import SectionScope, friendly_name_to_varname, parse_custom_type, read_exactly, \
                     write_section_header

log = logging.getLogger("eilib.database")
VT = TypeVar("VT")


class EiDatabaseCustomType(ABC):

    __slots__ = (
        '_schema',
        '_type_schema',
    )

    def __init__(self):
        class_name = self.__class__.__name__
        for schema in schemas.SCHEMAS_LIST:
            if class_name not in schema["types"]:
                continue

            log.debug("Found a custom type schema for class '%s'", class_name)
            self._schema = schema
            self._type_schema = schema["types"][class_name]
            break
        else:
            raise Exception(f"Failed to find a custom type schema for class '{class_name}'")

    def __eq__(self, value2):
        value1 = self
        if type(value1) is not type(value2):
            raise TypeError
        if isinstance(self._type_schema, list):
            field_names = [friendly_name_to_varname(field['name']) for field in self._type_schema]
        elif isinstance(self._type_schema, dict):
            field_names = [friendly_name_to_varname(name) for name in self._type_schema["names"]]
        else:
            assert False, "Unsupported custom type schema"

        for field_name in field_names:
            field_val1 = getattr(value1, field_name)
            field_val2 = getattr(value2, field_name)
            if field_val1 is not field_val2 and field_val1 != field_val2:
                try:
                    if math.isnan(field_val1) and math.isnan(field_val2):
                        continue
                except TypeError:
                    pass
                return False
        return True

    @classmethod
    def encode(cls, value) -> bytes:
        if isinstance(value._type_schema, list):
            buf = BytesIO()
            for field in value._type_schema:
                field_val = getattr(value, friendly_name_to_varname(field['name']))
                field_data = field['type'].encode(field_val)
                write_section_header(buf, field['id'], len(field_data))
                buf.write(field_data)
            return buf.getvalue()
        if isinstance(value._type_schema, dict):
            names = value._type_schema["names"]
            values = [getattr(value, friendly_name_to_varname(name)) for name in names]
            return value._type_schema["base"].encode(values)
        assert False, "Unsupported custom type schema"
        return None

    @classmethod
    def decode(cls, data: bytes):
        result = cls()
        if isinstance(result._type_schema, list):
            buf = BytesIO(data)
            for field in result._type_schema:
                with SectionScope(buf, field['id']) as scope:
                    data = read_exactly(buf, scope.size)
                    assert isinstance(field['type'], BasicType), (
                        "Only basic types are supported in custom types")
                    value = field['type'].decode(data)
                    setattr(result, friendly_name_to_varname(field['name']), value)
        elif isinstance(result._type_schema, dict):
            names = result._type_schema["names"]
            values = result._type_schema["base"].decode(data)
            for name, value in zip(names, values):
                setattr(result, friendly_name_to_varname(name), value)
        else:
            assert False, "Unsupported custom type schema"
        return result


class EiDatabaseTableRow(ABC):

    __slots__ = (
        '_schema',
        '_table_schema',
    )

    _custom_types = None

    def __init__(self):
        # Find schema
        class_name = self.__class__.__name__
        for schema in schemas.SCHEMAS_LIST:
            for table in schema["tables"]:
                if table["name"].replace(" ", "").lower() == class_name.lower() + "s":
                    log.debug("Found a table schema '%s' for class '%s'", table["name"], class_name)
                    break
            else:
                continue

            self._schema = schema
            self._table_schema = table
            break
        else:
            raise Exception(f"Failed to find a table schema for class '{class_name}'")

    def __eq__(self, row2):
        row1 = self
        if type(row1) is not type(row2):
            raise TypeError

        for field in self._table_schema['fields']:
            field_name = friendly_name_to_varname(field['name'])
            val1 = getattr(row1, field_name)
            val2 = getattr(row2, field_name)
            if val1 is not val2 and val1 != val2:
                try:
                    if math.isnan(val1) and math.isnan(val2):
                        continue
                except TypeError:
                    pass
                return False
        return True

    @property
    @abstractmethod
    def _db_type(self):
        pass

    def _parse_custom_type(self, field_type):
        field_type, is_list, fixed_size = parse_custom_type(field_type)

        field_type = self._db_type._custom_types[field_type]
        if is_list:
            field_type = BasicList(field_type, fixed_size)

        return field_type

    def save(self, f):
        for field in self._table_schema['fields']:
            value = getattr(self, friendly_name_to_varname(field['name']))
            if isinstance(field['type'], BasicType):
                data = field['type'].encode(value)
            elif isinstance(field['type'], str):
                data = self._parse_custom_type(field['type']).encode(value)
            else:
                assert False, "Unsupported field type"
            write_section_header(f, field['id'], len(data))
            f.write(data)

    def load(self, f):
        for field in self._table_schema['fields']:
            with SectionScope(f, field['id']) as scope:
                data = read_exactly(f, scope.size)
                if isinstance(field['type'], BasicType):
                    value = field['type'].decode(data)
                elif isinstance(field['type'], str):
                    value = self._parse_custom_type(field['type']).decode(data)
                else:
                    assert False, "Unsupported field type"
                setattr(self, friendly_name_to_varname(field['name']), value)


class EiDatabaseTable(Generic[VT], ABC):

    __slots__ = (
        '_schema',
        '_table_schema',
        '_rows',
    )
    _row_type: EiDatabaseTableRow = None

    def __init__(self):
        class_name = self.__class__.__name__
        for schema in schemas.SCHEMAS_LIST:
            for table in schema["tables"]:
                if table["name"].replace(" ", "").lower() == class_name.lower():
                    log.debug("Found a table schema '%s' for class '%s'", table["name"], class_name)
                    break
            else:
                continue

            self._schema = schema
            self._table_schema = table
            self._rows = []
            break
        else:
            raise Exception(f"Failed to find a table schema for class '{class_name}'")

    def __eq__(self, table2):
        table1 = self
        if type(table1) is not type(table2):
            raise TypeError

        for row1, row2 in zip(table1, table2):
            if row1 != row2:
                return False
        return True

    def save(self, f):
        with BytesIO() as buf:
            for row in self._rows:
                with BytesIO() as row_buf:
                    row.save(row_buf)
                    data = row_buf.getvalue()
                write_section_header(buf, 1, len(data))
                buf.write(data)
            data = buf.getvalue()
        write_section_header(f, self._table_schema['id'], len(data))
        f.write(data)

    def load(self, f):
        with SectionScope(f, self._table_schema['id']) as scope:
            self._rows = []
            while f.tell() < scope.end_pos:
                with SectionScope(f, 1):
                    assert isinstance(self._row_type, type)
                    row: EiDatabaseTableRow = self._row_type()
                    row.load(f)
                    self._rows.append(row)

    def __getitem__(self, key: int) -> VT:
        return self._rows[key]

    def __len__(self):
        return len(self._rows)

    def __iter__(self) -> Iterator[VT]:
        return iter(self._rows)


class EiDatabase(ABC):

    __slots__ = (
        '_schema',
        '_tables',
        '_db_end_magic',
    )
    _custom_types = None

    def __init__(self):
        class_name = self.__class__.__name__
        for schema in schemas.SCHEMAS_LIST:
            if schema["name"].lower() + "database" != class_name.lower():
                continue

            log.debug("Found a database schema for class '%s'", class_name)
            self._schema = schema
            break
        else:
            raise Exception(f"Failed to find a database schema for class '{class_name}'")

        # Cache tables
        self._tables = tuple(
            getattr(self, friendly_name_to_varname(table['name']))
            for table in self._schema['tables']
        )

        # It looks like some sections, but it's always the same
        self._db_end_magic = bytes([0, 0, 2, 12, 2, 8, 1, 0, 0, 0])

    def __eq__(self, database2):
        database1 = self
        if type(database1) is not type(database2):
            raise TypeError

        for table1, table2 in zip(database1.tables, database2.tables):
            if table1 != table2:
                return False
        return True

    def save(self, f):
        # Write tables
        with BytesIO() as buf:
            for table in self._schema['tables']:
                getattr(self, friendly_name_to_varname(table['name'])).save(buf)
            data = buf.getvalue()
        write_section_header(f, 1, len(data))
        f.write(data)

        # Write the end of database
        f.write(self._db_end_magic)

    def load(self, f):
        # Read tables
        with SectionScope(f, 1):
            for table in self._schema['tables']:
                getattr(self, friendly_name_to_varname(table['name'])).load(f)

        # Read the end of database
        remaining_data = read_exactly(f, len(self._db_end_magic))
        if remaining_data != self._db_end_magic:
            raise Exception('Invalid db file magic', f)

    @property
    def tables(self):
        return self._tables
