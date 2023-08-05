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
from . base import (
    DataImporterLocator, ADAFDataImporterBase, TableDataImporterBase,
    TextDataImporterBase)


def table_importer_from_filename_factory(fq_filename):
    dil = DataImporterLocator(TableDataImporterBase)
    importer = dil.importer_from_sniffer(fq_filename)
    return importer


def adaf_importer_from_filename_factory(fq_filename):
    dil = DataImporterLocator(ADAFDataImporterBase)
    importer = dil.importer_from_sniffer(fq_filename)
    return importer


def text_importer_from_filename_factory(fq_filename):
    dil = DataImporterLocator(TextDataImporterBase)
    importer = dil.importer_from_sniffer(fq_filename)
    return importer


def table_importer_from_datasource_factory(datasource, importer_type):
    return importer_from_datasource_factory(
        datasource, importer_type, TableDataImporterBase)


def adaf_importer_from_datasource_factory(datasource, importer_type):
    return importer_from_datasource_factory(
        datasource, importer_type, ADAFDataImporterBase)


def text_importer_from_datasource_factory(datasource, importer_type):
    return importer_from_datasource_factory(
        datasource, importer_type, TextDataImporterBase)


def importer_from_datasource_factory(datasource, importer_type,
                                     importer_base_class):
    dil = DataImporterLocator(importer_base_class)
    assert(importer_type is not None)
    importer = dil.importer_from_name(importer_type)
    return importer


def available_adaf_importers():
    dil = DataImporterLocator(ADAFDataImporterBase)
    return dil.available_importers()


def available_table_importers(datasource_compatibility=None):
    dil = DataImporterLocator(TableDataImporterBase)
    return dil.available_importers(datasource_compatibility)


def available_text_importers():
    dil = DataImporterLocator(TextDataImporterBase)
    return dil.available_importers()


def available_adaf_importer_names():
    dil = DataImporterLocator(ADAFDataImporterBase)
    return sorted(dil.available_importers().keys())


def available_table_importer_names():
    dil = DataImporterLocator(TableDataImporterBase)
    return sorted(dil.available_importers().keys())
