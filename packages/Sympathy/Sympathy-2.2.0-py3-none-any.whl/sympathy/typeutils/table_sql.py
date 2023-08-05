# This file is part of Sympathy for Data.
# Copyright (c) 2013, Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import struct
import binascii
import datetime
import numpy as np
import re
import os
import sqlite3
import sqlalchemy
import sys
from decimal import Decimal
from contextlib import contextmanager


def _pyodbc():
    """
    Avoid pre-loading pyodbc.
    """
    import pyodbc
    return pyodbc


def odbc_module(method_name):

    if method_name == 'ceODBC':
        try:
            import ceODBC
            return ceODBC
        except ImportError as e:
            print('Using default ODBC due to: {}'.format(e))
    return _pyodbc()


def get_interface(dbtype, dburl, odbc_name=None, capture_exc=True):
    if odbc_name is not None:
        try:
            odbc_module_ = odbc_module(odbc_name)
        except ImportError:
            odbc_module_ = None

    try:
        if dbtype == 'FILE':
            for filedb in filedbs:
                res = filedb(dburl)
                if res.is_valid():
                    return res
        elif dbtype == 'DATABASE':
            # DIRECT ODBC connection.
            return ODBCDatabase(dburl, odbc_module_)
        elif dbtype == 'DATABASE SQLALCHEMY':
            # SQLALCHEMY connection.
            return SQLAlchemyDatabase(dburl)
        return NullDatabase(dburl, None)
    except:
        if capture_exc:
            return NullDatabase(dburl, sys.exc_info())
        else:
            raise


def get_interface_guess_database(dburl, odbc_name=None, capture_exc=True):

    # TODO(Erik): No need to guess, all information
    # is directly available in the datasource.

    if dburl is None:
        dbtype = None
    elif dburl.find('://') > -1:
        # Guess that we have sqlalchemy engine.
        dbtype = 'DATABASE SQLALCHEMY'
    else:
        dbtype = 'DATABASE'

    return get_interface(dbtype, dburl, odbc_name, capture_exc=capture_exc)


class IDatabase(object):
    """
    Convenience interface for databases used by importer and exporter plugins.
    """
    exc_info = None

    @contextmanager
    def to_rows_table(self, table_name, columns=None):
        """
        Return the result of selecting all columns from table name as in a
        tuple together with the column names.

        Format: (column_names, data row iterator) object.
        """
        raise NotImplementedError

    @contextmanager
    def to_rows_query(self, query):
        """
        Return the result of executing query in a
        tuple together with the column names.

        Format: (column_names, data row iterator) object.
        """
        raise NotImplementedError

    def table_names(self):
        """
        Return the table names as a sorted list.
        """
        raise NotImplementedError

    def table_column_names(self, table_name):
        """
        Return the column names for table_name.
        """
        raise NotImplementedError

    def from_table(self, table_name, table, **kwargs):
        """
        Write the data from table argument to the database table called
        table_name.
        """
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class IFileDatabase(IDatabase):
    """
    Convenience interface for file-based databases used by importer and export
    plugins.
    """

    def __init__(self, fq_filename):
        self.fq_filename = fq_filename

    def is_valid(self):
        """Return True if self is a suitable interface for self.fq_filename."""
        raise NotImplementedError


class NullDatabase(IDatabase):
    def __init__(self, url, exc_info=None):
        self._url = url
        self.exc_info = exc_info

    def to_rows_table(self, table_name, columns=None):
        return self.to_rows_query('select * from %s' % table_name)

    @contextmanager
    def to_rows_query(self, query):
        yield [], []

    def table_names(self):
        return []

    def table_column_names(self, table_name):
        return []

    def from_table(self, table_name, table, **kwargs):
        return []

    def close(self):
        pass


