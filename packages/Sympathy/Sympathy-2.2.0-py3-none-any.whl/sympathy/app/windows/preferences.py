# This file is part of Sympathy for Data.
# Copyright (c) 2013 Combine Control Systems AB
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
import copy
import distutils.spawn
import collections
import pygments.styles
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from sympathy.platform import feature
from sympathy.platform import version_support as vs
from sympathy.platform import editor as editor_api
from sympathy.platform.widget_library import PathListWidget
from sympathy.app import settings
from sympathy.app.environment_variables import instance as env_instance
from sympathy.platform import library as library_platform
import sympathy.app.util
from .. flowview import grid
from .. import themes
num_recent_libs = 15
ENV = env_instance()


# Determines the order in which actions are applied
A_ENV, A_LIBRARY_PATH, A_LIBRARY_RELOAD, A_LIBRARY_TYPE, A_LIBRARY_HIGHLIGHTER = range(5)  # noqa


class BoolCheckBox(QtWidgets.QCheckBox):
    def __init__(self, param, parent=None):
        super().__init__(parent=parent)
        self._param = param
        self.update_value()

    def update_value(self):
        self.setChecked(settings.instance()[self._param])

    def save(self):
        settings.instance()[self._param] = self.isChecked()


class StringComboBox(QtWidgets.QComboBox):
    def __init__(self, param, options, parent=None):
        super().__init__(parent=parent)
        self.addItems(options)
        self._param = param
        self.update_value()

    def update_value(self):
        current_idx = self.findText(settings.instance()[self._param])
        if current_idx < 0:
            current_idx = self.findText(
                settings.permanent_defaults[self._param])
        self.setCurrentIndex(current_idx)

    def save(self):
        settings.instance()[self._param] = self.currentText()


class PreferenceSectionWidget(feature.PreferenceSection):
    """docstring for PreferenceSectionWidget"""

    _name =  ''

    def __init__(self, app_core, parent=None):
        super().__init__(parent)
        self._app_core = app_core

    def save(self):
        pass

    def name(self):
        return self._name

    def update(self):
        pass

    def _create_layout(self):
        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        layout.setFormAlignment(QtCore.Qt.AlignLeft)
        layout.setLabelAlignment(QtCore.Qt.AlignVCenter)
        layout.setVerticalSpacing(15)
        return layout

    def _add_row(self, label, field_widget, tooltip):
        self._layout.addRow(label, field_widget)
        label_widget = self._layout.labelForField(field_widget)
        label_widget.setToolTip(tooltip)
        field_widget.setToolTip(tooltip)

    def _centered_label(self, string):
        label = QtWidgets.QLabel(string)
        return label


class PreferencesItem(QtGui.QStandardItem):
    """docstring for PreferencesItem"""

    def __init__(self, title):
        super().__init__(title)
        self._widget = None

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value


