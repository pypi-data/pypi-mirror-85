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
"""
Created on Mon Nov 05 08:23:41 2012

@author: Helena
"""
import re
import os
from sympathy.api import importers
from sympathy.api import table
from sympathy.api import node as synode
from sympathy.api import qt2 as qt_compat
QtCore = qt_compat.QtCore
QtGui = qt_compat.import_module('QtGui')
QtWidgets = qt_compat.import_module('QtWidgets')
sql = table.table_sql()


def get_filedbs(fq_filename):
    fq_filename = os.path.abspath(fq_filename)

    return [filedb for filedb in [sql.MDBDatabase(fq_filename, True),
                                  sql.SQLite3Database(fq_filename, True)]
            if filedb.is_valid()]


class DataImportSQLWidget(QtWidgets.QWidget):
    def __init__(self, parameters, db_interface):
        super(DataImportSQLWidget, self).__init__()
        self._parameters = parameters
        self._db_interface = db_interface
        self._init_parameters()
        self._init_gui()

    def _init_gui(self):
        vlayout = QtWidgets.QVBoxLayout()
        hlayout_simple_table = QtWidgets.QHBoxLayout()
        hlayout_query_edit = QtWidgets.QHBoxLayout()
        hlayout_join_info = QtWidgets.QHBoxLayout()
        hlayout_where = QtWidgets.QHBoxLayout()
        max_height = 150

        if isinstance(self._db_interface, sql.ODBCDatabase):
            vlayout.addWidget(self._parameters['odbc'].gui())
        # Create ButtonGroup
        self._sqlite_query_alternatives = QtWidgets.QButtonGroup()
        self._sqlite_query_alternatives.setExclusive(True)

        self._table_query_button = QtWidgets.QRadioButton('Table query')
        self._table_query_button.setChecked(True)
        self._lineedit_query_button = QtWidgets.QRadioButton('Write query')
        self._custom_query_button = QtWidgets.QRadioButton('Make custom query')
        # Add buttons to group
        self._sqlite_query_alternatives.addButton(self._table_query_button)
        self._sqlite_query_alternatives.addButton(self._lineedit_query_button)
        self._sqlite_query_alternatives.addButton(self._custom_query_button)
        # Add group to layout
        vlayout.addWidget(self._table_query_button)

        self._row_label = QtWidgets.QLabel("Choose database table.")
        self._row_combo = QtWidgets.QComboBox()
        hlayout_simple_table.addWidget(self._row_label)
        hlayout_simple_table.addWidget(self._row_combo)
        vlayout.addLayout(hlayout_simple_table)
        vlayout.addWidget(self._lineedit_query_button)
        self._query_label = QtWidgets.QLabel("SQLite query:")
        self._query_edit = QtWidgets.QLineEdit(self)
        hlayout_query_edit.addWidget(self._query_label)
        hlayout_query_edit.addWidget(self._query_edit)
        vlayout.addLayout(hlayout_query_edit)
        vlayout.addWidget(self._custom_query_button)
        self._join_tables = QtWidgets.QListWidget()
        self._join_tables.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)
        self._join_tables.setMaximumHeight(max_height)
        self._join_tables.addItems(self._db_interface.table_names())
        self._table_columns = QtWidgets.QListWidget()
        self._table_columns.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)
        self._table_columns.setMaximumHeight(max_height)
        self._label_join_tables = QtWidgets.QLabel("Select tables")
        vlayout_join_tables = QtWidgets.QVBoxLayout()
        vlayout_join_tables.addWidget(self._label_join_tables)
        vlayout_join_tables.addWidget(self._join_tables)
        hlayout_join_info.addLayout(vlayout_join_tables)
        self._label_table_columns = QtWidgets.QLabel(
            "Select resulting table columns")
        vlayout_table_columns = QtWidgets.QVBoxLayout()
        vlayout_table_columns.addWidget(self._label_table_columns)
        vlayout_table_columns.addWidget(self._table_columns)
        hlayout_join_info.addLayout(vlayout_table_columns)

        self._join_column_selection = QtWidgets.QListWidget()
        self._join_column_selection.setDragEnabled(True)
        self._join_column_selection.setMaximumHeight(max_height)
        self._label_join_column_selection = QtWidgets.QLabel(
            "Double click on names to add to join")
        # vlayout_join_column_selection = QtWidgets.QVBoxLayout()
        # vlayout_join_column_selection.addWidget(
        #     self._label_join_column_selection)
        # vlayout_join_column_selection.addWidget(self._join_column_selection)
        # hlayout_join_info.addLayout(vlayout_join_column_selection)

        hlayout_where_preview = QtWidgets.QHBoxLayout()
        self._join_columns = QtWidgets.QListWidget()
        # Added for double click method
        self._join_columns.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)
        self._join_columns.setAcceptDrops(True)
        self._join_columns.setDropIndicatorShown(True)
        self._join_columns.setMaximumHeight(max_height)
        self._label_join_columns = QtWidgets.QLabel(
            "Join on two consecutive column names. Double click to remove."
            "Change order by drag and drop.")
        self._label_join_columns.setWordWrap(True)
        # vlayout_join_columns = QtWidgets.QVBoxLayout()
        # vlayout_join_columns.addWidget(
        #     self._label_join_columns)
        # vlayout_join_columns.addWidget(self._join_columns)
        # hlayout_join_info.addLayout(vlayout_join_columns)

        # For adding where statements
        hlayout_where_combo = QtWidgets.QHBoxLayout()
        self._where_column_combo = QtWidgets.QComboBox()
        hlayout_where_combo.addWidget(self._where_column_combo)
        self._where_comparison = QtWidgets.QComboBox()
        hlayout_where.addWidget(self._where_comparison)
        self._where_condition = QtWidgets.QLineEdit()
        hlayout_where.addWidget(self._where_condition)
        self._where_add_button = QtWidgets.QPushButton('Add', self)
        hlayout_where.addWidget(self._where_add_button)
        self._where_condition_list = QtWidgets.QListWidget()
        self._where_condition_list.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)
        self._where_condition_list.setAcceptDrops(True)
        self._where_condition_list.setDropIndicatorShown(True)
        self._where_condition_list.setMaximumHeight(max_height)
        self._label_where_condition = QtWidgets.QLabel(
            "Add WHERE statements")
        self._label_where_condition.setWordWrap(True)
        vlayout_where_condition = QtWidgets.QVBoxLayout()
        vlayout_where_condition.addWidget(
            self._label_where_condition)
        vlayout_where_condition.addLayout(hlayout_where_combo)
        vlayout_where_condition.addLayout(hlayout_where)
        vlayout_where_condition.addWidget(self._where_condition_list)
        hlayout_where_preview.addLayout(vlayout_where_condition)

        # Preview buttons, tables and label created.
        self._preview_query_button = QtWidgets.QPushButton('Preview query')
        self._preview_query_button.setFixedWidth(150)
        self._preview_query = QtWidgets.QLabel('Query')
        self._preview_query.setWordWrap(True)
        hlayout_query_preview = QtWidgets.QHBoxLayout()
        hlayout_query_preview.addWidget(self._preview_query_button)
        hlayout_query_preview.addWidget(self._preview_query)

        self._preview_table_button = QtWidgets.QPushButton('Preview table')
        self._preview_table = QtWidgets.QTableWidget()
        self._preview_table.setMaximumHeight(max_height)
        vlayout_table_preview = QtWidgets.QVBoxLayout()
        vlayout_table_preview.addWidget(self._preview_table_button)
        vlayout_table_preview.addWidget(self._preview_table)

        hlayout_where_preview.addLayout(vlayout_table_preview)

        vlayout.addLayout(hlayout_join_info)
        vlayout.addLayout(hlayout_where_preview)
        vlayout.addLayout(hlayout_query_preview)
        self.setLayout(vlayout)

        self._row_combo.addItems(self._parameters["table_names"].list)
        if self._parameters["table_names"].list and self._parameters[
                "table_names"].value:
            self._row_combo.setCurrentIndex(
                self._parameters["table_names"].value[0])
        self._query_edit.setText(self._parameters["query_str"].value)

        self._table_query_button.setChecked(
            self._parameters["table_query"].value)
        self._table_query_enable(self._parameters["table_query"].value)
        self._lineedit_query_button.setChecked(
            self._parameters["lineedit_query"].value)
        self._lineedit_query_enable(self._parameters["lineedit_query"].value)
        self._custom_query_button.setChecked(
            self._parameters["custom_query"].value)
        self._custom_query_enable(self._parameters["custom_query"].value)

        for item in self._parameters["join_tables"].list:
            try:
                self._join_tables.findItems(
                    item, QtCore.Qt.MatchCaseSensitive)[0].setSelected(True)
            except IndexError:
                pass

        # Add column names and mark previous selected ones as selected
        self._names_changed()

        for item in self._parameters["table_columns"].list:
            try:
                self._table_columns.findItems(
                    item, QtCore.Qt.MatchCaseSensitive)[0].setSelected(
                        True)
            except IndexError:
                pass

        for item in self._parameters["join_column_selection"].list:
            try:
                self._join_column_selection.findItems(
                    item, QtCore.Qt.MatchCaseSensitive)[0].setSelected(True)
            except IndexError:
                pass

        # Init where combos
        self._where_column_combo.clear()
        self._where_column_combo.addItems(
            self._parameters["where_column_combo"].list)
        if self._parameters["where_column_combo"].list:
            self._where_column_combo.setCurrentIndex(
                self._parameters["where_column_combo"].value[0])
        self._where_comparison.addItems(
            self._parameters["where_comparison_combo"].list)
        if self._parameters["where_comparison_combo"].list:
            self._where_comparison.setCurrentIndex(
                self._parameters["where_comparison_combo"].value[0])
        self._where_condition.setText(
            self._parameters["where_condition"].value)
        self._where_condition_list.clear()
        self._where_condition_list.addItems(
            self._parameters["where_condition_list"].list)

        self._row_combo.currentIndexChanged[int].connect(self._row_changed)
        self._query_edit.textChanged[str].connect(self._query_changed)

        self._join_tables.itemClicked.connect(self._names_changed)
        self._table_columns.itemClicked.connect(self._columns_changed)
        self._join_tables.itemSelectionChanged.connect(self._names_changed)
        self._table_columns.itemSelectionChanged.connect(
            self._columns_changed)

        # For double click method
        self._join_column_selection.itemDoubleClicked.connect(
            self._add_double_click)
        self._join_columns.itemDoubleClicked.connect(self._remove_double_click)
        self._join_columns.itemClicked.connect(self._change_order)
        self._join_columns.currentRowChanged.connect(self._change_order)

        self._where_condition_list.itemDoubleClicked.connect(
            self._remove_where_condition)
        self._where_condition_list.currentRowChanged.connect(
            self._change_order_where)

        # For where combo boxes changed
        (self._where_column_combo.currentIndexChanged[int].
            connect(self._where_column_changed))
        (self._where_comparison.currentIndexChanged[int].
            connect(self._where_comparison_changed))
        (self._where_condition.textChanged[str].
            connect(self._where_condition_changed))
        # Button clicked, add where statement
        self._where_add_button.clicked.connect(self._add_where_clause)

        # Preview buttons clicked:
        self._preview_table_button.clicked.connect(self._add_preview_table)
        self._preview_query_button.clicked.connect(self._add_preview_query)

        # query selection radiobuttons clicked
        self._table_query_button.clicked.connect(
            self._table_query_button_clicked)

        self._lineedit_query_button.clicked.connect(
            self._lineedit_query_button_clicked)

        self._custom_query_button.clicked.connect(
            self._custom_query_button_clicked)

    def _init_parameters(self):

        try:
            self._parameters["table_query"]
        except KeyError:
            self._parameters.set_boolean("table_query", value=True)

        try:
            table_names = self._db_interface.table_names()
        except Exception:
            table_names = []

        try:
            self._parameters["table_names"]
        except KeyError:
            self._parameters.set_list(
                "table_names",
                table_names or ['test'], value=[0])
        else:
            table_name = self._parameters["table_names"].selected
            if table_name not in table_names:
                table_names = ([table_name] + table_names)
            self._parameters['table_names'].list = table_names
            self._parameters['table_names'].selected = table_name

        try:
            self._parameters["query_str"]
        except KeyError:
            self._parameters.set_string("query_str")
        try:
            self._parameters["lineedit_query"]
        except KeyError:
            self._parameters.set_boolean("lineedit_query", value=False)
        try:
            self._parameters["custom_query"]
        except KeyError:
            self._parameters.set_boolean("custom_query", value=False)
        try:
            self._parameters["join_tables"]
        except KeyError:
            self._parameters.set_list("join_tables")
        try:
            self._parameters["table_columns"]
        except KeyError:
            self._parameters.set_list("table_columns")
        try:
            self._parameters["join_column_selection"]
        except KeyError:
            self._parameters.set_list("join_column_selection")
        try:
            self._parameters["join_columns"]
        except KeyError:
            self._parameters.set_list("join_columns")
        try:
            self._parameters["where_add_comparison"]
        except KeyError:
            self._parameters.set_string("where_add_comparison")
        try:
            self._parameters["where_column_combo"]
        except KeyError:
            self._parameters.set_list("where_column_combo",
                                      self._parameters['join_column_selection']
                                      .list)
        try:
            self._parameters["where_comparison_combo"]
        except KeyError:
            self._parameters.set_list("where_comparison_combo",
                                      ['=', '<', '>', '>=', '<=', '!=',
                                       ' LIKE ', ' GLOB ', ' BETWEEN '])
        try:
            self._parameters["where_condition"]
        except KeyError:
            self._parameters.set_string("where_condition")
        try:
            self._parameters["where_condition_list"]
        except KeyError:
            self._parameters.set_list("where_condition_list")
        try:
            self._parameters["preview_query"]
        except KeyError:
            self._parameters.set_string("preview_query")

        try:
            self._parameters['odbc']
        except KeyError:
            self._parameters.set_list(
                'odbc', ['default', 'pyodbc', 'ceODBC'],
                label='ODBC method', order=0,
                description='ODBC method to use.', value=[0],
                editor=synode.Util.combo_editor())

    def _row_changed(self, index):
        self._parameters["table_names"].value = [index]

    def _table_query_button_clicked(self):
        self._parameters["table_query"].value = True
        self._parameters["lineedit_query"].value = False
        self._parameters["custom_query"].value = False
        self._table_query_enable(True)
        self._lineedit_query_enable(False)
        self._custom_query_enable(False)

    def _lineedit_query_button_clicked(self):
        self._parameters["table_query"].value = False
        self._parameters["lineedit_query"].value = True
        self._parameters["custom_query"].value = False
        self._table_query_enable(False)
        self._lineedit_query_enable(True)
        self._custom_query_enable(False)

    def _custom_query_button_clicked(self):
        self._parameters["table_query"].value = False
        self._parameters["lineedit_query"].value = False
        self._parameters["custom_query"].value = True
        self._table_query_enable(False)
        self._lineedit_query_enable(False)
        self._custom_query_enable(True)

    def _table_query_enable(self, state):
        self._row_combo.setEnabled(state)
        self._row_label.setEnabled(state)

    def _lineedit_query_enable(self, state):
        self._query_edit.setEnabled(state)
        self._query_label.setEnabled(state)

    def _custom_query_enable(self, state):
        self._join_tables.setEnabled(state)
        self._label_join_tables.setEnabled(state)
        self._table_columns.setEnabled(state)
        self._label_table_columns.setEnabled(state)
        self._join_column_selection.setEnabled(state)
        self._label_join_column_selection.setEnabled(state)
        self._join_columns.setEnabled(state)
        self._label_join_columns.setEnabled(state)
        self._label_where_condition.setEnabled(state)
        self._where_column_combo.setEnabled(state)
        self._where_comparison.setEnabled(state)
        self._where_condition.setEnabled(state)
        self._where_add_button.setEnabled(state)
        self._where_condition_list.setEnabled(state)
        self._preview_query.setEnabled(state)
        self._preview_query_button.setEnabled(state)
        self._preview_table.setEnabled(state)
        self._preview_table_button.setEnabled(state)

    def _query_changed(self, text):
        self._parameters["query_str"].value = str(text)

    def _names_changed(self):
        current_join_columns = self._parameters["join_columns"].list
        names = self._join_tables.selectedItems()
        self._parameters["join_tables"].list = [str(name.text())
                                                for name in names]
        columns = []
        columns_with_table = []
        names_text = []

        for name in names:
            name = name.text()
            names_text.append(name)
            [columns.append(column)
             for column in self._db_interface.table_column_names(name)
             if column not in columns]
            [columns_with_table.append(str(name + '.' + column))
             for column in self._db_interface.table_column_names(name)]
            columns.sort()
        columns_with_table.sort()
        current_selected_cols = self._parameters["table_columns"].list
        self._table_columns.clear()
        self._table_columns.addItems(columns_with_table)
        # Mark columns previously selected as selected if column name still in
        # column list.
        for item in current_selected_cols:
            if item in columns_with_table:
                self._table_columns.findItems(
                    item, QtCore.Qt.MatchCaseSensitive)[0].setSelected(True)

        self._join_column_selection.clear()
        self._join_column_selection.addItems(columns_with_table)
        self._parameters["join_column_selection"].list = columns_with_table

        self._join_columns.clear()
        reset_join_on = []
        [reset_join_on.append(str(item))
         for item in current_join_columns
            if item in columns_with_table]
        if len(reset_join_on) != 0:
            self._join_columns.addItems(reset_join_on)
        self._parameters["join_columns"].list = reset_join_on

        # Fix where_columns_combo values
        self._where_column_combo.clear()
        self._where_column_combo.addItems(columns_with_table)
        self._parameters["where_column_combo"].list = columns_with_table
        if self._parameters["where_column_combo"].list:
            self._parameters["where_column_combo"].value = [0]

        # Remove where statements including table names not longer selected
        # for query
        where_statements = self._parameters["where_condition_list"].list
        valid_where_statements = []
        regex = re.compile("^([a-zA-Z0-9_]*).")
        [valid_where_statements.append(where_statement)
            for where_statement in where_statements
            if regex.findall(where_statement)[0] in names_text]

        self._parameters["where_condition_list"].list = valid_where_statements
        self._where_condition_list.clear()
        self._where_condition_list.addItems(valid_where_statements)

    def _columns_changed(self):
        columns = self._table_columns.selectedItems()
        self._parameters["table_columns"].list = (
            [str(column.text()) for column in columns])

    def _add_double_click(self):
        """Add items to join_column list widget."""
        item = self._join_column_selection.currentItem().text()
        self._join_columns.addItem(item)
        items = [str(self._join_columns.item(index).text())
                 for index in range(self._join_columns.count())]
        self._parameters["join_columns"].list = items

    def _remove_double_click(self):
        """Remove items from join_column list widget."""
        item = self._join_columns.currentItem().text()
        items = [str(self._join_columns.item(index).text())
                 for index in range(self._join_columns.count())]
        items.remove(item)
        self._join_columns.clear()
        self._join_columns.addItems(items)
        self._parameters["join_columns"].list = items

    def _change_order(self):
        """Change order on join_columns."""
        self._parameters["join_columns"].list = (
            [str(self._join_columns.item(index).text())
             for index in range(self._join_columns.count())])

    def _change_order_where(self):
        """Change order on where_statements."""
        self._parameters["where_condition_list"].list = (
            [str(self._where_condition_list.item(index).text())
             for index in range(self._where_condition_list.count())])

    def _where_column_changed(self, index):
        if index != -1:
            self._parameters["where_column_combo"].value = []
        else:
            self._parameters["where_column_combo"].value = [index]

    def _where_comparison_changed(self, index):
        self._parameters["where_comparison_combo"].value = [index]

    def _where_condition_changed(self, text):
        self._parameters["where_condition"].value = str(text)

    def _add_where_clause(self):
        where_clause = ''
        condition = self._parameters["where_condition"].value
        if (condition != '' and
                self._parameters["where_column_combo"].selected and
                self._parameters["where_comparison_combo"].selected):
            where_clause += self._parameters["where_column_combo"].selected
            where_clause += self._parameters["where_comparison_combo"].selected
            where_clause += condition
            self._where_condition_list.addItem(where_clause)
            items = [str(
                self._where_condition_list.item(index).text()) for index in
                     range(self._where_condition_list.count())]
            self._parameters["where_condition_list"].list = items

    def _remove_where_condition(self):
        item = self._where_condition_list.currentItem().text()
        items = [str(
            self._where_condition_list.item(index).text()) for index in
                 range(self._where_condition_list.count())]
        items.remove(item)
        self._where_condition_list.clear()
        self._where_condition_list.addItems(items)
        self._parameters["where_condition_list"].list = items

    def _add_preview_table(self):
        """Preview table when button clicked."""
        try:
            query = sql.build_where_query(
                self._parameters["join_tables"].list,
                self._parameters["table_columns"].list,
                self._parameters["join_columns"].list,
                self._parameters["where_condition_list"].list)

            with self._db_interface.to_rows_query(query) as (
                    tablenames, tabledata):
                tablenames = list(tablenames)
                tabledata = list(tabledata)
                self._preview_table.clear()
                nbr_rows = len(tabledata)
                nbr_cols = len(tablenames)
                self._preview_table.setRowCount(nbr_rows)
                self._preview_table.setColumnCount(nbr_cols)
                self._preview_table.setHorizontalHeaderLabels(tablenames)

                for row_ind, row in enumerate(tabledata):
                    for col_ind, item in enumerate(list(row)):
                        self._preview_table.setItem(
                            row_ind, col_ind,
                            QtWidgets.QTableWidgetItem(str(item)))
        except Exception:
            nbr_rows = 1
            self._preview_table.clear()
            self._preview_table.setRowCount(1)
            self._preview_table.setColumnCount(1)
            self._preview_table.setItem(
                0, 0, QtWidgets.QTableWidgetItem('Not a valid query'))
            self._preview_table.setHorizontalHeaderLabels(['Error'])

        self._preview_table.setVerticalHeaderLabels(
            [str(i) for i in range(nbr_rows)])

    def _add_preview_query(self):
        """Preview query."""
        query = sql.build_where_query(
            self._parameters["join_tables"].list,
            self._parameters["table_columns"].list,
            self._parameters["join_columns"].list,
            self._parameters["where_condition_list"].list)

        self._preview_query.setText(str(query))
        self._parameters["preview_query"].value = str(query)