class SQLAlchemyDatabase(IDatabase):
    def __init__(self, engine_url):
        self._engine = sqlalchemy.create_engine(engine_url)
        self._meta = sqlalchemy.MetaData()
        self._meta.reflect(bind=self._engine)

    def to_rows_table(self, table_name, columns=None):
        return self.to_rows_query('select * from %s' % table_name)

    def to_rows_query(self, query):
        conn = self._engine.raw_connection()
        return to_rows_query(conn, query)

    def table_names(self):
        return list(sorted(self._meta.tables.keys()))

    def table_column_names(self, table_name):
        return self._meta.tables[table_name].columns.keys()

    def from_table(self, table_name, table, **kwargs):
        column_names = table.column_names()

        self._engine.execute(
            self._meta.tables[table_name].insert(),
            [dict(zip(column_names, row)) for row in table.to_rows()])

    def close(self):
        self._engine = None
        self._meta = None


class ODBCDatabase(IDatabase):
    def __init__(self, connection_string, odbc_module):
        assert odbc_module is not None, (
            'Cannot connect to database without ODBC module.')
        self._odbc_module = odbc_module
        self._conn = odbc_module.connect(connection_string)

    def to_rows_table(self, table_name, columns=None):
        return self.to_rows_query('select * from %s' % table_name)

    def to_rows_query(self, query):
        return to_rows_query(self._conn, query)

    def table_names(self):
        cursor = self._conn.cursor()
        return list(sorted(elt[2] for elt in cursor.tables()
                           if elt[3] == 'TABLE'))

    def table_column_names(self, table_name):
        return read_table_column_names(self._conn, table_name)

    def from_table(self, table_name, table, **kwargs):
        table_to_odbc(self._conn, table, table_name, **kwargs)

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


def fix_sql_table_name(table_name):
    """Remove characters not allowed in sqlite table name."""
    return ''.join(letter for letter in table_name
                   if (letter.isalnum() or letter == '_'))


@contextmanager
def to_rows_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(str(query))
    except Exception as e:
        raise ValueError('{}'.format(e))
    except:
        raise ValueError('Not a valid SQL query.')
    try:
        # Get cursor description information on the form:
        # [(name, type_code, None, internal_size, precision, 0, null_ok)]
        names = [entry[0] for entry in cursor.description]

        # Check types of elements in the columns
        yield (names, convert_types(cursor))
    except TypeError:
        raise ValueError('Not a valid SQLite query')


@contextmanager
def read_rows_from_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(str(query))
    except Exception as e:
        raise ValueError('{}'.format(e))
    except:
        raise ValueError('Not a valid SQL query.')
    try:
        names = [entry[0] for entry in cursor.description]
        yield (names, cursor)
    except TypeError:
        raise ValueError('Not a valid SQL query')


@contextmanager
def read_rows_from_table(conn, table_name, columns=None):
    """
    Open a database, read columns from table and
    return as numpy record.
    """
    cursor = conn.cursor()
    column_string = None
    if columns is None:
        column_string = '*'
    else:
        column_string = ','.join(columns)
    assert(column_string is not None)

    cursor.execute("SELECT %s FROM %s" % (column_string, table_name))
    names = [entry[0] for entry in cursor.description]
    yield (names, cursor)


def read_table_column_names(conn, table_name):
    # Connect and get table names for database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" % table_name)
    description = cursor.description
    unzip_descr = zip(*list(description))
    column_names = list(unzip_descr)[0]
    return sorted(column_names)