class PreferencesNavigator(QtWidgets.QListView):
    preferences_widget_change = QtCore.Signal(PreferenceSectionWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)
        model = self.selectionModel()
        model.selectionChanged[
            QtCore.QItemSelection, QtCore.QItemSelection].connect(
            self.leaf_selected)

    @QtCore.Slot(QtCore.QItemSelection, QtCore.QItemSelection)
    def leaf_selected(self, selected_item, deselected_item):
        self.preferences_widget_change.emit(self._model.itemFromIndex(
            selected_item.indexes()[0]).widget)

    def _get_item(self, title, default_item):
        matches = self._model.findItems(
            title, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        if len(matches) > 0:
            return True, matches[0]
        else:
            return False, default_item

    def add_widget(self, widget):
        root_exists = False
        item = None
        name = widget.name()
        item_found, item = self._get_item(name, PreferencesItem(name))
        root = item
        root_exists = item_found

        item.widget = widget
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        if not root_exists:
            self._model.appendRow(root)
            if root is not item:
                root.setFlags(QtCore.Qt.NoItemFlags)


class PreferencesDialog(QtWidgets.QDialog):
    """docstring for PreferencesDialog"""

    def __init__(self, app_core, preference_widgets=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self._app_core = app_core
        self._preference_widgets = preference_widgets or []
        self._widgets = []
        self._imp_to_vis_widget = {}
        self._pane = None
        self._tree_widget = None
        self.setMinimumSize(QtCore.QSize(825, 425))
        self.setMaximumSize(QtCore.QSize(2000, 2000))

        self._pane = QtWidgets.QStackedWidget()
        self._pane.setMinimumSize(QtCore.QSize(600, 275))
        self._pane.setMaximumSize(QtCore.QSize(1900, 1900))
        self._tree_widget = PreferencesNavigator()
        self._tree_widget.setMinimumSize(QtCore.QSize(150, 275))
        self._tree_widget.setMaximumSize(QtCore.QSize(150, 1900))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._tree_widget)
        ok_cancel_layout = QtWidgets.QVBoxLayout()
        ok_cancel_buttons = QtWidgets.QDialogButtonBox()
        ok_cancel_buttons.addButton(QtWidgets.QDialogButtonBox.Ok)
        ok_cancel_buttons.addButton(QtWidgets.QDialogButtonBox.Cancel)
        ok_cancel_buttons.accepted.connect(self.accept)
        ok_cancel_buttons.rejected.connect(self.reject)
        ok_cancel_layout.addItem(layout)
        ok_cancel_layout.addWidget(ok_cancel_buttons)
        for widget in self._preference_widgets:
            self._add_widget(widget)
        layout.addWidget(self._pane, 1)
        self.setLayout(ok_cancel_layout)
        self._tree_widget.preferences_widget_change[
            PreferenceSectionWidget].connect(self.change_widget)
        self.accepted.connect(self.save)

    def _add_widget(self, widget):
        self._widgets.append(widget)
        container = QtWidgets.QScrollArea()
        container.setWidgetResizable(True)
        container.setWidget(widget)
        container.ensureWidgetVisible(widget)
        self._pane.addWidget(container)
        self._tree_widget.add_widget(widget)
        self._imp_to_vis_widget[widget] = container

    @QtCore.Slot(PreferenceSectionWidget)
    def change_widget(self, widget):
        self._pane.setCurrentWidget(self._imp_to_vis_widget[widget])

    @QtCore.Slot()
    def save(self):
        actions = []
        for widget in self._widgets:
            actions.extend(widget.save() or [])
        settings.instance().sync()

        # Each action_id is performed only once.
        for action_id, action in sorted(
                collections.OrderedDict(actions).items()):
            action()


class GeneralSectionWidget(PreferenceSectionWidget):
    """General settings"""

    send_stats_text = ('Help to improve Sympathy by sharing\n'
                        'anonymous statistics')

    _name = 'General'

    def __init__(self, menu_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._menu_manager = menu_manager

        settings_ = settings.instance()

        self._layout = self._create_layout()
        self._init_gui_settings(settings_)

    def _init_gui_settings(self, settings_):
        choices = ['Nothing'] + sorted(list(grid.SNAP_RESOLUTIONS.keys()))
        self._snap_type = StringComboBox('Gui/snap_type', choices)

        self._theme = StringComboBox(
            'Gui/theme', sorted(themes.available_themes().keys()))

        self._use_system_editor = BoolCheckBox('Gui/system_editor')
        self._send_stats = BoolCheckBox('send_stats')
        self._platform_developer = BoolCheckBox('Gui/platform_developer')
        self._autosave = BoolCheckBox('autosave')
        self._ask_for_save = BoolCheckBox('ask_for_save')
        self._on_start = StringComboBox('Gui/on_start', settings.on_start_choice)
        self._show_splash = BoolCheckBox('Gui/show_splash_screen')

        self._docking = StringComboBox(
            'Gui/docking_enabled', ['Detachable', 'Movable', 'Locked'])
        self._conn_shape = StringComboBox(
            'Gui/flow_connection_shape', ['Spline', 'Line'])

        self._clear_recent = QtWidgets.QPushButton('Clear recent flow list')
        self._clear_recent.setMaximumWidth(150)
        self._clear_recent.clicked.connect(self.clear_recent)

        self._layout.addRow('Snap nodes to', self._snap_type)
        if settings_['Gui/experimental']:
            self._layout.addRow('Theme (takes effect after restart)',
                                self._theme)
            self._layout.addRow('Platform developer mode',
                                self._platform_developer)
        if editor_api.can_edit_file():
            self._layout.addRow('Use system text editor',
                                self._use_system_editor)
        self._add_row(self.send_stats_text, self._send_stats,
                      'Anonymous statistics never include any identifiable '
                      'information. More information about this feature can '
                      'be found under "Data Privacy Notice" in the '
                      'documentation.')
        self._add_row('Ask about saving flows on quit/close',
                      self._ask_for_save,
                      'If checked, closing a flow with unsaved changes will '
                      'trigger a dialog asking you if you would like to save '
                      'the changes. If unchecked, the unsaved changes would '
                      'silently be discarded.')
        self._add_row('Autosave flows', self._autosave,
                      'If checked, changes to flows are automatically saved '
                      'every few seconds.')
        self._layout.addRow('Open when program starts', self._on_start)
        self._add_row('Show splash screen', self._show_splash,
                      'Show a splash screen while Sympathy is starting.')
        self._add_row('Views docking behavior', self._docking,
                      'Set the behavior of dockable views like the library '
                      'view and messages view.')

        if settings_['Gui/experimental']:
            self._layout.addRow('Connection shape', self._conn_shape)

        self._layout.addRow(self._clear_recent)
        self.setLayout(self._layout)

    def save(self):
        self._snap_type.save()
        self._use_system_editor.save()
        self._send_stats.save()
        self._platform_developer.save()
        self._ask_for_save.save()
        self._autosave.save()
        self._on_start.save()
        self._theme.save()
        self._show_splash.save()
        self._docking.save()
        self._conn_shape.save()
        return []

    def update(self):
        # Refresh in case startup changed the value after preferences dialog
        # was initialized.
        self._send_stats.update_value()

    def clear_recent(self):
        settings.instance()['Python/recent_library_path'] = []
        settings.instance()['Gui/recent_flows'] = []
        if self._menu_manager is not None:
            self._menu_manager.update_menus()


def get_recent_libs():
    settings_ = settings.instance()
    return settings_['Python/recent_library_path']


def set_recent_libs(recent_libs):
    settings_ = settings.instance()
    settings_['Python/recent_library_path'] = recent_libs[
        :num_recent_libs]


class NodeConfigsSectionWidget(PreferenceSectionWidget):
    """Node config settings"""

    _name = 'Node Configuration'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._available_themes = None

        if self._available_themes is None:
            self._available_themes = sorted(pygments.styles.get_all_styles())

        settings_ = settings.instance()
        self._layout = self._create_layout()
        self._init_gui_settings(settings_)

    def _init_gui_settings(self, settings_):
        self._code_editor_theme = StringComboBox(
            'Gui/code_editor_theme', self._available_themes)
        self._show_message_area = StringComboBox(
            'Gui/show_message_area', settings.show_message_area_choice)
        self._nodeconfig_confirm_cancel = BoolCheckBox('Gui/nodeconfig_confirm_cancel')

        self._add_row('Code editor theme', self._code_editor_theme,
                      'Set the color theme for syntax highlighting in any '
                      'code editors inside node configurations.')
        self._add_row('Show message area', self._show_message_area,
                      'Set behavior of the message area that can show up '
                      'at the top of some node configurations, for example '
                      'if the configuration is incorrect.')
        self._add_row('Confirm cancel on node configurations',
                      self._nodeconfig_confirm_cancel,
                      'If checked, closing a node configuration with unsaved '
                      'changes will trigger a dialog asking you if you would '
                      'like to save the changes. If unchecked, the unsaved '
                      'changes would silently be discarded.')
        self.setLayout(self._layout)

    def save(self):
        self._nodeconfig_confirm_cancel.save()
        self._code_editor_theme.save()
        self._show_message_area.save()
        return []


class LibrariesSectionWidget(PreferenceSectionWidget):
    """Settings concerning the node libraries"""

    library_path_changed = QtCore.Signal()

    _name =  'Node Libraries'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()
        self._layout = self._create_layout()
        self._initial_library = settings_['Python/library_path']
        self._initial_recent = get_recent_libs()
        self._path_list = PathListWidget(
            self._initial_library, root_path=settings_['install_folder'],
            recent=self._initial_recent, default_relative=False,
            parent=self)
        self._path_list.setToolTip(
            'Libraries added by path (global).\nSympathy will include these '
            'libraries among the active libraries')
        self._layout.addRow(
            self._centered_label('Libraries added by path'), self._path_list)

        self._installed_libs = QtWidgets.QListWidget(self)
        self._installed_libs.setToolTip(
            'Libraries added in to the python environment (global).\nSympathy '
            'will include these libraries among the active libraries.\n\n'
            'Can only be changed by uninstalling the packages from the python '
            'environment.')

        for entrypoint in library_platform.available_libraries(load=False):
            self._installed_libs.addItem(
                f'{entrypoint.dist} ({entrypoint.name})')

        self._layout.addRow(
            self._centered_label('Libraries added to python'), self._installed_libs)

        self.setLayout(self._layout)

    def update(self):
        settings_ = settings.instance()
        # Refresh in case library wizard added a new library.
        for path in settings_['Python/library_path']:
            if path not in self._initial_library:
                self._path_list.add_item(path)

        self._initial_library = settings_['Python/library_path']

    def save(self):
        result = []
        settings_ = settings.instance()
        new_lib_path = self._path_list.paths()
        old_lib_path = settings_['Python/library_path']

        if new_lib_path != self._initial_library:
            old_conflicts = sympathy.app.util.library_conflicts(
                sympathy.app.util.library_paths())
            settings_['Python/library_path'] = new_lib_path
            self._initial_library = new_lib_path
            new_conflicts = sympathy.app.util.library_conflicts(
                sympathy.app.util.library_paths())

            if sympathy.app.util.library_conflicts_worse(old_conflicts,
                                                         new_conflicts):
                settings_['Python/library_path'] = old_lib_path
                self._app_core.display_message(sympathy.app.util.TextMessage(
                    'Global Node Libraries',
                    warning=('Library change introduced new conflicts and was '
                             'therefore ignored. Using previous setting.')))
                return result

            set_recent_libs(self._path_list.recent())

            result.append(
                (A_LIBRARY_RELOAD,
                 self._app_core.reload_node_library))
            result.append(
                (A_LIBRARY_PATH,
                 self.library_path_changed.emit))
        self._initial_recent = get_recent_libs()
        return result


class PythonSectionWidget(PreferenceSectionWidget):
    """Settings concerning python"""

    _name =  'Python'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()
        self._layout = self._create_layout()
        self._initial_python_path = settings_['Python/python_path']
        self._path_list = PathListWidget(
            self._initial_python_path,
            root_path=settings_['install_folder'], parent=self)
        self._layout.addRow(
            self._centered_label('Python path'), self._path_list)
        self.setLayout(self._layout)

    def save(self):
        result = []
        settings_ = settings.instance()
        python_path = self._path_list.paths()

        if python_path != self._initial_python_path:
            settings_['Python/python_path'] = python_path
            self._initial_python_path = python_path
            result.append(
                (A_LIBRARY_RELOAD,
                 self._app_core.reload_node_library))
        return result


class MatlabSectionWidget(PreferenceSectionWidget):
    """Settings concerning MATLAB"""

    _name =  'Matlab'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()
        self._initial_matlab_path = settings_['MATLAB/matlab_path']
        self._initial_matlab_jvm = settings_['MATLAB/matlab_jvm']

        self._path_line = QtWidgets.QLineEdit()
        self._path_button = QtWidgets.QPushButton('...')
        self._jvm_checkbox = QtWidgets.QCheckBox()

        if len(self._initial_matlab_path):
            self._path_line.setText(self._initial_matlab_path)
        self._jvm_checkbox.setChecked(settings_['MATLAB/matlab_jvm'])

        self._layout = self._create_layout()
        path_widget = QtWidgets.QHBoxLayout()
        path_widget.addWidget(self._path_line)
        path_widget.addWidget(self._path_button)
        self._layout.addRow(
            self._centered_label('MATLAB path'), path_widget)
        self._layout.addRow('Disable JVM', self._jvm_checkbox)
        self.setLayout(self._layout)

        self._path_button.clicked.connect(self._get_path)

    def _get_path(self):
        default_directory = self._path_line.text()
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select MATLAB executable', default_directory)[0]
        if len(path):
            self._path_line.setText(path)

    def save(self):
        result = []
        settings_ = settings.instance()
        matlab_path = self._path_line.text()
        jvm = self._jvm_checkbox.isChecked()
        value_changed = False

        if matlab_path != self._initial_matlab_path:
            settings_['MATLAB/matlab_path'] = matlab_path
            self._initial_matlab_path = matlab_path
            value_changed = True
        if jvm != self._initial_matlab_jvm:
            self._initial_matlab_jvm = jvm
            settings_['MATLAB/matlab_jvm'] = jvm
            value_changed = True
        if value_changed:
            result.append(
                (A_LIBRARY_RELOAD,
                 self._app_core.reload_node_library))
        return result


class ModifyEnvironmentWidget(QtWidgets.QWidget):
    valueChanged = QtCore.Signal()
    DEFAULT_FLOW_VARIABLES = [
        'SY_FLOW_FILEPATH', 'SY_FLOW_DIR', 'SY_PARENT_FLOW_FILEPATH']

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_gui()

    def _init_gui(self):
        self._hlayout = QtWidgets.QHBoxLayout()
        self._hlayout.setContentsMargins(0, 0, 0, 0)

        self._tablewidget = QtWidgets.QTableWidget()
        self._tablewidget.setColumnCount(2)
        self._tablewidget.setHorizontalHeaderLabels(['Name', 'Value'])

        self._vlayout = QtWidgets.QVBoxLayout()
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        self._vlayout.setSpacing(5)

        self._name_lineedit = QtWidgets.QLineEdit()
        self._name_lineedit.setPlaceholderText('Name')
        self._value_lineedit = QtWidgets.QLineEdit()
        self._value_lineedit.setPlaceholderText('Value')
        self._add_button = QtWidgets.QPushButton('Add')
        self._remove_button = QtWidgets.QPushButton('Remove')

        self._hlayout.addWidget(self._name_lineedit)
        self._hlayout.addWidget(self._value_lineedit)
        self._hlayout.addWidget(self._add_button)

        self._vlayout.addLayout(self._hlayout)
        self._vlayout.addWidget(self._tablewidget)
        self._vlayout.addWidget(self._remove_button)

        self.setLayout(self._vlayout)

        self._add_button.clicked.connect(self._add_env_var)
        self._remove_button.clicked.connect(self._remove_env_var)

        self._tablewidget.itemChanged.connect(
            lambda: self.valueChanged.emit())

    def set_variables(self, variables):
        for name, value in variables.items():
            self._add(name, value)

    def variables(self):
        tw = self._tablewidget
        return {tw.item(row, 0).text(): tw.item(row, 1).text()
                for row in range(tw.rowCount())}

    def _add_env_var(self):
        name = self._name_lineedit.text()
        value = self._value_lineedit.text()
        self._add(name, value)

    def _add(self, name, value):
        row_count = self._tablewidget.rowCount()
        self._tablewidget.setRowCount(row_count + 1)

        self._tablewidget.blockSignals(True)

        name_item = QtWidgets.QTableWidgetItem(name)
        value_item = QtWidgets.QTableWidgetItem(value)
        self._tablewidget.setItem(row_count, 0, name_item)
        self._tablewidget.setItem(row_count, 1, value_item)
        if name in self.DEFAULT_FLOW_VARIABLES:
            name_item.setFlags(QtCore.Qt.NoItemFlags)
            value_item.setFlags(QtCore.Qt.NoItemFlags)

        self._tablewidget.resizeColumnsToContents()
        self._tablewidget.sortItems(0)
        self._tablewidget.blockSignals(False)

        self._tablewidget.setVerticalHeaderLabels(
            [str(i)
             for i in range(self._tablewidget.rowCount())])

        self.valueChanged.emit()

    def _remove_env_var(self):
        row = self._tablewidget.currentRow()
        remove = (
            row != -1 and
            self._tablewidget.item(row, 0).flags() != QtCore.Qt.NoItemFlags)
        if remove:
            self._tablewidget.removeRow(row)

        self.valueChanged.emit()

    def resize_to_content(self):
        self._tablewidget.resizeColumnsToContents()


class EnvironmentSectionWidget(PreferenceSectionWidget):
    """Settings concerning environment variables."""

    _name =  'Environment'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()
        self._layout = self._create_layout()

        self._global_env_widget = ModifyEnvironmentWidget()
        self._layout = self._create_layout()
        env_vars = settings_['environment']

        self._global_env_widget.set_variables(
            dict([env_var.split('=', 1) for env_var in env_vars]))
        self._global_env_widget.setMaximumHeight(300)

        self._textedit = QtWidgets.QTextEdit()
        self._tablewidget = QtWidgets.QTableWidget()
        self._tablewidget.setColumnCount(2)
        self._tablewidget.setHorizontalHeaderLabels(['Name', 'Value'])

        self._update_table(ENV.prioritized_variables())

        vlayout = QtWidgets.QGridLayout()
        vlayout.addWidget(QtWidgets.QLabel('Global environment'), 0, 0)
        vlayout.addWidget(self._global_env_widget, 0, 1)
        vlayout.addWidget(QtWidgets.QLabel('Environment variables'), 1, 0)
        vlayout.addWidget(self._tablewidget, 1, 1)
        self.setLayout(vlayout)

        self._global_env_widget.valueChanged.connect(self._update_globals)
        self._tablewidget.resizeColumnsToContents()
        self._global_env_widget.resize_to_content()

    def save(self):
        result = []
        settings_ = settings.instance()
        global_env_vars = self._global_env_widget.variables()
        values = []
        for name, value in global_env_vars.items():
            values.append('{}={}'.format(name, value))
        ENV.set_global_variables(global_env_vars)
        settings_['environment'] = values
        return result

    @QtCore.Slot(dict)
    def _update_table(self, env_variables):
        self._tablewidget.setRowCount(len(env_variables))

        for row, (name, value) in enumerate(env_variables.items()):
            name_item = QtWidgets.QTableWidgetItem(name)
            value_item = QtWidgets.QTableWidgetItem(value)
            name_item.setFlags(QtCore.Qt.NoItemFlags)
            value_item.setFlags(QtCore.Qt.NoItemFlags)
            self._tablewidget.setItem(row, 0, name_item)
            self._tablewidget.setItem(row, 1, value_item)
        self._tablewidget.sortItems(0)

    @QtCore.Slot()
    def _update_globals(self):
        global_env_vars = self._global_env_widget.variables()
        prio_env_var = copy.deepcopy(
            ENV.prioritized_variables(exclude=('global',)))

        global_env_vars.update(prio_env_var)
        self._update_table(global_env_vars)
        self._global_env_widget.resize_to_content()
        self._tablewidget.resizeColumnsToContents()


class DebugSectionWidget(PreferenceSectionWidget):
    """Settings concerning debugging and profiling."""

    profile_path_types = ['Session folder', 'Workflow folder']

    _name =  'Debug'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dot_in_path = distutils.spawn.find_executable(vs.str_('dot'))

        def graphviz_path_dialog():
            default_directory = self._graphviz_path.text()
            dir_ = QtWidgets.QFileDialog.getExistingDirectory(
                self, 'Locate Graphviz directory containing dot',
                default_directory)
            if dir_:
                self._graphviz_path.setText(dir_)
                test_graphviz_path()

        def test_graphviz_path():
            gviz_path = self._graphviz_path.text()
            dot = distutils.spawn.find_executable(vs.str_('dot'), gviz_path)
            if dot:
                self._graphviz_status.setText("Graphviz found!")
                self._graphviz_status.setStyleSheet("QLabel { color: green; }")
            elif self._dot_in_path:
                self._graphviz_status.setText("Graphviz found in PATH!")
                self._graphviz_status.setStyleSheet("QLabel { color: green; }")
            else:
                self._graphviz_status.setText("Graphviz not found!")
                self._graphviz_status.setStyleSheet("QLabel { color: red; }")

        settings_ = settings.instance()
        path_type = settings_['Debug/profile_path_type']
        graphviz_path = settings_['Debug/graphviz_path']

        self._profile_path_type = QtWidgets.QComboBox()
        self._profile_path_type.addItems(self.profile_path_types)
        self._profile_path_type.setCurrentIndex(
            self._profile_path_type.findText(path_type))

        gviz_path_layout = QtWidgets.QHBoxLayout()
        self._graphviz_path = QtWidgets.QLineEdit(graphviz_path)
        file_button = QtWidgets.QPushButton('...')
        gviz_path_layout.addWidget(self._graphviz_path)
        gviz_path_layout.addWidget(file_button)

        self._graphviz_status = QtWidgets.QLabel()

        self._layout = self._create_layout()
        self._layout.addRow('Store profiling data in', self._profile_path_type)
        self._layout.addRow(
            self._centered_label('Graphviz install path'),
            gviz_path_layout)
        self._layout.addRow('', self._graphviz_status)
        self.setLayout(self._layout)

        self._graphviz_path.textEdited.connect(test_graphviz_path)
        file_button.clicked.connect(graphviz_path_dialog)

        test_graphviz_path()

    def save(self):
        settings_ = settings.instance()
        settings_[
            'Debug/profile_path_type'] = self._profile_path_type.currentText()
        settings_['Debug/graphviz_path'] = self._graphviz_path.text()


class TempFilesSectionWidget(PreferenceSectionWidget):
    """Temporary session files settings"""

    _name = 'Temporary Files'
    _apply_order = 10000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()
        self._layout = self._create_layout()
        self._init_sessions_folder(settings_)

    def _init_sessions_folder(self, settings_):
        self._path_layout = QtWidgets.QHBoxLayout()
        sessions_folder = settings_['temp_folder']
        self._original_sessions_folder = sessions_folder
        self._sessions_folder = QtWidgets.QLineEdit(sessions_folder)

        self._path_layout.addWidget(self._sessions_folder)

        self._file_button = QtWidgets.QPushButton('...')
        self._file_button.clicked.connect(self._open_sessions_folder_dialog)
        self._path_layout.addWidget(self._file_button)

        if settings_.sessions_folder_override:
            self._file_button.setDisabled(True)
            self._sessions_folder.setDisabled(True)
            self._sessions_folder.setToolTip(
                settings_.sessions_folder_override_description)

        self._layout.addRow(
            self._centered_label('Temporary files path'),
            self._path_layout)

        self._session_files = QtWidgets.QComboBox()
        self._session_files.addItems(settings.session_temp_files_choice)
        self._session_files.setCurrentIndex(self._session_files.findText(
            settings_.session_temp_files))

        self._layout.addRow(
            'Handling of session files',
            self._session_files)

        limits_group = QtWidgets.QGroupBox()
        limits_layout = self._create_layout()

        self._temp_age = QtWidgets.QSpinBox()
        self._temp_age.setMaximum(999999)
        self._temp_age.setValue(settings_['max_temp_folder_age'])
        limits_layout.addRow(
            'Age of temporary files (days)', self._temp_age)

        self._temp_size = QtWidgets.QLineEdit()
        self._temp_size.setText(settings_['max_temp_folder_size'])
        self._temp_size.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._temp_size.setMaximumSize(QtCore.QSize(70, 25))
        limits_layout.addRow(
            'Size of temporary files (x k/M/G)', self._temp_size)

        self._temp_number = QtWidgets.QSpinBox()
        self._temp_number.setMaximum(999999)
        self._temp_number.setValue(settings_['max_temp_folder_number'])
        limits_layout.addRow(
            'Number of session folders',
            self._temp_number)
        self._session_files.currentIndexChanged.connect(
            limits_group.setDisabled)

        limits_group.setLayout(limits_layout)
        self._layout.addRow('Limits for keeping session files', limits_group)
        limits_group.setDisabled(self._session_files.currentIndex())

        self.setLayout(self._layout)

    @QtCore.Slot()
    def _open_sessions_folder_dialog(self):
        default_directory = self._sessions_folder.text()
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Locate a directory for temporary files',
            default_directory)
        if len(dir_) > 0:
            self._sessions_folder.setText(dir_)

    def save(self):
        settings_ = settings.instance()

        if self._original_sessions_folder != self._sessions_folder.text():
            settings_['temp_folder'] = str(self._sessions_folder.text())
        else:
            settings_['temp_folder'] = self._sessions_folder.text()

        settings_.session_temp_files = self._session_files.currentText()

        settings_['max_temp_folder_age'] = int(self._temp_age.text())
        settings_['max_temp_folder_number'] = self._temp_number.value()
        settings_['max_temp_folder_size'] = self._temp_size.text()


class AdvancedSectionWidget(PreferenceSectionWidget):
    """Advanced settings"""

    _name =  'Advanced'
    _apply_order = 10000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = self._create_layout()
        settings_ = settings.instance()

        self._nbr_of_threads = QtWidgets.QSpinBox()
        self._nbr_of_threads.setMaximum(999)
        self._nbr_of_threads.setValue(settings_['max_nbr_of_threads'])

        self._char_limit = QtWidgets.QSpinBox()
        self._char_limit.setMaximum(2**31 - 1)  # Max 32 bit signed int.
        self._char_limit.setValue(settings_['max_task_chars'])

        self._deprecated_warning = QtWidgets.QCheckBox()
        self._deprecated_warning.setChecked(settings_['deprecated_warning'])

        self._clear_settings = QtWidgets.QCheckBox()
        self._clear_settings.setChecked(settings_.get('clear_settings', False))
        self._clear_caches = QtWidgets.QCheckBox()
        self._clear_caches.setChecked(settings_.get('clear_caches', False))

        self._show_experimental = QtWidgets.QCheckBox()
        self._show_experimental.setChecked(settings_['Gui/experimental'])

        clear_layout = QtWidgets.QGridLayout()
        clear_layout.addWidget(QtWidgets.QLabel('Caches'), 0, 0)
        clear_layout.addWidget(self._clear_caches, 1, 0,
                               QtCore.Qt.AlignHCenter)
        clear_layout.addWidget(QtWidgets.QLabel('Settings'), 0, 1)
        clear_layout.addWidget(
            self._clear_settings, 1, 1, QtCore.Qt.AlignHCenter)
        clear_layout.setHorizontalSpacing(10)
        clear_layout.setVerticalSpacing(2)

        self._layout.addRow(
            'Number of worker processes (0 = automatic)\n'
            'Sympathy has to be restarted to apply this setting.',
            self._nbr_of_threads)

        self._layout.addRow(
            'Node output character limit (0 = unlimited)',
            self._char_limit)

        self._layout.addRow(
            'Display warnings for deprecated nodes',
            self._deprecated_warning)
        self._layout.addRow(
            'Reset on next close:\n'
            'CAUTION! This may affect all open instances of Sympathy',
            clear_layout)
        self._layout.addRow(
            'Show experimental options\n'
            'Sympathy has to be restarted to apply this setting',
            self._show_experimental)

        self.setLayout(self._layout)

    def save(self):
        settings_ = settings.instance()
        settings_['max_nbr_of_threads'] = self._nbr_of_threads.value()
        settings_['deprecated_warning'] = self._deprecated_warning.isChecked()
        settings_['clear_settings'] = self._clear_settings.isChecked()
        settings_['clear_caches'] = self._clear_caches.isChecked()
        settings_['max_task_chars'] = self._char_limit.value()
        settings_['Gui/experimental'] = self._show_experimental.isChecked()


class LibraryViewSectionWidget(PreferenceSectionWidget):
    """Library view settings"""

    library_separated_changed = QtCore.Signal(bool)
    library_show_hidden_changed = QtCore.Signal()
    library_highlighter_changed = QtCore.Signal(tuple)

    _name =  'Library View'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_ = settings.instance()

        self._layout = self._create_layout()
        self._init_gui_settings(settings_)

    def _init_gui_settings(self, settings_):
        self._library_separated = QtWidgets.QCheckBox()
        self._library_separated.setChecked(settings_['Gui/library_separated'])

        self._show_hidden = QtWidgets.QCheckBox()
        self._show_hidden.setChecked(settings_['Gui/library_show_hidden'])

        self._library_matcher_type = QtWidgets.QComboBox()
        choices = ['character', 'word']
        self._library_matcher_type.addItems(choices)
        self._library_matcher_type.setCurrentIndex(choices.index(
            settings_['Gui/library_matcher_type']))

        self._library_highlighter_type = QtWidgets.QComboBox()
        choices = ['color', 'background-color', 'font-weight']
        self._library_highlighter_type.addItems(choices)
        self._library_highlighter_type.setCurrentIndex(choices.index(
            settings_['Gui/library_highlighter_type']))

        self._library_highlighter_color = QtWidgets.QLineEdit()
        self._library_highlighter_color.setText(
            settings_['Gui/library_highlighter_color'].upper())
        self._library_highlighter_color.setFixedWidth(100)

        self._color_button = QtWidgets.QPushButton('...')
        self._color_button.clicked.connect(self._set_color)

        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(self._library_highlighter_color)
        color_layout.addWidget(self._color_button)
        self._color_button.setFixedWidth(55)

        self._quickview_popup_position = QtWidgets.QComboBox()
        choices = ['left', 'center', 'right']
        self._quickview_popup_position.addItems(choices)
        self._quickview_popup_position.setCurrentIndex(choices.index(
            settings_['Gui/quickview_popup_position']))

        self._layout.addRow(
            'Separate each node library', self._library_separated)
        self._layout.addRow('Show hidden nodes', self._show_hidden)

        if settings_['Gui/experimental']:
            self._layout.addRow('Highlighter', self._library_matcher_type)
            self._layout.addRow(
                'Highlighter type', self._library_highlighter_type)
            self._layout.addRow('Highlighter color', color_layout)
        self._layout.addRow('Popup position', self._quickview_popup_position)

        self.setLayout(self._layout)

        self._library_highlighter_type.currentIndexChanged.connect(
            self._disable_colorfield)
        self._disable_colorfield()

    def _disable_colorfield(self):
        if self._library_highlighter_type.currentText() == 'font-weight':
            self._library_highlighter_color.setDisabled(True)
            self._color_button.setDisabled(True)
        else:
            self._library_highlighter_color.setDisabled(False)
            self._color_button.setDisabled(False)

    def _set_color(self):
        picker = QtWidgets.QColorDialog()
        res = picker.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self._library_highlighter_color.setText(
                picker.currentColor().name().upper())

    def save(self):
        result = []
        settings_ = settings.instance()

        separated = self._library_separated.isChecked()
        separated_prev = settings_['Gui/library_separated']
        settings_['Gui/library_separated'] = separated
        if separated_prev != separated:
            result.append(
                (A_LIBRARY_TYPE,
                 lambda:
                 self.library_separated_changed.emit(separated)))
        show_hidden = self._show_hidden.isChecked()
        show_hidden_prev = settings_['Gui/library_show_hidden']
        settings_['Gui/library_show_hidden'] = show_hidden
        if show_hidden_prev != show_hidden:
            result.append(
                (A_LIBRARY_TYPE,
                 lambda: self.library_show_hidden_changed.emit()))

        lib_highlighter_type = self._library_highlighter_type.currentText()
        lib_highlighter_type_prev = settings_['Gui/library_highlighter_type']
        settings_['Gui/library_highlighter_type'] = lib_highlighter_type

        lib_highlighter_color = self._library_highlighter_color.text()
        lib_highlighter_color_prev = settings_[
            'Gui/library_highlighter_color']
        settings_['Gui/library_highlighter_color'] = lib_highlighter_color

        lib_matcher_type = self._library_matcher_type.currentText()
        lib_matcher_type_prev = settings_['Gui/library_matcher_type']
        settings_['Gui/library_matcher_type'] = lib_matcher_type

        if (lib_highlighter_type_prev != lib_highlighter_type or
                lib_highlighter_color_prev != lib_highlighter_color or
                lib_matcher_type_prev != lib_matcher_type):
            result.append(
                (A_LIBRARY_HIGHLIGHTER,
                 lambda: self.library_highlighter_changed.emit((
                     lib_matcher_type,
                     lib_highlighter_type,
                     lib_highlighter_color
                 ))))

        quickview_popup_pos = self._quickview_popup_position.currentText()
        settings_['Gui/quickview_popup_position'] = quickview_popup_pos

        return result
