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
In the standard libray there exist two nodes which exports the data from the
:ref:`Table` format to the :ref:`ADAF` format. Together with the existing
nodes in the reversed transiton, :ref:`ADAF to Table`, there exists a wide
spectrum of nodes which gives the possibility to, in different ways, change
between the two internal data types.

A container in the ADAF is specified in the configuration GUI as a target
for the export. If the timeseries container is choosen it is necessary
to specify the column in the Table which will be the time basis signal in
the ADAF. There do also exist an opportunity to specify both the name of the
system and raster containers, see :ref:`ADAF` for explanations of containers.
"""
from sympathy.api import qt2 as qt_compat
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, adjust
from sympathy.api.exceptions import SyDataError, SyConfigurationError
QtGui = qt_compat.import_module('QtGui')
QtWidgets = qt_compat.import_module('QtWidgets')


def write_table_timeseries_to_adaf(system_name, raster_name, tb_column,
                                   tabledata, adaffile):
    if system_name == '':
        raise SyConfigurationError('System name can not be left blank.')
    if raster_name == '':
        raise SyConfigurationError('Raster name can not be left blank.')
    if tb_column in tabledata:
        tb_group = adaffile.sys
        if system_name in tb_group:
            system = tb_group[system_name]
        else:
            system = tb_group.create(system_name)

        if raster_name in system:
            raster = system[raster_name]
        else:
            raster = system.create(raster_name)

        # Move the table into the raster and remove tb_column from raster
        raster.from_table(tabledata, tb_column)
    else:
        raise SyDataError('The selected time basis column does not exist in '
                          'the incoming Table')


def write_tabledata_to_adaf(export_to_meta, tablefile, adaffile):
    if export_to_meta:
        adaffile.meta.from_table(tablefile)
    else:
        adaffile.res.from_table(tablefile)


def check_table_columns_consistence_and_clear(
        table_name, columns_table, parameter_root):
    """Check whether table columns have changed since parameter
    view last was executed. If yes, clear lists.
    """
    selected_tb = parameter_root['tb'].selected
    parameter_root['tb'].list = columns_table

    if selected_tb is None:
        if table_name in parameter_root['tb'].list:
            parameter_root['tb'].selected = table_name

        parameter_root['raster'].value = parameter_root['tb'].selected


def _get_single_tb_editor():
    return synode.Util.combo_editor('', filter=True, edit=False)


class TableConvertWidget(QtWidgets.QWidget):
    def __init__(self, node_context, parent=None):
        super(TableConvertWidget, self).__init__(parent)
        self._parameters = node_context.parameters
        self._init_gui()

    def _init_gui(self):
        self._group_target = self._parameters['export_to_group'].gui()
        self._system_edit = self._parameters['system'].gui()
        self._raster_edit = self._parameters['raster'].gui()
        self._tb_selection = self._parameters['tb'].gui()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._group_target)
        layout.addWidget(self._system_edit)
        layout.addWidget(self._raster_edit)
        tb_group = QtWidgets.QGroupBox()
        tb_group_layout = QtWidgets.QVBoxLayout()
        tb_group_layout.addWidget(self._tb_selection)
        tb_group.setLayout(tb_group_layout)
        layout.addWidget(tb_group)
        self.setLayout(layout)
        self._target_changed(self._parameters['export_to_group'].value[0])
        self._group_target.editor().currentIndexChanged[int].connect(
            self._target_changed)
        self._tb_selection.editor().valueChanged.connect(
            self._tb_column_changed)

    def _target_changed(self, index):
        if index in (0, 1):
            self._tb_selection.setEnabled(False)
            self._system_edit.setEnabled(False)
            self._raster_edit.setEnabled(False)
        else:
            self._tb_selection.setEnabled(True)
            self._system_edit.setEnabled(True)
            self._raster_edit.setEnabled(True)

    def _tb_column_changed(self, value):
        self._raster_edit.set_value(value)


class Table2ADAFSuperNode(object):
    tags = Tags(Tag.DataProcessing.Convert)
    parameters = synode.parameters()
    parameters.set_list(
        'export_to_group', plist=['Meta', 'Result', 'Time series'],
        label='Export to group',
        description=(
            'Choose a container in the ADAF as target for the export'),
        editor=synode.Util.combo_editor())

    tb_editor = _get_single_tb_editor()
    tb_editor.set_attribute('filter', True)
    parameters.set_string('system', label='Timeseries system name',
                          description=('Specify name of the created system in '
                                       'the ADAF'),
                          value='system0')
    parameters.set_string('raster', label='Timeseries raster name',
                          description=('Specify name of the created raster in '
                                       'the ADAF'),
                          value='')
    parameters.set_list('tb',
                        label="Time basis column",
                        description=('Select a column in the Table which will '
                                     'be the time basis signal in the ADAF'),
                        editor=tb_editor)


class Table2ADAF(Table2ADAFSuperNode, synode.Node):
    """
    Export the full content of a Table to a specified container in an ADAF.
    """

    author = "Alexander Busck"
    version = '1.0'
    name = 'Table to ADAF'
    description = 'Export content of Table to specified container in ADAF.'
    nodeid = 'org.sysess.sympathy.data.table.table2adaf'
    icon = 'import_table.svg'
    related = ['org.sysess.sympathy.data.table.tables2adafs',
               'org.sysess.sympathy.data.table.updateadafwithtable',
               'org.sysess.sympathy.data.adaf.adaf2table']

    inputs = Ports([Port.Table('Input Table', name='port1')])
    outputs = Ports([Port.ADAF('ADAF with data in input Table', name='port1')])

    def update_parameters(self, old_params):
        param = 'tb'
        if param in old_params:
            old_params[param].editor = _get_single_tb_editor()

    def adjust_parameters(self, node_context):
        adjust(node_context.parameters['tb'],
               node_context.input['port1'])

    def exec_parameter_view(self, node_context):
        return TableConvertWidget(node_context)

    def execute(self, node_context):
        parameters = node_context.parameters
        group_name = parameters['export_to_group'].selected
        tb_column = parameters['tb'].value_names
        system_name = parameters['system'].value
        raster_name = parameters['raster'].value

        export_to = group_name.lower()
        tablefile = node_context.input['port1']
        adaffile = node_context.output['port1']
        if export_to in ('meta', 'result'):
            write_tabledata_to_adaf(export_to == 'meta', tablefile,
                                    adaffile)
        else:
            write_table_timeseries_to_adaf(system_name, raster_name,
                                           tb_column[0], tablefile,
                                           adaffile)


@node_helper.list_node_decorator(['port1'], ['port1'])
class Tables2ADAFs(Table2ADAF):
    name = 'Tables to ADAFs'
    nodeid = 'org.sysess.sympathy.data.table.tables2adafs'


class UpdateADAFWithTable(Table2ADAF):
    """
    Update ADAF with the full content of a Table to a specified container in
    the ADAF. Existing container will be replaced completely.
    """

    author = "Erik der Hagopian"
    version = '1.0'
    name = 'Update ADAF with Table'
    description = 'Export content of Table to specified container in ADAF.'
    nodeid = 'org.sysess.sympathy.data.table.updateadafwithtable'
    icon = 'import_table.svg'
    tags = Tags(Tag.DataProcessing.Convert)
    related = ['org.sysess.sympathy.data.table.updateadafswithtables',
               'org.sysess.sympathy.data.table.table2adaf',
               'org.sysess.sympathy.data.adaf.adaf2table']

    inputs = Ports([Port.Table('Input Table', name='port1'),
                    Port.ADAF('Input ADAF', name='port2')])
    outputs = Ports([Port.ADAF(
        'ADAF updated with data in input Table', name='port1')])

    def execute(self, node_context):
        node_context.output['port1'].source(node_context.input['port2'])
        super(UpdateADAFWithTable, self).execute(node_context)


@node_helper.list_node_decorator(['port1', 'port2'], ['port1'])
class UpdateADAFsWithTables(UpdateADAFWithTable):
    name = 'Update ADAFs with Tables'
    nodeid = 'org.sysess.sympathy.data.table.updateadafswithtables'