def write_table_sqlite3(conn, table_name, table):
    """Write table to sqlite 3."""
    if table.number_of_columns() == 0:
        print('Cannot create empty table [{}].'.format(table_name))
        return

    if table_name == "":
        table_name = 'from_table'
    else:
        table_name = fix_sql_table_name(table_name)

    # Fick problem med utf-8 nar jag korde fran csv-filer annars.. Fult?
    conn.text_factory = str
    cursor = conn.cursor()
    names = table.column_names()
    input_types = [table.column_type(name) for name in names]
    # Fix illegal column names
    names = [
        '[{}]'.format(re.sub(r'[\\[\\]\\(\\)]', '', name))
        for name in names]
    types = []

    for input_type in input_types:
        input_type_base = input_type.str[:2]
        if input_type_base == '<i':
            types.append('integer')
        elif input_type_base == '<f':
            types.append('real')
        elif input_type_base == '|b':
            types.append('bit')
        elif input_type_base == '<M':
            types.append('datetime')
        elif input_type_base in ['<U', '|S']:
            types.append('text')
        else:
            raise NotImplementedError(
                'Type {} not implemented.'.format(input_type.str))

    assert(len(names) == len(types))

    columns = ', '.join(['{} {}'.format(iname, itype)
                         for iname, itype in zip(names, types)])
    sqlite_data = table.to_rows()
    sqlite_names = ', '.join(names)

    create_str = ("CREATE TABLE IF NOT EXISTS " + table_name +
                  " (" + columns + ")")

    # Create table from create_str.
    cursor.execute(create_str)
    insert_str = ("INSERT INTO " + table_name + "(" + sqlite_names +
                  ") VALUES(")
    insert_qm = ['?' for name in names]
    insert_qm_string = ','.join(insert_qm)
    insert_str += insert_qm_string + ')'

    type_dict = {np.int: int,
                 np.int8: int,
                 np.int16: int,
                 np.int32: int,
                 np.int64: int,
                 np.int32: int,
                 np.uint: int,
                 np.uint8: int,
                 np.uint16: int,
                 np.uint32: int,
                 np.uint64: int,
                 np.uint32: int,
                 np.float: float,
                 np.float16: float,
                 np.float32: float,
                 np.float64: float,
                 np.string_: str,
                 str: str,
                 bytes: bytes,
                 np.unicode_: str,
                 np.bool: bool,
                 np.complex: str,
                 np.complex64: str,
                 type(None): lambda x: None}
    try:
        sqlite_data = [tuple(type_dict[type(sqlite_item)](sqlite_item)
                       for sqlite_item in sqlite_row)
                       for sqlite_row in sqlite_data]
    except Exception:
        import traceback
        traceback.print_exc()
        raise KeyError("Data type not valid.")
    # Create table from insert_str and data from table.
    cursor.executemany(insert_str, sqlite_data)
    conn.commit()


def read_table_names_pyodbc(conn):
    # Connect and get table names for database
    cursor = conn.cursor()
    table_names = [table.table_name for table in cursor.tables()
                   if table.table_type == 'TABLE']
    return list(sorted(table_names))


def build_where_query(tables, columns, join_columns, where_conditions):
    """Return a SQL query from input arguments using WHERE."""
    query = 'SELECT '
    query += ', '.join(columns)
    query += ' FROM '
    query += ', '.join(tables)
    if join_columns or where_conditions:
        query += ' WHERE '
    joins = []

    if join_columns:
        for ind in range(1, len(join_columns), 2):
            joins.append(join_columns[ind - 1] + '=' + join_columns[ind])
        query += ' AND '.join(joins)
    if where_conditions:
        if join_columns:
            query += ' AND '
        query += ' AND '.join(where_conditions)

    return query


