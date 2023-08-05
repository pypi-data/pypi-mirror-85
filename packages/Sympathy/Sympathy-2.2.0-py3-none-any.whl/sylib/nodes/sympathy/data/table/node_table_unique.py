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
from sympathy.api import node as synode
from sympathy.api import node_helper
from sympathy.api.nodeconfig import Tag, Tags, adjust
from sympathy.api import table


class UniqueOperation(node_helper._TableOperation):
    """
    The Table in the output will have no more rows than the incoming Table.
    """

    author = 'Greger Cronquist'
    description = ('For each unique value in selected columns only keep the '
                   'first row with that value. When multiple columns are '
                   'selected, unique combinations of values are considered.')
    nodeid = 'org.sysess.sympathy.data.table.uniquetables'
    icon = 'unique_table.svg'
    version = '1.0'
    inputs = ['Input']
    outputs = ['Output']
    tags = Tags(Tag.DataProcessing.Select)

    @staticmethod
    def get_parameters(parameter_group):
        editor = synode.Util.multilist_editor(edit=True)
        parameter_group.set_list(
            'column', label='Columns to filter by',
            description='Columns to use as uniqueness filter.',
            editor=editor)

    def adjust_table_parameters(self, in_table, parameters):
        adjust(parameters['column'], in_table['Input'])

    def execute_table(self, in_table, out_table, parameters):
        current_selected = parameters['column'].selected_names(
            in_table['Input'].names())
        if not (in_table['Input'].number_of_rows() and current_selected):
            out_table['Output'].update(in_table['Input'])
            return

        df = in_table['Input'].to_dataframe()
        df2 = df.drop_duplicates(current_selected)

        out_table['Output'].source(table.File.from_dataframe(df2))
        out_table['Output'].set_attributes(in_table['Input'].get_attributes())
        out_table['Output'].set_name(in_table['Input'].get_name())


UniqueTable = node_helper._table_node_factory(
    'UniqueTable', UniqueOperation,
    'Unique Table', 'org.sysess.sympathy.data.table.uniquetable')


UniqueTables = node_helper._tables_node_factory(
    'UniqueTables', UniqueOperation,
    'Unique Tables', 'org.sysess.sympathy.data.table.uniquetables')
