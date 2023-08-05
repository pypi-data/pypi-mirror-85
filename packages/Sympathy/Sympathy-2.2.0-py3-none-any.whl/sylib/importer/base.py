# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2017-2018 Combine Control Systems AB
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
from collections import OrderedDict
import inspect
import sys
import os
import sympathy.api
from sympathy.api import node as synode
from sympathy.api import datasource as dsrc
from sympathy.api import importers
from sympathy.api.nodeconfig import Port, Ports, Tag, Tags, settings
from sympathy.api import exceptions
import sylib.url


def hasarg(func, arg):
    return arg in inspect.getargspec(func).args


FAILURE_STRATEGIES = OrderedDict(
    [('Exception', 0), ('Create Empty Entry', 1)])

LIST_FAILURE_STRATEGIES = OrderedDict(
    [('Exception', 0), ('Create Empty Entry', 1), ('Skip File', 2)])


def _set_supported_cardinalities(importer, multi):
    options = [importer.one_to_one]
    if multi:
        options = [importer.one_to_many, importer.one_to_one]
    importer.set_supported_cardinalities(options)


def import_data(item_factory, importer_cls, datasource,
                parameters, manage_input, progress, multi=False):

    def import_native(importer, dspath, manage_input):
        """
        Special case where the file is native sydata of the right type and
        should be copied into the platform.
        """
        try:
            # Got plugin adaf importer.
            import_links = importer.import_links
        except AttributeError:
            import_links = False

        ds_infile = item_factory(importer.cardinality())(
            filename=dspath, mode='r', import_links=import_links)
        if manage_input is not None:
            manage_input(dspath, ds_infile)
        return ds_infile

    def import_external(importer, parameters, progress, manage_input):

        output = item_factory(importer.cardinality())()
        if hasarg(importer.import_data, 'manage_input'):
            importer.import_data(
                output, parameters, progress=progress,
                manage_input=manage_input)
        else:
            importer.import_data(
                output, parameters, progress=progress)
        return output

    dspath = datasource.decode_path()
    importer = importer_cls(dspath, parameters)

    _set_supported_cardinalities(importer, multi)

    if importer.is_type():
        return (import_native(importer, dspath, manage_input),
                importer.cardinality())
    return (import_external(importer, parameters, progress, manage_input),
            importer.cardinality())


class SuperNode(object):
    tags = Tags(Tag.Input.Import)
    plugins = (importers.IDataImporter, )

    @staticmethod
    def parameters_base():
        parameters = synode.parameters()
        parameters.set_string(
            'active_importer', label='Importer', value='Auto',
            description=('Select data format importer'))
        custom_importer_group = parameters.create_group(
            'custom_importer_data')
        custom_importer_group.create_group('Auto')
        return parameters

    def _available_plugins(self, name=None):
        return importers.available_plugins(self.plugins[0])

    def _create_temp_file_datasource(self, datasource):
        return sylib.url.download_datasource(
            datasource,
            tempfile_kwargs=dict(prefix='import_http_',
                                 dir=settings()['session_folder']))

    def _remove_temp_file_datasource(self, url_temp_filename):
        if url_temp_filename:
            try:
                os.remove(url_temp_filename)
            except (OSError, IOError):
                pass

    def _output_item_filename_hook(self, output_item, filename):
        pass


class ImportSingle(SuperNode):
    inputs = Ports([Port.Datasource('Datasource')])

    parameters = SuperNode.parameters_base()
    parameters.set_list(
        'fail_strategy', label='Action on import failure',
        list=list(FAILURE_STRATEGIES.keys()), value=[0],
        description='Decide how failure to import a file should be handled.',
        editor=synode.Util.combo_editor())

    def exec_parameter_view(self, node_context):
        dspath = None
        try:
            datasource = node_context.input.first
            dspath = datasource.decode_path()
        except exceptions.NoDataError:
            # This is if no input is connected.
            pass
        return importers.configuration_widget(
            self._available_plugins(),
            node_context.parameters, dspath,
            cardinalities=[importers.IDataImporter.one_to_one])

    def execute(self, node_context):

        def item_factory(cardinality):
            if cardinality == importer_cls.one_to_one:
                return type(node_context.output.first)
            assert False, (
                'Single importer plugin must support one to one relation '
                'between input and output.')

        params = synode.parameters(node_context.parameters)
        importer_type = params['active_importer'].value
        if 'fail_strategy' in params:
            fail_strategy = params['fail_strategy'].value[0]
        else:
            fail_strategy = 0

        url_temp_filename = None
        try:
            importer_cls = self._available_plugins().get(importer_type)
            datasource = node_context.input.first

            if datasource.decode_type() == datasource.modes.url:
                datasource = self._create_temp_file_datasource(datasource)
                url_temp_filename = datasource['path']

            importer_cls = self._available_plugins().get(importer_type)
            ds_dict = datasource.decode()

            if importer_cls is None:
                raise exceptions.SyConfigurationError(
                    "Selected importer plugin ({}) could not be found.".format(
                        importer_type))

            with import_data(
                    item_factory,
                    importer_cls, datasource,
                    params["custom_importer_data"][importer_type],
                    None,
                    progress=self.set_progress, multi=False)[0] as output:

                if ds_dict['type'] == 'FILE':
                    self._output_item_filename_hook(output, ds_dict['path'])

                node_context.output.first.source(output)
        except Exception:
            if fail_strategy == FAILURE_STRATEGIES['Create Empty Entry']:
                pass
            else:
                raise
        finally:
            self._remove_temp_file_datasource(url_temp_filename)

        self.set_progress(70)