class DataImportSQL(importers.TableDataImporterBase):
    """Importer for SQL databases."""
    IMPORTER_NAME = "SQL"
    PARAMETER_VIEW = DataImportSQLWidget
    DATASOURCES = [importers.DATASOURCE.FILE,
                   importers.DATASOURCE.DATABASE]

    def __init__(self, fq_infilename, parameters):
        super(DataImportSQL, self).__init__(fq_infilename, parameters)

    def _datasource(self):
        return (
            importers.DATASOURCE.FILE
            if self.valid_for_file()
            else importers.DATASOURCE.DATABASE)

    def _db_interface(self, capture_exc=True):
        dburl = self._fq_infilename

        if self.valid_for_file():
            return sql.get_interface('FILE', dburl)

        try:
            odbc_name = self._parameters['odbc'].selected
        except KeyError:
            odbc_name = 'odbc'

        return sql.get_interface_guess_database(
            dburl,  odbc_name, capture_exc=capture_exc)

    def name(self):
        return self.IMPORTER_NAME

    def valid_for_file(self):
        """Return True if input file is a valid SQL file."""
        if self._fq_infilename is None or not os.path.isfile(
                self._fq_infilename):
            return False

        # Check if file Sqlite3
        return len(get_filedbs(self._fq_infilename)) > 0

    def parameter_view(self, parameters):
        db_interface = self._db_interface()

        return DataImportSQLWidget(parameters, db_interface)

    def import_data(self, out_datafile,
                    parameters=None, progress=None):
        """Import SQLite data from a file"""
        self._parameters = parameters
        # For auto to work. Need to know table name if not table name selected
        # yet.

        db_interface = self._db_interface(capture_exc=False)

        try:
            lineedit_query = self._parameters['lineedit_query'].value
        except KeyError:
            lineedit_query = False
        try:
            query_str = self._parameters['query_str'].value
        except KeyError:
            query_str = ''
        try:
            custom_query = self._parameters['custom_query'].value
        except KeyError:
            custom_query = False
        try:
            table_name = self._parameters['table_names'].selected
        except KeyError:
            table_name = None

        try:
            join_tables = self._parameters['join_tables'].list
        except Exception:
            join_tables = []

        tabledata = table.File()

        if lineedit_query:
            with db_interface.to_rows_query(query_str) as (names, rows):
                tabledata = table.File.from_rows(names, rows)
        elif custom_query:
            table_columns = self._parameters['table_columns'].list
            join_columns = self._parameters['join_columns'].list
            where_conditions = (
                self._parameters['where_condition_list'].list)
            query = sql.build_where_query(
                join_tables, table_columns, join_columns, where_conditions)
            with db_interface.to_rows_query(query) as (names, rows):
                tabledata = table.File.from_rows(names, rows)
        else:
            # TODO(Erik): Make this less questionable.
            table_names = db_interface.table_names()
            if table_names and table_name not in table_names:
                table_name = table_names[0]

            with db_interface.to_rows_table(table_name) as (names, rows):
                tabledata = table.File.from_rows(names, rows)
        out_datafile.update(tabledata)