class SQLite3Database(IFileDatabase):
    def __init__(self, fq_filename, read_only=False):
        super(SQLite3Database, self).__init__(fq_filename)
        self._valid = False
        self._conn = None

        if read_only and not (fq_filename and os.path.isfile(
                fq_filename)):
            self._valid = False
        else:

            try:
                with open(fq_filename, 'rb') as sqlite_file:
                    try:
                        s = sqlite_file.read(1024)
                        s_h = binascii.hexlify(s)
                        if s_h[0:32] == b'53514c69746520666f726d6174203300':
                            self._valid = True

                    except sqlite3.Error:
                        self._valid = False
            except IOError:
                self._valid = False

            try:
                self._conn = sqlite3.connect(fq_filename)
            except Exception:
                self._valid = False

    def is_valid(self):
        return self._valid

    def to_rows_table(self, table_name, columns=None):
        return read_rows_from_table(self._conn, table_name, columns)

    def to_rows_query(self, query):
        return read_rows_from_query(self._conn, query)

    def table_names(self):
        # Connect and get table names for database
        cursor = self._conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        # tables: list with tuples containing table names.
        # Extra table: sqlite_sequence
        # needs to be removed and 'strings' need to be converted to 'strings'
        table_names = [str(table[0]) for table in tables
                       if table[0] != 'sqlite_sequence']
        return list(sorted(table_names))

    def table_column_names(self, table_name):
        return read_table_column_names(self._conn, table_name)

    def from_table(self, table_name, table, **kwargs):
        return write_table_sqlite3(self._conn, table_name, table)

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


class AccessFileHeader:
    """
    Check if file is a Microsoft Access Database.
    Recognizes Access 97-2010.
    """
    _header_fmt = '<L16sL'
    _header_size = struct.calcsize(_header_fmt)

    @classmethod
    def _get_stream_info(cls, stream):
        const, ident, version = struct.unpack(
            cls._header_fmt,
            stream.read(cls._header_size))
        ident = ident.split(b'\0', 1)[0].decode('latin1')
        return const, ident, version

    @classmethod
    def _is_info_valid(cls, const, ident, version):
        if const != 0x100:
            res = False
        else:
            if ident == 'Standard Jet DB':
                # 0: Access 97, 1: Access 2000-2003
                res = version in [0, 1]
            elif ident == 'Standard ACE DB':
                # 2: Access 2007 0x103: Access 2010
                res = version in [2, 0x103]
            else:
                res = False
        return res

    @classmethod
    def is_stream_valid(cls, stream):
        try:
            info = cls._get_stream_info(stream)
        except Exception:
            res = False
        else:
            res = cls._is_info_valid(*info)
        return res

    @classmethod
    def is_file_valid(cls, filename):
        with open(filename, 'rb') as f:
            return cls.is_stream_valid(f)


class MDBDatabase(IFileDatabase):
    """
    Import Microsoft Access database files using the ODBC driver if it is
    available. The driver is installed with office and can also be installed
    separately.
    """
    def __init__(self, fq_filename,  read_only=True, connect=True):
        super(MDBDatabase, self).__init__(fq_filename)
        self._conn = None
        self._valid = False
        if not read_only:
            raise NotImplementedError()

        if fq_filename:
            access_file = self._is_file_access_format(fq_filename)
            if not (read_only and not access_file):
                try:
                    if connect:
                        self._conn = _pyodbc().connect(self.connection_string)
                        self._valid = self._conn is not None
                    else:
                        self._valid = True
                except Exception:
                    pass
    @property
    def connection_string(self):
        return (
            'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %
            self.fq_filename)

    def _is_file_access_format(self, filename):
        return (os.path.isfile(filename) and
                AccessFileHeader.is_file_valid(filename))

    def is_valid(self):
        return self._valid

    def to_rows_table(self, table_name, columns=None):
        return read_rows_from_table(self._conn, table_name, columns)

    def to_rows_query(self, query):
        return table_from_odbc_query(self._conn, query)

    def table_names(self):
        return read_table_names_pyodbc(self._conn)

    def table_column_names(self, table_name):
        return read_table_column_names(self._conn, table_name)

    def from_table(self, table_name, table, **kwargs):
        raise NotImplementedError

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


