# This file is part of Sympathy for Data.
# Copyright (c) 2016, 2017, Combine Control Systems AB
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
import os
import copy

from sympathy.api import node as synode
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, deprecated_node
from sympathy.api import exporters
from sylib.export import base


inches_per_mm = 0.039370


class ExportFigures(base.ExportMultiple, synode.Node):
    """
    Export Figures to a selected data format.

    :Ref. nodes:
        :ref:`org.sysess.sympathy.visualize.figure`,
        :ref:`org.sysess.sympathy.visualize.figures`
    """

    name = 'Export Figures'
    description = 'Export Figures to image files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Benedikt Ziegler'
    nodeid = 'org.sysess.sympathy.export.exportfigures'
    version = '0.2'
    inputs = Ports([Port.Figures('Input figures', name='figures'),
                    Port.Datasources(
                        'External filenames',
                        name='port1', n=(0, 1, 0))])
    plugins = (exporters.FigureDataExporterBase, )
    parameters = base.base_params()

    def update_parameters(self, old_params):
        if 'custom_exporter_data' not in old_params:
            custom_exporter_data = old_params.create_group(
                'custom_exporter_data')
        else:
            custom_exporter_data = old_params['custom_exporter_data']

        # Update to next version
        extension = old_params._parameter_dict.pop('extension', None)
        width = old_params._parameter_dict.pop('width', None)
        height = old_params._parameter_dict.pop('height', None)
        if 'Image' not in custom_exporter_data:
            image = custom_exporter_data.create_group('Image')
        else:
            image = custom_exporter_data['Image']
        if extension is not None:
            image.set_list('extension',
                           label=extension['label'],
                           description=extension['description'],
                           value=extension['value'],
                           plist=extension['list'],
                           editor=extension['editor'])
        if width is not None:
            image.set_integer('width',
                              label=width['label'],
                              description=width['description'],
                              value=width['value'],
                              editor=width['editor'])
        if height is not None:
            image.set_integer('height',
                              label=height['label'],
                              description=height['description'],
                              value=height['value'],
                              editor=height['editor'])

        # Update to next version
        vectorized_extensions = ['eps', 'pdf', 'ps', 'svg', 'svgz']
        try:
            active_exporter_data = (
                old_params._parameter_dict['active_exporter'])
            active_exporter = active_exporter_data['value']
            old_exporter_data = custom_exporter_data._parameter_dict['Image']
            extension_data = old_exporter_data['extension']
            extension = extension_data['value_names'][0]
            strategy = old_exporter_data['selected_strategy']['value_names'][0]
            dpi = old_exporter_data['dpi']['value']
        except Exception:
            pass
        else:
            if active_exporter == 'Image' and extension in vectorized_extensions:
                active_exporter_data['value'] = 'Vectorized'
                group = custom_exporter_data.create_group('Vectorized')
                params_to_copy = [
                    'paper_orientation',
                    'paper_size',
                    'size_height',
                    'size_width',
                ]
                for param_name in params_to_copy:
                    group.parameter_dict[param_name] = copy.deepcopy(
                        old_exporter_data[param_name])
                if strategy == 'Set Pixels':
                    for param_name in ['height', 'width']:
                        new_param = group.parameter_dict['size_' + param_name]
                        old_px_size = old_exporter_data[param_name]['value']
                        new_param['value'] = old_px_size/dpi/inches_per_mm
                group.set_list('extension',
                               label=extension_data['label'],
                               description=extension_data['description'],
                               value_names=[extension],
                               plist=vectorized_extensions,
                               editor=extension_data['editor'])
            elif active_exporter == 'Image' and 'svg' in extension_data['list']:
                # This is an old Image plugin containing both vectorized and
                # rasterized formats, and with rasterized format selected.
                exporter = custom_exporter_data['Image']
                exporter['extension'].list = [extension]
                if strategy == 'Set Pixels' and dpi != 96:
                    exporter['selected_strategy'].selected = 'Set Page Size'
                    for param_name in ['height', 'width']:
                        old_px_size = exporter[param_name].value
                        new_param = exporter['size_' + param_name]
                        new_param.value = old_px_size/dpi/inches_per_mm

        return old_params


@deprecated_node('3.0.0', 'Export Figures (with optional datasource port)')
class ExportFiguresWithDsrcs(base.ExportMultiple, synode.Node):
    """
    Export Figures to a selected data format with a list of datasources for
    output paths.
    """

    name = 'Export Figures with Datasources'
    description = 'Export Figures to image files.'
    icon = 'export_figure.svg'
    tags = Tags(Tag.Output.Export)
    author = 'Magnus Sandén'
    nodeid = 'org.sysess.sympathy.export.exportfigureswithdscrs'
    version = '0.1'

    inputs = Ports([
        Port.Figures('Input figures', name='figures'),
        Port.Datasources('Datasources', name='dsrcs')])
    plugins = (exporters.FigureDataExporterBase, )
    parameters = base.base_params()

    def _exporter_ext_filenames_portname(self):
        return 'dsrcs'

    def _exporter_ext_filename(self, custom_parameters, filename):
        if not os.path.splitext(filename)[1]:
            ext = custom_parameters['extension'].selected
            filename = '{}.{}'.format(filename, ext)
        return filename
