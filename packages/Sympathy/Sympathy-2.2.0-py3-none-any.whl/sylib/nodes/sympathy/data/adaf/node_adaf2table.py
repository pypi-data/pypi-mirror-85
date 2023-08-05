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
In the standard library there exist three nodes which exports data from
:ref:`ADAF` to :ref:`Table`. Together with nodes for export in the
reversed direction, :ref:`Table to ADAF`, one can make transitions back and
forth between the two internal data types.

For all nodes one has to specify which container in the incoming
ADAF/ADAFs that is going to be exported. Selectable containers are metadata,
results and timeseries, see :ref:`ADAF` for further information.

For one of the nodes, :ref:`ADAF to Tables` the full content of the specified
container in the ADAF is exported.
For the other ones, when exporting timebased data one has to select the
specific rasters that are going to be exported.

The exported timebases will, in the Tables, be given the name of their
corrspondning rasters. It is important to know that if the name of the
timebases already exists among the names of the timeseries signals,
the timebases will not be exported to the Table.
"""
import warnings

from sylib.widget_library import FilterListView
from sympathy.api import qt2 as qt_compat
from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags
from sympathy.api.exceptions import SyDataError
from sympathy.api.exceptions import SyConfigurationError
QtGui = qt_compat.import_module('QtGui')
QtWidgets = qt_compat.import_module('QtWidgets')


def write_adaf_to_table(export_group, adaffile, tablefile, tb_name=None,
                        tb_col_name=''):
    """Write the selected export group to a table."""
    if export_group == 'Meta':
        tablefile.update(adaffile.meta.to_table())
    elif export_group == 'Result':
        tablefile.update(adaffile.res.to_table())
    elif export_group == 'Time series':
        system_name, raster_name = get_system_raster_names(tb_name)
        if system_name in adaffile.sys:
            system = adaffile.sys[system_name]
            if raster_name in system:
                raster = system[raster_name]
            else:
                raise SyDataError(
                    'The selected raster does not exist in incoming ADAF')
        else:
            raise SyDataError(
                'The selected system does not exist in incoming ADAF')

        if not tb_col_name:
            tb_col_name = raster_name
        # Check if tb_col_name already exists in Table
        if tb_col_name in raster.keys():
            message = ('A column with the entered time basis column name '
                       'do already exist. Time basis will not be included '
                       'in the outgoing Table.')
            warnings.warn(message)

        tablefile.update(raster.to_table(tb_col_name))

    source = adaffile.source_id()
    if source:
        tablefile.set_name(source)


def get_system_raster_names(tb_path):
    """Split time basis path, system_name/raster_name/ and the return the
    system_name and the raster_name.
    """
    return tuple(tb_path.split('/')[:2])


def get_raster_name(tb_path):
    """Return the raster name from given time basis path."""
    system_name, raster_name = get_system_raster_names(tb_path)
    return raster_name


def get_rasters_from_adaf(adafdata):
    """Return a list with the paths to all rasters in an adaf,
    system_name/raster_name/
    """
    if not adafdata:
        return []
    return ['{0}/{1}/'.format(system, raster)
            for system, rastergroup in adafdata.sys.items()
            for raster in rastergroup.keys()]


class ADAF2TableSuperNode(synode.Node):
    author = "Alexander Busck"
    version = '1.0'
    icon = 'adaf2table.svg'
    tags = Tags(Tag.DataProcessing.Convert)


def _get_single_tb_editor():
    return synode.Util.combo_editor('', filter=True, edit=False)


def base_parameters(multiselect):
    parameters = simple_base_parameters()

    if multiselect:
        tb_editor = synode.Util.multilist_editor(mode=False)
    else:
        tb_editor = _get_single_tb_editor()
    tb_editor.set_attribute('filter', True)
    parameters.set_list('tb',
                        label="Time basis raster",
                        description=(
                            'Specify the raster among the time resolved data '
                            'which will be exported'),
                        value=[],
                        editor=tb_editor)

    parameters.set_string('tb_col_name',
                          label='Time basis column name',
                          description=('Specify the name for the time basis '
                                       'column in the outgoing Table. The '
                                       'default name is the name of the '
                                       'selected raster.'),
                          value='')
    return parameters


def simple_base_parameters():
    parameters = synode.parameters()
    parameters.set_list(
        'export_group', ['Meta', 'Result', 'Time series'],
        label='Export group',
        description='Specify group in the ADAF which will be exported',
        value=[0],
        editor=synode.Util.combo_editor())
    return parameters


def get_params(node_context):
    group_name = node_context.parameters['export_group'].selected
    try:
        tb_names = node_context.parameters['tb'].value_names
    except Exception:
        tb_names = []
    try:
        tb_col_name = node_context.parameters['tb_col_name'].value
    except Exception:
        tb_col_name = ''
    return group_name, tb_names, tb_col_name


class ADAF2Table(ADAF2TableSuperNode):
    """
    Export of specified data in ADAF to Table. The data can either be
    the a raster from the timeseries container or the full content of either
    the metadata or the results containers.
    """

    name = 'ADAF to Table'
    description = 'Export of data from an ADAF to a Table.'
    nodeid = 'org.sysess.sympathy.data.adaf.adaf2table'
    related = ['org.sysess.sympathy.data.adaf.adafs2tables',
               'org.sysess.sympathy.data.adaf.adaf2tables',
               'org.sysess.sympathy.data.table.table2adaf']

    inputs = Ports([Port.ADAF('Input ADAF', name='port1')])
    outputs = Ports([Port.Table(
        'Table with the content of a specified group in the incoming ADAF',
        name='port1')])

    parameters = base_parameters(False)

    def adjust_parameters(self, node_context):
        if node_context.input['port1'].is_valid():
            adafdata = node_context.input['port1']
        else:
            adafdata = None
        rasters = get_rasters_from_adaf(adafdata)
        node_context.parameters['tb'].adjust(rasters)

    def update_parameters(self, old_params):
        param = 'tb'
        if param in old_params:
            old_params[param].editor = _get_single_tb_editor()

    def exec_parameter_view(self, node_context):
        if node_context.input['port1'].is_valid():
            adafdata = node_context.input['port1']
        else:
            adafdata = None
        return ADAF2TableWidget(node_context.parameters, adafdata)

    def execute(self, node_context):
        adaffile = node_context.input['port1']
        tablefile = node_context.output['port1']

        group_name, tb_names, tb_col_name = get_params(node_context)
        if group_name in ('Meta', 'Result'):
            write_adaf_to_table(group_name, adaffile, tablefile)
        for tb_name in tb_names:
            try:
                write_adaf_to_table(
                    group_name, adaffile, tablefile, tb_name, tb_col_name)
            except AttributeError:
                raise SyConfigurationError('Configuration error')


class ADAFs2Tables(ADAF2TableSuperNode):
    """
    Elementwise export of specified data from ADAFs to Tables.
    The data can either be the a raster from the timeseries
    container or the full content of either the metadata or the results
    containers.
    """

    name = 'ADAFs to Tables'
    description = ('Elementwise export of data from list of ADAFs to a '
                   'list of Tables.')
    nodeid = 'org.sysess.sympathy.data.adaf.adafs2tables'
    related = ['org.sysess.sympathy.data.adaf.adaf2table',
               'org.sysess.sympathy.data.adaf.adaf2tables',
               'org.sysess.sympathy.data.table.table2adaf']

    inputs = Ports([Port.ADAFs('Input ADAF', name='port1')])
    outputs = Ports([Port.Tables(
        'Tables with the content of a specified group in the incoming ADAFs',
        name='port1')])

    parameters = base_parameters(True)

    def adjust_parameters(self, node_context):
        port1 = node_context.input['port1']
        if port1.is_valid() and len(port1):
            adafdata = port1[0]
        else:
            adafdata = None
        rasters = get_rasters_from_adaf(adafdata)
        node_context.parameters['tb'].adjust(rasters)

    def update_parameters(self, old_params):
        try:
            old_params['tb'].editor['mode'] = True
        except KeyError:
            pass

    def exec_parameter_view(self, node_context):
        port1 = node_context.input['port1']
        if port1.is_valid() and len(port1):
            adafdata = port1[0]
        else:
            adafdata = None
        return ADAF2TableWidget(node_context.parameters, adafdata)

    def execute(self, node_context):
        input_list = node_context.input['port1']
        output_list = node_context.output['port1']

        group_name, tb_names, tb_col_name = get_params(node_context)
        for i, adaffile in enumerate(input_list):
            if group_name in ('Meta', 'Result'):
                tablefile = output_list.create()
                write_adaf_to_table(group_name, adaffile, tablefile)
                output_list.append(tablefile)
            else:
                tb_names = get_rasters_from_adaf(adaffile)
                for tb_name in node_context.parameters['tb'].selected_names(
                        tb_names):
                    tablefile = output_list.create()
                    try:
                        write_adaf_to_table(
                            group_name, adaffile, tablefile, tb_name,
                            tb_col_name)
                    except AttributeError:
                        raise SyConfigurationError('Configuration error')
                    output_list.append(tablefile)
            self.set_progress(100.0 * i / len(input_list))


class ADAF2Tables(ADAF2TableSuperNode):
    """
    Export of specified data from ADAF to Tables. The data can
    be the full content of either the metadata, the results or the timeseries
    containers.
    """

    name = 'ADAF to Tables'
    description = 'Export of data from an ADAF to a list of Tables.'
    nodeid = 'org.sysess.sympathy.data.adaf.adaf2tables'
    icon = 'adaf2tables.svg'
    related = ['org.sysess.sympathy.data.adaf.adaf2table',
               'org.sysess.sympathy.data.adaf.adafs2tables',
               'org.sysess.sympathy.data.table.table2adaf']

    inputs = Ports([Port.ADAF('Input ADAF', name='port1')])
    outputs = Ports([Port.Tables(
        'All data from an ADAF group as a Tables list', name='port1')])

    parameters = simple_base_parameters()

    def exec_parameter_view(self, node_context):
        return ADAF2TableWidgetSimple(node_context)

    def execute(self, node_context):
        group_name = node_context.parameters['export_group'].selected

        adaffile = node_context.input['port1']
        output_list = node_context.output['port1']
        if group_name == 'Time series':
            tb_names = get_rasters_from_adaf(adaffile)
        else:
            tb_names = [None]
        for tb_name in tb_names:
            tablefile = output_list.create()
            write_adaf_to_table(
                group_name, adaffile, tablefile, tb_name)
            output_list.append(tablefile)


class ADAF2TableWidget(QtWidgets.QWidget):

    def __init__(self, parameter_root, adafdata, parent=None):
        super(ADAF2TableWidget, self).__init__(parent)
        self._adafdata = adafdata
        self._parameter_root = parameter_root
        self._init_gui()

    def _init_gui(self):
        self._group_target = self._parameter_root['export_group'].gui()
        self._tb_selection = self._parameter_root['tb'].gui()

        self._ts_display = FilterListView(
            header='Timeseries in selected raster')

        self._tb_col_name_edit = self._parameter_root['tb_col_name'].gui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._group_target)

        layout.addWidget(self._tb_col_name_edit)
        layout.addWidget(self._tb_selection)
        layout.addWidget(self._ts_display)
        self.setLayout(layout)

        self._target_changed(self._parameter_root['export_group'].selected)
        self._update_signals()
        self._group_target.editor().currentIndexChanged[int].connect(
            self._target_changed)
        self._tb_selection.editor().valueChanged.connect(
            self._update_signals)

    def _update_signals(self):
        self._ts_display.clear()
        signals = []
        if self._adafdata:
            for raster_path in self._parameter_root['tb'].value_names:
                system_name, raster_name = get_system_raster_names(raster_path)
                if (system_name in self._adafdata.sys and
                        raster_name in self._adafdata.sys[system_name]):
                    signals.extend(
                        self._adafdata.sys[system_name][raster_name].keys())

        self._ts_display.add_items(signals)

    def _target_changed(self, index):
        if index in (0, 1, 'Meta', 'Result'):
            self._ts_display.setEnabled(False)
            self._tb_selection.setEnabled(False)
            self._tb_col_name_edit.setEnabled(False)
        else:
            self._ts_display.setEnabled(True)
            self._tb_selection.setEnabled(True)
            self._tb_col_name_edit.setEnabled(True)


class ADAF2TableWidgetSimple(QtWidgets.QWidget):

    def __init__(self, node_context, parent=None):
        super(ADAF2TableWidgetSimple, self).__init__(parent)
        self._node_context = node_context
        self._parameters = node_context.parameters
        self._init_gui()

    def _init_gui(self):
        self._group_target = self._parameters['export_group'].gui()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._group_target)
        self.setLayout(layout)
