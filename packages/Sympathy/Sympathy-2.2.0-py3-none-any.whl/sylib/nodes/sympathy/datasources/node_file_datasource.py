# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2017, Combine Control Systems AB
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
In Sympathy for Data, the action of pointing out where data is located and
actual import of data are separated into two different categories of
nodes. The internal data type Datasource is used to carry the information
about the location of the data to the import nodes.

There exist two nodes for establishing paths to locations with data, either you
are interested in a single source of data, :ref:`Datasource`, or several
sources, :ref:`org.sysess.sympathy.datasources.filedatasourcemultiple`. The
single source can either be a data file or a location in a data base. While for
multiple sources only several data files are handled.

"""
import os
from collections import OrderedDict
import fnmatch

from sympathy.api import node as synode
from sympathy.api import datasource as dsrc
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api import qt2 as qt_compat
QtCore = qt_compat.QtCore
QtWidgets = qt_compat.import_module('QtWidgets')

MAX_DISPLAYED_FILES = 500
TIME_EXCEEDED_MSG = (
    f'Preview looked in {MAX_DISPLAYED_FILES} directories '
    '(and then stopped searching to avoid excessive wait).\n'
    '\nPlease execute the node to get all results.')


class SuperNode(object):
    author = "Alexander Busck"
    version = '1.1'
    icon = 'datasource.svg'
    tags = Tags(Tag.Input.Import)


class FileDatasourceWidget(QtWidgets.QWidget):
    def __init__(self, ctx, parameters, parent=None):
        super(FileDatasourceWidget, self).__init__(parent)
        self._parameters = parameters

        self._init_gui()
        self._init_gui_from_parameters()

    def _init_gui(self):
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        file_widget = QtWidgets.QWidget()
        file_vlayout = QtWidgets.QVBoxLayout()
        file_widget.setLayout(file_vlayout)

        db_widget = QtWidgets.QWidget()
        db_vlayout = QtWidgets.QVBoxLayout()
        odbc_vlayout = QtWidgets.QVBoxLayout()
        sqlalchemy_vlayout = QtWidgets.QVBoxLayout()
        db_widget.setLayout(db_vlayout)

        url_widget = QtWidgets.QWidget()
        url_vlayout = QtWidgets.QVBoxLayout()
        url_widget.setLayout(url_vlayout)

        self._filename_widget = self._parameters['filename'].gui()

        self._db_driver = self._parameters['db_driver']
        self._db_servername = self._parameters['db_servername']
        self._db_databasename = self._parameters['db_databasename']
        self._db_user = self._parameters['db_user']
        self._db_password = self._parameters['db_password']

        self._db_driver_widget = self._db_driver.gui()
        self._db_servername_widget = self._db_servername.gui()
        self._db_databasename_widget = self._db_databasename.gui()
        self._db_user_widget = self._db_user.gui()
        self._db_password_widget = self._db_password.gui()

        self._connection_widget = (
            self._parameters['db_connection_string'].gui())
        self._db_sqlalchemy_engine_url = (
            self._parameters['db_sqlalchemy_engine_url'].gui())
        self._db_method = (
            self._parameters['db_method'].gui())

        self._type_selector = QtWidgets.QComboBox()
        self._url_str_widget = self._parameters['url_str'].gui()
        self._url_env_widget = self._parameters['url_env'].gui()

        self._type_selector.addItem('File')
        self._type_selector.addItem('Database')
        self._type_selector.addItem('Url')
        self._type_selector.setCurrentIndex(
            self._parameters['datasource_type'].value[0])
        self._datasource_stackwidget = QtWidgets.QStackedWidget()

        file_vlayout.addWidget(self._filename_widget)
        url_vlayout.addWidget(self._url_str_widget)
        url_vlayout.addWidget(self._url_env_widget)

        self._odbc_split_widgets = [
            self._db_driver_widget,
            self._db_servername_widget,
            self._db_databasename_widget,
            self._db_user_widget,
            self._db_password_widget]

        self._connection_widget_active = False

        file_vlayout.addStretch()
        url_vlayout.addStretch()

        self._sqlalchemy_group = QtWidgets.QGroupBox('SQLAlchemy settings')
        self._sqlalchemy_group.setLayout(sqlalchemy_vlayout)
        self._odbc_group = QtWidgets.QGroupBox('ODBC settings')
        self._odbc_group.setLayout(odbc_vlayout)

        self._db_methods = OrderedDict(
            zip(_db_options, [self._odbc_group, self._sqlalchemy_group]))

        for odbc_split_widget in self._odbc_split_widgets:
            odbc_vlayout.addWidget(odbc_split_widget)

        for odbc_split in [self._db_driver,
                           self._db_servername,
                           self._db_databasename,
                           self._db_user,
                           self._db_password]:
            odbc_split.value_changed.add_handler(self._odbc_split_changed)

        odbc_vlayout.addWidget(self._connection_widget)
        sqlalchemy_vlayout.addWidget(self._db_sqlalchemy_engine_url)

        db_vlayout.addWidget(self._db_method)
        db_vlayout.addWidget(self._sqlalchemy_group)
        db_vlayout.addWidget(self._odbc_group)

        self._datasource_stackwidget.addWidget(file_widget)
        self._datasource_stackwidget.addWidget(db_widget)
        self._datasource_stackwidget.addWidget(url_widget)

        vlayout.addWidget(self._type_selector)
        vlayout.addWidget(self._datasource_stackwidget)

        self.setLayout(vlayout)

        self._type_selector.currentIndexChanged[int].connect(
            self._type_changed)

        self._db_method_changed(self._parameters['db_method'].value)
        self._db_method.valueChanged.connect(
            self._db_method_changed)

    def _init_gui_from_parameters(self):
        try:
            index = self._parameters['datasource_type'].value[0]
        except KeyError:
            index = 0
        self._datasource_stackwidget.setCurrentIndex(index)

    def _type_changed(self, index):
        self._parameters['datasource_type'].value = [index]
        self._datasource_stackwidget.setCurrentIndex(index)

    def _odbc_split_changed(self):
        args = [
            self._db_driver.selected,
            self._db_servername.value,
            self._db_databasename.value,
            self._db_user.value,
            self._db_password.value]

        tabledata = dsrc.File.to_database_dict(*args, db_method='ODBC')
        self._connection_widget.set_value(tabledata['path'])

    def _db_method_changed(self, value):
        for key, db_method in self._db_methods.items():
            db_method.setEnabled(key == value)


def datasource_factory(datasource, parameters):
    try:
        datasource_type = parameters['datasource_type'].selected
    except KeyError:
        datasource_type = 'File'

    if datasource_type == 'File':
        tabledata = datasource.to_file_dict(
            os.path.abspath(parameters['filename'].value))
    elif datasource_type == 'Database':
        db_method = parameters['db_method'].value
        if db_method == 'ODBC':
            args = [
                parameters['db_driver'].selected,
                parameters['db_servername'].value,
                parameters['db_databasename'].value,
                parameters['db_user'].value,
                parameters['db_password'].value,
                parameters['db_connection_string'].value]
        elif db_method == 'SQLAlchemy':
            args = [
                parameters['db_sqlalchemy_engine_url'].value]

        tabledata = datasource.to_database_dict(*args, db_method=db_method)

    elif datasource_type == 'Url':
        url_env = parameters['url_env'].value
        url_env = OrderedDict(url_env or [])
        tabledata = datasource.to_url_dict(
            url=parameters['url_str'].value,
            env=url_env)
    else:
        assert(False)

    return tabledata


_db_options = ['ODBC', 'SQLAlchemy']
_type_options = ['File', 'Database', 'Url']


class FileDatasource(SuperNode, synode.Node):
    """
    Specify Datasource.

    The primary usecase for this node is to specify a resource for use with
    an import or export node. But in principle, any node may use datasource
    input in the same way.

    .. _datasource_node_file:

    File
    ----

    Choose from existing filenames on disk or edit the filename directly to
    point to non-existing files. For example, to point to output files that
    have not yet been created.

    The filename has at most different: absolute path, relative to top-flow,
    relative to sub-flow and relative to library root.

    All filenames are made absolute and normalized before they are written to
    the output and even the options which allow you to specify relative
    filenames will result in absolute output filenames.

    Absolute path
    =============

    Absolute path is the most basic selection. Input the absolute filename
    and that filename will be used as output.

    Relative to top-flow
    ====================

    Relative to top-flow is one of the relative ways to reference files and is
    used to express filenames relative to the file of the top-flow (the .syx
    file opened from disk).

    Relative to sub-flow
    ====================

    Relative to sub-flow is one of the relative ways to reference files and is
    used to express filenames relative to the file of the sub-flow. The
    sub-flow location can be different from that of the top-flow when the
    Datasource node is part of a linked sub-flow.

    Relative to library root
    ========================

    Relative to library is one of the relative ways to reference files and is
    used to express filenames relative to the library location of the current
    sub-flow node. This option is only available for sub-flow nodes added to a
    library and offers a way to express paths to other resources within the
    same library.


    Database
    --------

    Specify properties for SQLAlchemy or ODBC database connections.

    See `Engine <https://docs.sqlalchemy.org/en/13/core/engines.html>`_ for
    details about how to specify SQLAlchemy engine URL for different databases.

    See `Connection String Syntax <https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms722656(v%3Dvs.85)>`_ for
    information about how to specify ODBC connection strings.

    URL
    ---

    Specify an URL, for example, in HTTP(s) scheme.  URL environment might be
    handled differently depending on the scheme and corresponds to HTTP headers
    for the HTTP(s) case.

    """

    name = 'Datasource'
    nodeid = 'org.sysess.sympathy.datasources.filedatasource'
    related = ['org.sysess.sympathy.datasources.filedatasourcemultiple']

    outputs = Ports([Port.Datasource(
        'Datasource with path to file', name='port1', scheme='text')])

    parameters = synode.parameters()
    parameters.set_string(
        'filename', label='Filename',
        description='A filename including path if needed',
        editor=synode.Util.filename_editor(['Any files (*)']))
    parameters.set_string(
        'db_sqlalchemy_engine_url', label='SQLAlchemy engine URL',
        value='mssql+pyodbc:///',
        description='SQLAlchemy engine URL for connecting to the database')
    parameters.set_string(
        'db_method',
        label='Database connection method',
        editor=synode.Util.combo_editor(options=_db_options),
        value=_db_options[0],
        description=(
            'Select which Database connection method that you want to use.'))
    parameters.set_list(
        'db_driver', ['SQL Server'], label='Database driver',
        description='Database driver to use.',
        editor=synode.Util.combo_editor())
    parameters.set_string(
        'db_servername', label='Server name',
        description='A valid name to a database server.')
    parameters.set_string(
        'db_databasename', label='Database name',
        description='The name of the database.')
    parameters.set_string(
        'db_user', label='User',
        description='A valid database user.')
    parameters.set_string(
        'db_password', label='Password',
        description='A valid password for the selected user.')
    parameters.set_string(
        'db_connection_string', label='Connection string',
        description='A connection string that will override other settings.')

    parameters.set_string(
        'url_str', label='URL string',
        description='Uniform Resource Locator (URL) string',
        value='')

    parameters.set_json(
        'url_env', label='Url environment',
        description='Environment for URL. '
        'Used as headers in case of HTTP URL. '
        'Input as a Python expression that evaluates to.',
        value=[],
        editor=synode.editors.table_editor(
            headers=['Name', 'Value'],
            types=['text', 'text'],
            unique=['Name']))

    parameters.set_list(
        'datasource_type', _type_options,
        label='Datasource type',
        description='Type of datasource.')

    INTERACTIVE_NODE_ARGUMENTS = {
        'uri': ['filename', 'value']
    }

    def update_parameters(self, old_parameters):
        datasource_type = old_parameters['datasource_type']

        if 'Url' not in datasource_type.list:
            datasource_type.list = _type_options

    def exec_parameter_view(self, ctx):
        return FileDatasourceWidget(
            ctx, ctx.parameters)

    def execute(self, ctx):
        """Execute"""
        ctx.output['port1'].encode(
            datasource_factory(ctx.output['port1'],
                               ctx.parameters))


def find_filenames(directory, pattern, fully_qualified=True,
                   recursive=False, include_files=True,
                   include_dirs=True, max_length=None):

    if not directory.strip():
        directory = os.path.abspath('.')

    def inner():
        length = 0
        for i, (root, dirnames, filenames) in enumerate(
                os.walk(directory)):
            if max_length and (i > max_length or length > max_length):
                # Signal that we gave up.
                yield None
                break
            inputs = []
            outputs = []

            if include_dirs:
                inputs.extend(dirnames)

            if include_files:
                inputs.extend(filenames)

            for filename in fnmatch.filter(inputs, pattern):
                if fully_qualified:
                    outputs.append(os.path.normpath(
                        os.path.join(root, filename)))
                else:
                    outputs.append(os.path.normpath(filename))
            length += len(outputs)
            yield outputs

    matches = []
    gave_up = False
    results = inner()

    if not recursive:
        try:
            matches.extend(next(results))
        except StopIteration:
            pass
    else:
        for outputs in results:
            if outputs is not None:
                matches.extend(outputs)
            else:
                gave_up = True
    if max_length:
        matches = matches[:max_length]
    return gave_up, matches


class FileDatasourcesWidget(QtWidgets.QWidget):
    def __init__(self, ctx, parameter_root, parent=None):
        super(FileDatasourcesWidget, self).__init__(parent)
        self._parameter_root = parameter_root

        self._init_gui()

    def _init_gui(self):
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        use_recursive_widget = self._parameter_root['recursive'].gui()
        self._directory_widget = self._parameter_root['directory'].gui()
        search_pattern_widget = self._parameter_root['search_pattern'].gui()
        include_types_widget = self._parameter_root['include_types'].gui()
        self._file_widget = QtWidgets.QListWidget()
        self._file_widget.setAlternatingRowColors(True)
        self._file_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        _file_widget_label = QtWidgets.QLabel(
            f'Preview ({MAX_DISPLAYED_FILES} first hits displayed)')

        vlayout.addWidget(use_recursive_widget)
        vlayout.addWidget(self._directory_widget)
        vlayout.addWidget(search_pattern_widget)
        vlayout.addWidget(include_types_widget)
        vlayout.addWidget(_file_widget_label)
        vlayout.addWidget(self._file_widget)
        self.setLayout(vlayout)

        self._update_filewidget()

        use_recursive_widget.stateChanged.connect(
            self._update_filewidget)
        self._directory_widget.editor().dialogChanged[str].connect(
            self._update_filewidget)
        self._directory_widget.editor().text_changed.connect(
            self._update_filewidget)
        search_pattern_widget.valueChanged.connect(
            self._update_filewidget)
        include_types_widget.editor().currentIndexChanged.connect(
            self._update_filewidget)

    def _update_filewidget(self, *args):
        gave_up, selected_fq_filenames = find_filenames(
            self._directory_widget.editor().filename(),
            self._parameter_root['search_pattern'].value,
            fully_qualified=True,
            max_length=MAX_DISPLAYED_FILES,
            recursive=self._parameter_root['recursive'].value,
            **_included_types(self._parameter_root['include_types'].value))

        preview_list = selected_fq_filenames
        if gave_up:
            preview_list = preview_list + [TIME_EXCEEDED_MSG]
        self._file_widget.clear()
        self._file_widget.addItems(preview_list)


_type_choice_files, _type_choice_dirs, _type_choice_both = _type_choices = [
    'Files', 'Directories', 'Files and Directories']


def _add_include_types_param(parameters):
    parameters.set_string(
        'include_types', label='Include',
        description='Choose whether matching files, directories or both '
        'should be included in the result',
        editor=synode.editors.combo_editor(options=_type_choices),
        value=_type_choice_files)


def _included_types(value):
    include_files = False
    include_dirs = False
    if value == _type_choice_files:
        include_files = True
    elif value == _type_choice_dirs:
        include_dirs = True
    else:
        include_files = True
        include_dirs = True
    return {'include_files': include_files,
            'include_dirs': include_dirs}


class FileDatasourceMultiple(SuperNode, synode.Node):
    """
    Create Datasources with paths to data sources.
    """

    name = 'File Datasources'
    description = 'Select data sources.'
    nodeid = 'org.sysess.sympathy.datasources.filedatasourcemultiple'
    related = ['org.sysess.sympathy.datasources.filedatasource']

    outputs = Ports([Port.Datasources(
        'Datasources with paths files',
        name='port1', scheme='text')])

    parameters = synode.parameters()
    parameters.set_boolean(
        'recursive', value=False, label='Recursive',
        description=('If unchecked, only the selected directory will be '
                     'searched. If checked, all subdirectories of the '
                     'selected directory will also be searched.'))
    parameters.set_string(
        'directory', label='Directory',
        description=('Directory where to search for files.'),
        editor=synode.Util.directory_editor())
    parameters.set_string(
        'search_pattern', value='*', label='Search pattern',
        description='A wildcard pattern which the filenames must match.')

    _add_include_types_param(parameters)

    def update_parameters(self, parameters):
        if ('include_types' not in parameters and
                not parameters['recursive'].value):
            _add_include_types_param(parameters)
            parameters['include_types'].value = _type_choice_both

    def exec_parameter_view(self, ctx):
        return FileDatasourcesWidget(ctx, ctx.parameters)

    def execute(self, ctx):
        """Create a list of datasources and add them to the output
        file.
        """
        selected_fq_filenames = find_filenames(
            ctx.parameters['directory'].value,
            ctx.parameters['search_pattern'].value,
            fully_qualified=True,
            recursive=ctx.parameters['recursive'].value,
            **_included_types(
                ctx.parameters['include_types'].value))[1]

        for fq_filename in selected_fq_filenames:
            datasource = dsrc.File()
            datasource.encode_path(os.path.abspath(fq_filename))
            ctx.output['port1'].append(datasource)
