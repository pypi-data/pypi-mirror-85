# This file is part of Sympathy for Data.
# Copyright (c) 2015, Combine Control Systems AB
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
import json
import collections

import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets

from sylib.report import data_manager


class SignalMappingWidget(QtWidgets.QWidget):
    """Class to be used as GUI in Report Apply nodes."""

    delegate = None

    def __init__(self, parameter_root, document, input_data, data_type,
                 parent=None):
        super(SignalMappingWidget, self).__init__(parent)
        if input_data:
            data_manager.init_data_source(input_data, data_type)

        self.parameter_root = parameter_root

        self.remove_invalid_sources()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        self.setLayout(layout)
        layout.addWidget(QtWidgets.QLabel('Signal Mapping'))
        layout.addWidget(self.build_signal_mapping_widget(
            parameter_root, document))
        if 'save_path' in list(parameter_root.keys()):
            layout.addWidget(self.build_save_path_widget())
            layout.addWidget(self.build_prefix_widget())
        layout.addWidget(self.build_file_format_widget())

    def build_signal_mapping_widget(self, parameter_root, document):
        model = SignalMappingModel(parameter_root, document)
        self.delegate = None
        w = QtWidgets.QTableView()
        w.setModel(model)
        w.resizeRowsToContents()
        w.resizeColumnsToContents()
        w.setShowGrid(False)
        w.setAlternatingRowColors(True)
        w.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        w.horizontalHeader().setStretchLastSection(True)
        w.verticalHeader().hide()
        w.sizePolicy().setVerticalStretch(5)

        if data_manager.data_source:
            self.delegate = ComboDelegate(
                parameter_root, data_manager.data_source.signal_list())
        w.setItemDelegateForColumn(0, self.delegate)

        return w

    def build_save_path_widget(self):
        w = self.parameter_root['save_path'].gui()
        return w

    def build_prefix_widget(self):
        w = self.parameter_root['filename_prefix'].gui()
        return w

    def build_file_format_widget(self):
        w = self.parameter_root['file_format'].gui()
        return w

    def remove_invalid_sources(self):
        # Remove invalid mappings in case the signal source was changed.
        signal_mapping = json.loads(
            self.parameter_root['signal_mapping'].value)
        invalid_targets = []
        for target_signal, source_signal in signal_mapping.items():
            if source_signal not in data_manager.data_source.signal_list():
                invalid_targets.append(target_signal)
        for invalid_target in invalid_targets:
            del signal_mapping[invalid_target]
        self.parameter_root['signal_mapping'].value = json.dumps(
            signal_mapping)


class SignalMappingModel(QtCore.QAbstractTableModel):
    def __init__(self, parameter_root, document, parent=None):
        super(SignalMappingModel, self).__init__(parent)

        if data_manager.data_source:
            self.input_signals = data_manager.data_source.signal_list()
        self.template_signals = self.used_template_signals(document)
        self.parameter_root = parameter_root

    @staticmethod
    def used_template_signals(document):
        """
        Extract a list of all template signals which are referred to in the
        document.
        :return: List of all signals which are used.
        """
        available_signals = None
        if document:
            available_signals = document['signals']

        def walk_document(item):
            signal_set = set()
            if isinstance(item, str):
                if item in available_signals:
                    signal_set.add(item)
            elif isinstance(item, collections.Sequence):
                for list_item in item:
                    signal_set.update(walk_document(list_item))
            elif isinstance(item, collections.Mapping):
                for key, value in item.items():
                    if key == 'signals':
                        continue
                    signal_set.update(walk_document(value))
            return signal_set

        used_signals = sorted(list(walk_document(document)))

        return used_signals

    def rowCount(self, parent_index=QtCore.QModelIndex()):
        return len(self.template_signals)

    def columnCount(self, parent_index=QtCore.QModelIndex()):
        return 2

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                if section == 0:
                    return 'Source Input Signal'
                elif section == 1:
                    return 'Target Template Signal'
        return None

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                signal_mapping = json.loads(self.parameter_root[
                    'signal_mapping'].value)
                return signal_mapping.get(
                    self.template_signals[index.row()], None)
            elif index.column() == 1:
                return self.template_signals[index.row()]
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.column() == 0:
            target_signal = self.data(self.index(index.row(), 1))
            signal_mapping = json.loads(
                self.parameter_root['signal_mapping'].value)
            signal_mapping[target_signal] = value
            self.parameter_root['signal_mapping'].value = json.dumps(
                signal_mapping)
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    def remove_mapping(self, index):
        target_signal = self.data(self.index(index.row(), 1))
        signal_mapping = json.loads(
            self.parameter_root['signal_mapping'].value)
        try:
            del signal_mapping[target_signal]
            self.parameter_root['signal_mapping'].value = json.dumps(
                signal_mapping)
        except KeyError:
            pass


class ComboDelegate(QtWidgets.QStyledItemDelegate):
    editor = None

    def __init__(self, parameter_root, signal_list, parent=None):
        super(ComboDelegate, self).__init__(parent)
        self.parameter_root = parameter_root
        self.signal_list = signal_list

    def createEditor(self, parent_widget, style_option, model_index):
        editor = QtWidgets.QComboBox(parent_widget)
        editor.addItem('<none>')
        item_list = ['{} : {}'.format(
            data_manager.data_source.row_count(name), name)
            for name in self.signal_list]
        editor.addItems(item_list)
        return editor

    def setEditorData(self, editor_widget, model_index):
        source_signal = model_index.data()
        if source_signal is None or len(source_signal) == 0:
            row = -1
        else:
            row = self.signal_list.index(source_signal)
        editor_widget.setCurrentIndex(row + 1)

    def updateEditorGeometry(self, editor_widget, style_option, model_index):
        editor_widget.setGeometry(style_option.rect)

    def setModelData(self, editor_widget, model, model_index):
        current_row = editor_widget.currentIndex()
        if current_row == 0:
            model.remove_mapping(model_index)
        else:
            model.setData(model_index, self.signal_list[current_row - 1])
