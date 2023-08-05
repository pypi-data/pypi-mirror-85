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
import traceback

from .. utils.components import get_components
from .. utils import context
from .. platform.exceptions import sywarn
from .. api import component
from .. platform import qt_compat2
QtGui = qt_compat2.import_module(str('QtGui'))
QtWidgets = qt_compat2.import_module(str('QtWidgets'))


class DATASOURCE(object):
    FILE = 'FILE'
    DATABASE = 'DATABASE'


class IDataImportFactory(object):
    """A factory interface for DataImporters."""
    def __init__(self):
        super(IDataImportFactory, self).__init__()

    def importer_from_datasource(self, datasource):
        """Get an importer from the given datasource."""
        raise NotImplementedError("Not implemented for interface.")


class IDataSniffer(object):
    def __init__(self):
        super(IDataSniffer, self).__init__()

    def sniff(self, path):
        """Sniff the given file and return the data format."""
        raise NotImplementedError("Not implemented for interface.")


class IDataImporterWidget(object):
    """Interface for data importer widgets, used to configure
    parameters to the importer."""
    def __init__(self):
        pass


class DataImporterLocator(object):
    """Given a folder locate all eligable importer classes derived from
    the IDataImporter interface."""
    def __init__(self, importer_parent_class):
        super(DataImporterLocator, self).__init__()
        self._importer_parent_class = importer_parent_class

    def importer_from_sniffer(self, file2import):
        """Use sniffers to evaluate a valid importer and return it."""
        def valid_importer(c):
            return c(file2import, None).valid_for_file()

        for importer in get_components('plugin_*.py',
                                       self._importer_parent_class):
            try:
                if valid_importer(importer):
                    return importer
            except Exception:
                sywarn("{} importer failed to sniff resource. "
                       "The exception was:\n{}".format(
                           importer.display_name(), traceback.format_exc()))

        return None

    def importer_from_name(self, importer_name):
        """Return the importer associated with importer_name."""
        importers = get_components('plugin_*.py', self._importer_parent_class)
        valid_importers = (importer for importer in importers
                           if importer.IMPORTER_NAME == importer_name)
        try:
            return next(valid_importers)
        except StopIteration:
            raise KeyError(importer_name)

    def available_importers(self, datasource_compatibility=None):
        """Return the available importers."""
        importers = get_components('plugin_*.py', self._importer_parent_class)
        if datasource_compatibility is None:
            return {importer.IMPORTER_NAME: importer for importer in importers}
        else:
            return {importer.IMPORTER_NAME: importer for importer in importers
                    if datasource_compatibility in importer.DATASOURCES}


class ImporterConfigurationWidget(QtWidgets.QWidget):
    def __init__(self, available_importers, parameters,
                 fq_infilename, cardinalities=None, parent=None):
        if cardinalities is None:
            cardinalities = []

        super(ImporterConfigurationWidget, self).__init__(parent)
        self._parameters = parameters
        self._custom_parameters = self._parameters["custom_importer_data"]
        self._available_importers = available_importers
        self._importer_name = None
        self._fq_infilename = fq_infilename
        self._cardinalities = cardinalities
        self.widgets = []

        self._init_gui()
        self._init_gui_from_parameters()

    def _init_gui(self):
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        hlayout = QtWidgets.QHBoxLayout()

        importer_label = QtWidgets.QLabel("Importer to use")
        self._importer_combobox = QtWidgets.QComboBox()
        hlayout.addWidget(importer_label)
        hlayout.addWidget(self._importer_combobox)
        hlayout.addSpacing(250)

        self.stacked_widget = QtWidgets.QStackedWidget()

        importers = sorted(
            self._available_importers.values(),
            key=lambda x: x.display_name())

        for i, importer_cls in enumerate(importers):
            self._importer_combobox.addItem(importer_cls.display_name())
            self._importer_combobox.setItemData(i, importer_cls.identifier())

        for importer_cls in importers:
            imp_name = importer_cls.identifier()
            disp_name = importer_cls.display_name()

            try:
                if imp_name not in self._custom_parameters:
                    self._custom_parameters.create_group(imp_name)

                importer = importer_cls(self._fq_infilename,
                                        self._custom_parameters[imp_name])

                importer.set_supported_cardinalities(self._cardinalities)

                if not context.is_original(importer.parameter_view):
                    parameter_widget = (
                        importer.parameter_view(
                            self._custom_parameters[imp_name]))
                else:
                    parameter_widget = QtWidgets.QLabel()

            except Exception:
                parameter_widget = QtWidgets.QLabel('Failed to load')
                sywarn("{} importer failed to build its configuration gui. "
                       "The exception was:\n{}".format(
                           disp_name, traceback.format_exc()))

            self.stacked_widget.addWidget(parameter_widget)
            self.widgets.append(parameter_widget)

        vlayout.addItem(hlayout)
        vlayout.addWidget(self.stacked_widget)
        vlayout.addItem(QtWidgets.QSpacerItem(500, 1))
        fail_layout = QtWidgets.QHBoxLayout()
        fail_layout.addWidget(self._parameters['fail_strategy'].gui())
        vlayout.addItem(fail_layout)
        self.setLayout(vlayout)

        self._importer_combobox.currentIndexChanged[int].connect(
            self._importer_changed)
        self._importer_combobox.activated.connect(
            self.stacked_widget.setCurrentIndex)

    def _init_gui_from_parameters(self):
        active_importer = self._parameters["active_importer"].value
        index = self._importer_combobox.findData(active_importer)
        # Select the first item if none is selected.
        if index == -1:
            self._importer_combobox.setCurrentIndex(0)
        else:
            self._importer_combobox.setCurrentIndex(index)

    def _importer_changed(self, index):
        active_importer = str(self._importer_combobox.itemData(index))
        self._parameters["active_importer"].value = active_importer
        self.stacked_widget.setCurrentIndex(index)

    def cleanup(self):
        for parameter_widget in self.widgets:
            if parameter_widget and hasattr(parameter_widget, 'cleanup'):
                parameter_widget.cleanup()


