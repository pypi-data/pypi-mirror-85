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
import inspect
from Qt.QtWidgets import QLabel

from sympathy.api import importers
from sympathy.api.exceptions import SyDataError


def hasarg(func, arg):
    return arg in inspect.getargspec(func).args


class DataImportAuto(importers.ADAFDataImporterBase):
    """Auto importer."""
    IMPORTER_NAME = "Auto"

    def __init__(self, fq_infilename, parameters):
        self.__importer_class = None
        super(DataImportAuto, self).__init__(fq_infilename, parameters)

    def _importer_class(self):
        if self._fq_infilename is not None:
            if self.__importer_class is None:
                self.__importer_class = (
                    importers.plugin_for_file(
                        importers.ADAFDataImporterBase,
                        self._fq_infilename))
        return self.__importer_class

    def valid_for_file(self):
        """Never valid when sniffing."""
        return False

    def is_type(self):
        importer_class = self._importer_class()

        if importer_class is None:
            raise SyDataError(
                "No importer could automatically be found for this file.")
        importer = importer_class(self._fq_infilename, None)
        return importer.is_type()

    def parameter_view(self, parameters):
        importer_class = self._importer_class()

        if importer_class is None:
            text = "No importer could automatically be found for this file."
        else:
            text = "This file will be imported using the {} importer.".format(
                importer_class.display_name())
        return QLabel(text)

    def import_data(self, out_datafile, parameters=None, progress=None,
                    manage_input=None):
        """Sniff all available importers."""
        importer_class = self._importer_class()

        if importer_class is None:
            raise SyDataError(
                "No importer could automatically be found for this file.")
        importer = importer_class(self._fq_infilename, parameters)

        if hasarg(importer.import_data, 'manage_input'):
            importer.import_data(out_datafile, parameters, progress,
                                 manage_input)
        else:
            importer.import_data(out_datafile, parameters, progress)
