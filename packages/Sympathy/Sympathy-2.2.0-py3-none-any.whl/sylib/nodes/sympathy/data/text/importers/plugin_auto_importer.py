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
from Qt.QtWidgets import QLabel

from sympathy.api import importers
from sympathy.api.exceptions import SyDataError


class DataImportAuto(importers.TextDataImporterBase):
    """Auto importer."""
    IMPORTER_NAME = "Auto"

    def __init__(self, fq_infilename, parameters):
        super(DataImportAuto, self).__init__(fq_infilename, parameters)

    def valid_for_file(self):
        """Never valid when sniffing."""
        return False

    def is_type(self):
        return False

    def parameter_view(self, parameters):
        if self._fq_infilename is not None:
            importer_class = (
                importers.plugin_for_file(
                    importers.TextDataImporterBase,
                    self._fq_infilename))
        else:
            importer_class = None

        if importer_class is None:
            text = "No importer could automatically be found for this file."
        else:
            text = "This file will be imported using the {} importer.".format(
                importer_class.display_name())
        return QLabel(text)

    def import_data(self, out_datafile, parameters=None, progress=None):
        """Sniff all available importers."""
        importer_class = (
            importers.plugin_for_file(
                importers.TextDataImporterBase,
                self._fq_infilename))
        if importer_class is None:
            raise SyDataError(
                "No importer could automatically be found for this file.")
        importer = importer_class(self._fq_infilename, self._parameters)
        importer.import_data(out_datafile, parameters, progress)