class ImportMulti(SuperNode):
    inputs = Ports([
        Port.Datasources('Datasources', name='input')])

    parameters = SuperNode.parameters_base()
    parameters.set_list(
        'fail_strategy', label='Action on import failure',
        list=list(LIST_FAILURE_STRATEGIES.keys()), value=[0],
        description='Decide how failure to import a file should be handled.',
        editor=synode.Util.combo_editor())

    def exec_parameter_view(self, node_context):
        dspath = None
        try:
            try:
                datasource = node_context.input.first[0]
            except IndexError:
                datasource = dsrc.File()
            dspath = datasource.decode_path()
        except exceptions.NoDataError:
            # This is if no input is connected.
            pass

        return importers.configuration_widget(
            self._available_plugins(),
            node_context.parameters, dspath,
            cardinalities=[importers.IDataImporter.one_to_many,
                           importers.IDataImporter.one_to_one])

    def execute(self, node_context):

        def item_factory(cardinality):

            if cardinality == importer_cls.one_to_one:
                return type(output_list.create())
            elif cardinality == importer_cls.one_to_many:
                return (lambda *args, **kwargs:
                        sympathy.api.from_type(output_list.container_type))
            else:
                assert False, (
                    'List importer plugin must support one to one or '
                    'one to many relation between input and output.')

        params = node_context.parameters
        importer_type = params['active_importer'].value
        if 'fail_strategy' in params:
            fail_strategy = params['fail_strategy'].value[0]
        else:
            fail_strategy = 0

        input_list = node_context.input.first
        len_input_list = len(input_list)
        output_list = node_context.output.first

        for i, datasource in enumerate(input_list):
            url_temp_filename = None
            try:
                if datasource.decode_type() == datasource.modes.url:
                    datasource = self._create_temp_file_datasource(datasource)
                    url_temp_filename = datasource['path']

                importer_cls = self._available_plugins().get(importer_type)
                ds_dict = datasource.decode()
                if importer_cls is None:
                    raise exceptions.SyDataError(
                        "No importer could automatically be found for "
                        "this file.")

                output_item, cardinality = import_data(
                    item_factory,
                    importer_cls,
                    datasource,
                    params['custom_importer_data'][importer_type],
                    node_context.manage_input,
                    lambda x: self.set_progress(
                        (100 * i + x) / len_input_list), multi=True)

                if cardinality == importer_cls.one_to_one:
                    output_items = [output_item]
                elif cardinality == importer_cls.one_to_many:
                    output_items = output_item
                else:
                    raise NotImplementedError()

                if ds_dict['type'] == 'FILE':
                    for output_item in output_items:
                        self._output_item_filename_hook(
                            output_item, ds_dict['path'])
                for output_item in output_items:
                    output_list.append(output_item)
            except Exception:
                if fail_strategy == LIST_FAILURE_STRATEGIES['Exception']:
                    raise exceptions.SyListIndexError(i, sys.exc_info())
                elif fail_strategy == LIST_FAILURE_STRATEGIES[
                        'Create Empty Entry']:
                    print('Creating empty output file (index {}).'.format(i))
                    output_item = output_list.create()
                    output_list.append(output_item)
                else:
                    print('Skipping file (index {}).'.format(i))

            finally:
                self._remove_temp_file_datasource(url_temp_filename)

            self.set_progress(100 * (1 + i) / len_input_list)