# External API

class IDataImporter(component.NodePlugin):
    """Interface for a DataImporter. It's important to set IMPORTER_NAME
    to a unique name otherwise errors will occur."""
    IMPORTER_NAME = "UNDEFINED"
    DISPLAY_NAME = None
    DATASOURCES = [DATASOURCE.FILE]
    one_to_one, one_to_many, many_to_one = range(3)

    def __init__(self, fq_infilename, parameters):
        """
        Parameters
        ----------
        fq_infilename : str
                        Fully qualified filename.
        parameters : ParameterGroup or NoneType
                     plugin parameters or None, make sure to handle the case
                     where None is passed for parameters.
        """
        self._cardinality = self.one_to_one
        self._fq_infilename = fq_infilename
        self._parameters = parameters
        self._supported_cardinalities = None

        super(IDataImporter, self).__init__()

    @classmethod
    def identifier(cls):
        """
        Returns
        -------
        str
            Unique identifier for importer.
        """
        return cls.IMPORTER_NAME

    @classmethod
    def display_name(cls):
        """
        Returns
        -------
        str
            Display name for importer.
        """
        return cls.DISPLAY_NAME or cls.IMPORTER_NAME

    def valid_for_file(self):
        """
        Returns
        -------
        bool
            True if plugin handles self._fq_infilename.
        """
        return False

    def import_data(self, out_file, parameters=None, progress=None):
        """
        Fill out_file with data.
        """
        raise NotImplementedError

    @classmethod
    def name(cls):
        """
        Returns
        -------
        str
            Name for importer.
        """
        return cls.IMPORTER_NAME

    @context.original
    def parameter_view(self, parameters):
        """
        Returns
        -------
        QtWidgets.QWidget
            GUI widget for importer.
        """
        return QtWidgets.QWidget()

    def is_type(self):
        """
        Returns
        -------
        bool
            True if self._fq_infilename points to a native "sydata file.
        """
        return False

    @classmethod
    def cardinalities(cls):
        """
        Return list of options for cardinality. In order of preference, first
        choice is the preferred.
        """
        return [cls.one_to_one]

    def cardinality(self):
        """
        Relation between input elements and output elements created.
        The result is the first out of any items from cardinalities()
        that is also part of the cardinalites set as supported using
        set_supported_cardinalities().

        Returns
        -------
        int
            Cardinality enum.
            IDataImporter.one_to_one, IDataImporter.one_to_many
            IDataImporter.many_to_one.
        """
        supported = self._supported_cardinalities or []
        for option in self.cardinalities():
            if option in supported:
                return option

        return self.one_to_one

    def set_supported_cardinalities(self, options):
        """
        Set relation between input elements and output elements created
        that is supported for the importer.

        Parameters
        ----------
        options : list of Cardinality enum
            List of supported cardinalities for importer.
        """
        self._supported_cardinalities = options

    @classmethod
    def plugin_impl_name(cls) -> str:
        return cls.display_name()


class ADAFDataImporterBase(IDataImporter):

    def __init__(self, fq_infilename, parameters):
        super(ADAFDataImporterBase, self).__init__(fq_infilename, parameters)

    @staticmethod
    def plugin_base_name():
        return 'Import ADAF'

    def valid_for_file(self):
        """Return True if this importer is valid for fq_filename."""
        return False

    def is_type(self):
        return self.is_adaf()

    def is_adaf(self):
        """Is the file to be imported a valid ADAF file."""
        return False


class TableDataImporterBase(IDataImporter):

    def __init__(self, fq_infilename, parameters):
        super(TableDataImporterBase, self).__init__(fq_infilename, parameters)

    @staticmethod
    def plugin_base_name():
        return 'Import Table'

    def valid_for_file(self):
        """Return True if this importer is valid for fq_filename."""
        return False

    def is_type(self):
        return self.is_table()

    def is_table(self):
        """Is the file to be imported a valid Table file."""
        return False


class TextDataImporterBase(IDataImporter):

    def __init__(self, fq_infilename, parameters):
        super(TextDataImporterBase, self).__init__(fq_infilename, parameters)

    @staticmethod
    def plugin_base_name():
        return 'Import Text'

    def valid_for_file(self):
        """Return True if this importer is valid for fq_filename."""
        return False

    def is_type(self):
        return self.is_text()

    def is_text(self):
        """Is the file to be imported a valid Table file."""
        return False


class JsonDataImporterBase(IDataImporter):

    def __init__(self, fq_infilename, parameters):
        super(JsonDataImporterBase, self).__init__(fq_infilename, parameters)

    @staticmethod
    def plugin_base_name():
        return 'Import JSON'

    def valid_for_file(self):
        """Return True if this importer is valid for fq_filename."""
        return False

    def is_type(self):
        return self.is_json()

    def is_json(self):
        """Is the file to be imported a valid Json file."""
        return False


def available_plugins(plugin_base_class, datasource_compatibility=None):
    dil = DataImporterLocator(plugin_base_class)
    return dil.available_importers(datasource_compatibility)


def plugin_for_file(plugin_base_class, filename):
    dil = DataImporterLocator(plugin_base_class)
    return dil.importer_from_sniffer(filename)


def configuration_widget(plugins, parameters, filename,
                         cardinalities=None):
    return ImporterConfigurationWidget(plugins, parameters, filename,
                                       cardinalities=cardinalities)