def table_to_odbc(conn, table, table_name, drop_table=False,
                  use_nvarchar_size=False):
    """Write table to ODBC."""
    def nan_to_none(x):
        None if np.isnan(x) else float(x)

    if table is None:
        raise IOError(
            'A table without columns is not possible to export to a database.')

    if table.number_of_columns() == 0:
        print('Cannot create empty table [{}].'.format(table_name))
        return

    if table_name == "":
        table_name = 'from_table'
    else:
        table_name = fix_sql_table_name(table_name)
    cursor = conn.cursor()
    names = table.column_names()
    input_types = [table.column_type(name) for name in names]

    # Fix illegal column names
    names = [
        '[{}]'.format(re.sub('[-\\[\\]\\(\\)]', '', name)) for name in names]
    types = []

    for input_type in input_types:
        input_type_base = input_type.str[:2]

        if input_type_base == '<i':
            types.append('int')
        elif input_type_base == '<f':
            types.append('float')
        elif input_type_base == '|b':
            types.append('bit')
        elif input_type_base == '<M':
            types.append('datetime')
        elif input_type_base in ['<U', '|S']:
            if use_nvarchar_size:
                types.append('nvarchar({})'.format(input_type.itemsize))
            else:
                types.append('nvarchar(MAX)')
        else:
            raise NotImplementedError(
                'Type {} not implemented.'.format(input_type.str))

    assert(len(names) == len(types))

    columns = ', '.join(['{} {}'.format(iname, itype)
                         for iname, itype in zip(names, types)])

    sqlite_data = table.to_rows()
    sqlite_names = ', '.join(names)

    tables_in_database_query = 'SELECT * FROM sys.Tables'
    cursor.execute(tables_in_database_query)
    tables_in_database = [tdata[0] for tdata in cursor.fetchall()]

    if drop_table and table_name in tables_in_database:
        cursor.execute('DROP TABLE {}'.format(table_name))
    # Create if table is missing otherwise append data.
    if drop_table or table_name not in tables_in_database:
        create_table_query = 'CREATE TABLE {} ({})'.format(table_name, columns)
        cursor.execute(create_table_query)
    insert_data_query = 'INSERT INTO {} ({}) VALUES('.format(
        table_name, sqlite_names)

    insert_qm = ['?' for name in names]
    insert_qm_string = ','.join(insert_qm)
    insert_data_query += insert_qm_string + ')'

    type_dict = {float: nan_to_none,
                 datetime.datetime: str}

    try:
        sqlite_data = [tuple(type_dict.get(type(sqlite_item),
                                           type(sqlite_item))(sqlite_item)
                       for sqlite_item in sqlite_row)
                       for sqlite_row in sqlite_data]
    except KeyError:
        raise KeyError("Data type not valid.")
    # Enable autocommit or memory problems can occur.
    conn.autocommit = True
    if sqlite_data != []:
        try:
            cursor.executemany(insert_data_query, sqlite_data)
        except:
            print('input, [(type, name)]:', zip(names, input_types))
            print('output, [(type, name)]:', zip(names, types))
            print('drop_table', str(drop_table))
            raise
    conn.commit()
    conn.close()


def convert_types(rows):
    """
    Convert cells in rows accorting to the conversions dictionary.
    Values with types present in conversions will be converted.
    Values with types not present in conversions will be preserved.

    Return a new row generator with values converted in accordance with
    conversions.
    """
    conversions = {Decimal: float}

    def convert(cell):
        cell_type = type(cell)
        if cell_type in conversions:
            return conversions[cell_type](cell)
        else:
            return cell

    for row in rows:
        yield [convert(cell) for cell in row]


@contextmanager
def table_from_odbc_query(conn, query, odbc=None):
    cursor = conn.cursor()
    try:
        cursor.execute(str(query))
    except Exception as e:
        raise ValueError('{}'.format(e))
    except:
        raise ValueError('Not a valid SQLite query.')
    try:
        # Get cursor description information on the form:
        # [(name, type_code, None, internal_size, precision, 0, null_ok)]
        names = [entry[0] for entry in cursor.description]
        # Check types of elements in the columns
        yield (names, convert_types(cursor))
    except TypeError:
        raise ValueError('Not a valid SQLite query')
    finally:
        conn.close()


filedbs = [MDBDatabase, SQLite3Database]
