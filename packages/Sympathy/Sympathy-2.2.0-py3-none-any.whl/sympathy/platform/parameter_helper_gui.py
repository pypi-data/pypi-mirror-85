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
import os
import json
import datetime
import contextlib
from collections.abc import Iterable

from sympathy.platform import qt_compat2
from sympathy.platform import widget_library as sywidgets
from sympathy.platform import settings
from sympathy.platform import parameter_helper_visitors as visitors
from sympathy.platform import parameter_helper as models
from sympathy.platform.exceptions import sywarn
from sympathy.platform.editors import table_editor
from sympathy.utils import prim
from sympathy.utils import search
from sympathy.utils.context import original, is_original

import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtWidgets as QtWidgets

# QtCore = qt_compat2.QtCore
# QtGui = qt_compat2.import_module('QtGui')


def get_default_path(old_path, flow_dir):
    if old_path and os.path.exists(old_path):
        return old_path
    elif flow_dir:
        return flow_dir
    return settings.get_default_dir()


def _warn_missing_editor(param_type, editor_type):
    return (
        f'There is no suitable {editor_type} editor for {param_type} '
        'parameter.')


class _ParameterContext(object):
    """Mock NodeContext used for validation of generated GUIs."""

    def __init__(self, params):
        self._params = params
        self._objects = {}
        self._own_objects = {}

    @property
    def definition(self):
        return {'ports': {'inputs': [], 'outputs': []}}

    @property
    def typealiases(self):
        return {}

    @property
    def parameters(self):
        return self._params

    @property
    def input(self):
        return []

    @property
    def output(self):
        return []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class ParameterView(QtWidgets.QWidget):
    """
    Base class for generated and custom GUIs.
    Custom GUIs signal status changed that can trigger an update
    of status and messages. This can prevent accepting invalid
    configurations and enables interactive feedback in a standardized way.
    """

    status_changed = qt_compat2.Signal()

    def __init__(self, params=None, validator=None, parent=None):
        self._params = params
        self._validator = validator
        self._original_validator = True
        self._original_status = is_original(type(self).status.fget)
        super().__init__(parent)

    @property
    @original
    def status(self):
        """
        For custom GUIs that have custom parameter handling:
        override this property to include the current status message.

        Return status message string.
        """
        return ''

    @property
    def valid(self):
        """
        For custom GUIs that have custom parameter handling:
        override this property to reflect if the configuration is valid.

        Return True if the view is valid and False otherwise.
        """
        if self._validator:
            return self._validator(_ParameterContext(self._params))
        # Returning True for compatiblility with old custom_parameters.
        return True

    def save_parameters(self):
        """
        For custom GUIs that have custom parameter handling:
        override this method to update parameters just before the widget is
        accepted.
        """

    def cleanup(self):
        """
        For custom GUIs that need custom cleanup:
        override this method to perform cleanup just before the widget is
        closed.
        """

    def has_preview(self):
        """
        Return True if configuration has a preview and False otherwise.
        """
        return False

    def has_status(self):
        """
        Return True if view might change status and use the message area
        and False otherwise.
        """
        return not self._original_status

    def preview_active(self):
        """
        Return True if configuration has an active preview and False otherwise.
        """
        return False

    def set_preview_active(self, value):
        """
        Activate preview, for widgets where has_preview() == True.
        """


class ClampedButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        font = self.font()
        fm = QtGui.QFontMetrics(font)
        rect = fm.boundingRect(text)
        self.setMaximumWidth(rect.width() + 32)

        # For OSX this is the minimum size allowed for a button with rounded
        # corners.
        if prim.is_osx():
            self.setMinimumWidth(50)
            self.setMinimumHeight(30)


class ParameterWidget(QtWidgets.QWidget):
    def __init__(self, parameter_value, editor=None, parent=None):
        super().__init__(parent)
        self._parameter_value = parameter_value
        self._editor = editor

        # If the editor is Expanding, then the containing widget should be too.
        if editor is not None:
            editor_policy = editor.sizePolicy()
            policy = self.sizePolicy()
            policy.setVerticalPolicy(editor_policy.verticalPolicy())
            self.setSizePolicy(policy)

    @qt_compat2.Slot(bool)
    def set_visible(self, value):
        self.setVisible(value)
        self._editor.setVisible(value)

    @qt_compat2.Slot(bool)
    def set_enabled(self, value):
        self.setEnabled(value)
        self._editor.setEnabled(value)

    @qt_compat2.Slot(bool)
    def set_disabled(self, value):
        self.setDisabled(value)
        self._editor.setDisabled(value)

    def editor(self):
        return self._editor

    def set_value(self, value):
        self._editor.set_value(value)


class NullParameterWidget(object):
    def add_group(self, widget):
        pass

    def add_page(self, widget, label):
        pass

    def add_widget(self, widget):
        pass


class ParameterBaseValueWidget(ParameterWidget):
    def __init__(self, parameter_value, editor, parent=None):
        if editor is None:
            editor = ParameterEditorTextLineWidget(parameter_value, {})
        super().__init__(parameter_value, editor, parent)
        self._value_label = None

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        if self._parameter_value.label:
            self._value_label = QtWidgets.QLabel(self._parameter_value.label)
            hlayout.addWidget(self._value_label)
            hlayout.addItem(QtWidgets.QSpacerItem(10, 1))
            self._value_label.setToolTip(self._parameter_value.description)
        if self._parameter_value.description:
            self._editor.setToolTip(self._parameter_value.description)
            self.setToolTip(self._parameter_value.description)
        hlayout.addWidget(self._editor)
        self.setLayout(hlayout)

        self._init_gui_from_parameters()
        assert(self.editor() is not None)

    def _init_gui_from_parameters(self):
        self._editor.set_value(self._parameter_value.value)

    def label_widget(self):
        return self._value_label

    @qt_compat2.Slot(bool)
    def set_visible(self, value):
        super().set_visible(value)
        self.label_widget().setVisible(value)

    @qt_compat2.Slot(bool)
    def set_enabled(self, value):
        super().set_enabled(value)
        self.label_widget().setEnabled(value)

    @qt_compat2.Slot(bool)
    def set_disabled(self, value):
        super().set_disabled(value)
        self.label_widget().setDisabled(value)


class ParameterValueWidget(ParameterBaseValueWidget):
    def __init__(self, parameter_value, editor, parent=None):
        super().__init__(parameter_value, editor, parent)

        self._editor.valueChanged[str].connect(self._text_changed)

    def label_widget(self):
        return self._value_label

    def _text_changed(self, text):
        raise NotImplementedError(
            "Override when extending!")


class ParameterNumericValueWidget(ParameterWidget):
    def __init__(self, parameter_value, editor=None, parent=None):
        if editor is None:
            editor = lineedit_editor_factory({}, parameter_value)
        super().__init__(parameter_value, editor, parent)
        self._value_label = None
        self._layout = None
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        if self._parameter_value.label:
            self._value_label = QtWidgets.QLabel(self._parameter_value.label)
            self._layout.addWidget(self._value_label)
            self._layout.addItem(QtWidgets.QSpacerItem(10, 1))
        if self._parameter_value.description:
            self._value_label.setToolTip(self._parameter_value.description)
            self._editor.setToolTip(self._parameter_value.description)
            self.setToolTip(self._parameter_value.description)

        self._layout.addWidget(self._editor)

        vlayout.addItem(self._layout)
        self.setLayout(vlayout)

        self._init_gui_from_parameters()

    def _init_gui_from_parameters(self):
        self._editor.set_value(self._parameter_value.value)

    def label_widget(self):
        return self._value_label


class ParameterStringWidget(ParameterValueWidget):
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, parameter_value, editor=None, parent=None):
        super().__init__(parameter_value, editor, parent)

    def _text_changed(self, text):
        self._parameter_value.value = str(text)
        self.valueChanged.emit(str(text))


class ParameterBooleanWidget(ParameterWidget):
    stateChanged = qt_compat2.Signal(int)
    valueChanged = qt_compat2.Signal(bool)

    def __init__(self, parameter_value, editor=None, parent=None):
        if editor:
            # TODO(erik): make it possible to choose editor.
            self._avoid_gc_issues_with_ignored_editor = editor
            sywarn('ParameterBooleanWidget does not currently support '
                   'editor argument.')

        # TODO: ParameterBooleanWidget has a checkbox, not a proper editor
        # (different interface).
        editor = QtWidgets.QCheckBox()
        super().__init__(parameter_value, editor=editor, parent=parent)
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        if self._parameter_value.label:
            self._editor.setText(self._parameter_value.label)
        if self._parameter_value.description:
            self._editor.setToolTip(
                self._parameter_value.description)
        vlayout.addWidget(self._editor)
        self.setLayout(vlayout)

        self._init_gui_from_parameters()

        self._editor.stateChanged[int].connect(self._state_changed)
        assert(self._editor is not None)

    def _init_gui_from_parameters(self):
        self.set_value(self._parameter_value.value)

    def set_value(self, value):
        try:
            self._editor.setChecked(value)
        except Exception:
            self._editor.setChecked(QtCore.Qt.Unchecked)

    def _state_changed(self, state):
        self._parameter_value.value = state > 0
        self.stateChanged.emit(state)
        self.valueChanged.emit(state > 0)


class ParameterDateTimeWidget(ParameterBaseValueWidget):
    valueChanged = qt_compat2.Signal(datetime.datetime)

    def __init__(self, parameter_value, editor=None, parent=None):
        if editor is None:
            editor = ParameterEditorDateTimeWidget(
                parameter_value, {})

        super().__init__(parameter_value, editor, parent)
        editor.valueChanged.connect(self._datetime_changed)

    def _init_gui_from_parameters(self):
        dt = self._parameter_value.value
        # Initialized using constructor.
        # self._editor.setValue(dt)

    def _datetime_changed(self, value):
        self._parameter_value.value = value
        self.valueChanged.emit(value)


class ParameterEditorWidget(QtWidgets.QWidget):
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, parameter_list, editor_dict, customization=None,
                 parent=None):
        super().__init__(parent)
        self._customization = customization or {}
        self._parameter_list = parameter_list
        self._editor_dict = editor_dict
        self._init_customizations()

    def _init_customizations(self):
        for key in self._customization:
            try:
                self._customization[key] = self._editor_dict[key]
            except KeyError:
                pass

    @property
    def parameter_model(self):
        return self._parameter_list


class ParameterEditorDateTimeWidget(ParameterEditorWidget):
    valueChanged = qt_compat2.Signal(datetime.datetime)

    def __init__(self, parameter_value, editor_dict, parent=None):
        customization = {'datetime_format': None}

        super().__init__(
            parameter_value, editor_dict, customization, parent=parent)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        widget = sywidgets.DateTimeWidget(
            parameter_value.value,
            datetime_format=self._customization['datetime_format'])
        self._widget = widget
        widget.valueChanged.connect(self.valueChanged)
        self._layout.addWidget(widget)
        self.setLayout(self._layout)

    def set_value(self, value):
        self._widget.setValue(value)


class ParameterEditorTextLineWidget(ParameterEditorWidget):
    def __init__(self, parameter_value, editor_dict, parent=None):
        customization = {'placeholder': ''}

        super().__init__(
            parameter_value, editor_dict, customization, parent=parent)
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        if self._parameter_list.type == 'float':
            line_edit = sywidgets.ValidatedFloatLineEdit()
            line_edit.valueChanged[float].connect(
                self._value_changed)
        elif self._parameter_list.type == 'integer':
            line_edit = sywidgets.ValidatedIntLineEdit()
            line_edit.valueChanged[int].connect(
                self._value_changed)
        else:
            line_edit = sywidgets.ValidatedTextLineEdit()
            line_edit.valueChanged[str].connect(
                self._value_changed)

        self._value_lineedit = line_edit
        self._layout.addWidget(self._value_lineedit)
        self.setLayout(self._layout)

        self._init_gui_from_parameters()

    def _init_gui_from_parameters(self):
        self._value_lineedit.setPlaceholderText(
            self._customization['placeholder'])

    def set_value(self, value):
        self._value_lineedit.setText(str(value))

    def set_builder(self, builder):
        return self._value_lineedit.setBuilder(builder)

    def _value_changed(self, value):
        if self._parameter_list.type == 'float':
            try:
                self._parameter_list.value = float(value)
            except ValueError:
                self._parameter_list.value = 0.0
        elif self._parameter_list.type == 'integer':
            try:
                self._parameter_list.value = int(value)
            except ValueError:
                self._parameter_list.value = 0
        elif self._parameter_list.type == 'string':
            self._parameter_list.value = value
        elif self._parameter_list.type == 'dict':
            self._parameter_list.value = value
        else:
            raise Exception("Unknown parameter type")
        self.valueChanged.emit(self._parameter_list.value)


class ParameterEditorTextAreaWidget(ParameterEditorWidget):
    def __init__(self, parameter_value, editor_dict, parent=None):
        customization = {}

        super().__init__(
            parameter_value, editor_dict, customization,
            parent=parent)
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._value_lineedit = sywidgets.SyTextEdit()
        self._layout.addWidget(self._value_lineedit)
        self.setLayout(self._layout)

        # This editor can make use of any extra space it gets.
        policy = self.sizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(policy)

        self._value_lineedit.textChanged.connect(self._value_changed)

    def set_value(self, value):
        self._value_lineedit.setText(str(value))

    def _value_changed(self):
        self._parameter_list.value = self._value_lineedit.toPlainText()
        self.valueChanged.emit(self._parameter_list.value)


class ParameterEditorCodeEditWidget(ParameterEditorWidget):
    def __init__(self, parameter_value, editor_dict, parent=None):
        customization = {'language': 'python'}

        super().__init__(
            parameter_value, editor_dict, customization,
            parent=parent)
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._value_lineedit = sywidgets.CodeEdit(
            self._customization['language'])
        self._layout.addWidget(self._value_lineedit)
        self.setLayout(self._layout)

        # This editor can make use of any extra space it gets.
        policy = self.sizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(policy)

        self._value_lineedit.textChanged.connect(self._value_changed)

    def set_value(self, value):
        self._value_lineedit.setPlainText(str(value))

    def _value_changed(self):
        self._parameter_list.value = self._value_lineedit.toPlainText()
        self.valueChanged.emit(self._parameter_list.value)


class ParameterEditorSpinBoxWidget(ParameterEditorWidget):
    def __init__(self, parameter_value, editor_dict, customization,
                 value_spinbox, parent=None):
        self._value_spinbox = value_spinbox
        super().__init__(
            parameter_value, editor_dict, customization, parent)
        # The following must be true in order to execute.
        assert(hasattr(self, '_value_spinbox'))
        assert(self._value_spinbox is not None)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        vlayout.addWidget(self._value_spinbox)
        self.setLayout(vlayout)

        self._init_gui_from_parameters()

    def set_value(self, value):
        """Give the spinbox a new value."""
        self._value_spinbox.setValue(value)

    def set_range(self, minimum, maximum):
        """Set the minimum and maximum values."""
        self._value_spinbox.setRange(minimum, maximum)

    def _init_gui_from_parameters(self):
        self._value_spinbox.setMaximum(self._customization['max'])
        self._value_spinbox.setMinimum(self._customization['min'])
        self._value_spinbox.setSingleStep(self._customization['step'])


class ParameterEditorIntegerWidget(ParameterEditorSpinBoxWidget):
    valueChanged = qt_compat2.Signal(int)

    def __init__(self, parameter_value, editor_dict, spin_buttons=False,
                 parent=None):
        customization = {
            'max': 100,
            'min': 0,
            'step': 1} if spin_buttons else {
                'max': None,
                'min': None,
                'step': 1}
        value_spinbox = sywidgets.ValidatedIntSpinBox()
        if not spin_buttons:
            value_spinbox.setButtonSymbols(
                QtWidgets.QAbstractSpinBox.NoButtons)

        super().__init__(
            parameter_value, editor_dict, customization, value_spinbox, parent)
        self._value_spinbox.valueChanged[int].connect(
            self._value_changed)

    @qt_compat2.Slot(int)
    def _value_changed(self, value):
        self._parameter_list.value = value
        self.valueChanged.emit(value)


class ParameterEditorFloatWidget(ParameterEditorSpinBoxWidget):
    valueChanged = qt_compat2.Signal(float)

    def __init__(self, parameter_value, editor_dict, spin_buttons=False,
                 parent=None):
        customization = {
            'max': 100.0,
            'min': 0.0,
            'step': 1.0} if spin_buttons else {
                'max': None,
                'min': None,
                'step': 1.0}
        customization['decimals'] = 2

        value_spinbox = sywidgets.ValidatedFloatSpinBox()
        if not spin_buttons:
            value_spinbox.setButtonSymbols(
                QtWidgets.QAbstractSpinBox.NoButtons)

        super().__init__(
            parameter_value, editor_dict, customization, value_spinbox, parent)
        self._value_spinbox.valueChanged[float].connect(
            self._value_changed)
        self._init_gui_from_parameters()

    def _init_gui_from_parameters(self):
        self._value_spinbox.setDecimals(self._customization['decimals'])
        super()._init_gui_from_parameters()

    @qt_compat2.Slot(float)
    def _value_changed(self, value):
        self._parameter_list.value = value
        self.valueChanged.emit(value)


class FileSystemModel(QtWidgets.QFileSystemModel):

    def __init__(self, parent):
        super().__init__(parent)


class ParameterPath(object):
    def __init__(self, parameter_string):
        self._parameter = parameter_string

        # All paths should be stored in unipath_separators format. If it isn't,
        # we update it:
        self._parameter.value = prim.unipath_separators(self._parameter.value)

    @property
    def value(self):
        return prim.nativepath_separators(self._parameter.value)

    @value.setter
    def value(self, value):
        self._parameter.value = prim.unipath_separators(value)


class ParameterEditorFileDialogWidget(ParameterEditorTextLineWidget):
    dialogChanged = qt_compat2.Signal(str)
    state_changed = qt_compat2.Signal(bool)
    text_changed = qt_compat2.Signal()

    _abs = ('abs', 'Absolute path')
    _abs_key = _abs[0]
    _rel = ('top', 'Relative to top-flow')
    _rel_key = _rel[0]
    _flo = ('sub', 'Relative to sub-flow')
    _lib = ('lib', 'Relative to library root')

    _flow_dir = '$(SY_FLOW_DIR)'
    _lib_dir = '$(SY_LIBRARY_DIR)'

    _old_states = {
        # Keep support for specifying old 'rel' state:
        'rel': _rel_key
    }
    _env_states = {
        _flo: {'state_key': 'node/flow_dir', 'env_var': _flow_dir},
        _lib: {'state_key': 'node/lib_dir', 'env_var': _lib_dir},
    }

    def __init__(self, parameter_string, editor_dict, parent=None):
        customization = {
            'placeholder': '',
            'states': None,
        }
        # specifically don't call the direct super class to be able to
        # override the __init_gui() call
        self._env_values = {}
        self._parameter_path = ParameterPath(parameter_string)
        ParameterEditorWidget.__init__(self, self._parameter_path, editor_dict,
                                       customization, parent)

        for k, v in self._env_states.items():
            try:
                self._env_values[k] = prim.unipath(
                    parameter_string._state_settings[v['state_key']])
            except KeyError:
                pass

        self._env_states = {k: self._env_states[k] for k in self._env_values}
        self._flow_dir_value = self._env_values[self._flo]

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        value = self._parameter_path.value

        # Customization
        self._rel_dir_value = os.getcwd()
        self._states = []
        if self._customization['states'] is None:
            self._states = [self._abs, self._rel] + list(
                self._env_states.keys())
        else:
            has_rel_state = False
            for state in self._customization['states']:
                state = self._old_states.get(state, state)
                env_state = self._env_state_from_key(state)

                if env_state:
                    self._states.append(env_state)
                elif state == self._abs_key:
                    self._states.append(self._abs)
                elif state == self._rel_key:
                    if has_rel_state:
                        raise ValueError("Only one relative state is allowed.")
                    has_rel_state = True
                    self._states.append(self._rel)
                elif isinstance(state, str):
                    raise ValueError(
                        "Only these states are allowed as bare strings: "
                        "{}".format([
                            self._abs_key,
                            self._rel_key,
                            self._flo[0],
                            self._lib[0],
                        ]))
                else:
                    if has_rel_state:
                        raise ValueError("Only one relative state is allowed.")
                    if not os.path.isabs(state[2]):
                        raise ValueError(
                            "Need an absolute path as root for "
                            "relative state '{}'.".format(state[0]))
                    has_rel_state = True
                    self._states.append(state[:2])
                    self._rel = state[:2]
                    self._rel_dir_value = state[2]
        for state in list(self._states):
            if state in self._env_states and state not in self._env_values:
                self._states.remove(state)

        # Initial state and value
        text = value
        env_state = self._env_state_from_value(value)

        if env_state:
            self._state = env_state
            text = self._env_state_text(env_state, value)
        else:
            if os.path.isabs(value):
                self._state = self._abs
            else:
                self._state = self._rel
        # At this point self._state can possibly be a state not included in
        # states. We fix this as soon as the lineedit widget and completer have
        # been set up.

        self._value_lineedit = sywidgets.MenuLineEdit(
            options=self._states, value=self._state, parent=self)
        self._text = text
        self._value_lineedit.setText(text)

        self._layout.addWidget(self._value_lineedit)
        self.setLayout(self._layout)

        self._value_lineedit.prefix_button.setToolTip(
            'Toggle between relative and absolute path.')

        self._dialog_button = ClampedButton('\u2026')
        self._layout.addWidget(self._dialog_button)

        completer = QtWidgets.QCompleter(self)
        self._completer_model = FileSystemModel(completer)
        completer.setModel(self._completer_model)
        self._value_lineedit.setCompleter(completer)
        self._completer_model.setRootPath(
            os.path.abspath(self._abs_path(self._get_text())))

        # Now we can fix the possible problem of self._state not being one of
        # the available states.
        if self._state not in self._states:
            if self._abs in self._states:
                # Defaulting to absolute path feels natural if it is available
                self._state_edited(self._abs)
            else:
                # otherwise default to whatever is available
                self._state_edited(self._states[0])

        self._dialog_button.clicked.connect(self._dialog_click)
        self.dialogChanged.connect(self._filename_changed_from_dialog)

        self._value_lineedit.state_edited.connect(self._state_edited)
        self._value_lineedit.textEdited.connect(self._text_edited)
        completer.activated.connect(self._text_edited)

    def filename(self):
        return self._abs_path(self._get_text())

    def _abs_path(self, text):
        if self._state in self._env_states:
            value = self._env_values[self._state]
            return os.path.normpath(os.path.join(value, text))
        elif self._state == self._rel:
            return os.path.normpath(os.path.join(self._rel_dir_value, text))
        return text

    def _rel_cwd_path(self, text):
        abs_path = self._abs_path(text)
        try:
            return os.path.relpath(abs_path, self._rel_dir_value), self._rel
        except Exception:
            return abs_path, self._abs

    def _rel_env_path(self, text, state):
        abs_path = self._abs_path(text)
        try:
            value = self._env_values[state]
            return os.path.relpath(abs_path, value), state
        except Exception:
            return abs_path, self._abs

    def _get_text(self):
        """Return the current text from the gui."""
        return self._value_lineedit.text()

    def _get_state(self):
        """Return the current state from the gui."""
        return self._value_lineedit.current_value

    def _set_text(self, value):
        """Set the text in the gui."""
        self._value_lineedit.setText(value)

    def _set_state(self, value):
        """Set the state in the gui."""
        self._value_lineedit.current_value = value

    def _env_state_from_value(self, value):
        for k, v in self._env_states.items():
            var = v['env_var']
            if value.startswith(var):
                return k

    def _env_state_from_key(self, key):
        for k, v in self._env_states.items():
            if k[0] == key:
                return k

    def _env_state_text(self, state, text):
        var = self._env_states[state]['env_var']
        return text[len(var) + 1:]

    def set_value(self, value):
        value = prim.nativepath_separators(value)
        env_state = self._env_state_from_value(value)
        if env_state:
            text = self._env_state_text(env_state, value)
        else:
            text = value
        self._set_text(text)

    def _can_change_state(self, state):
        """
        Return True if it is possible to modify the current path to state.
        This will return False on Windows when going to rel or flow states if
        the path is on a different drive than the flow.
        """
        abs_path = self._abs_path(self._get_text())

        if state == self._rel:
            try:
                os.path.relpath(abs_path, self._rel_dir_value)
                return True
            except Exception:
                return False

        elif state in self._env_states:
            try:
                value = self._env_values[state]
                os.path.relpath(abs_path, value)
                return True
            except Exception:
                return False

        return True

    def _change(self, state, text):
        """
        Set state and text in local model, parameter model and (if needed) in
        the gui. Also update the completer model to the current directory.
        """
        if self._get_state() != state:
            self._set_state(state)
        if self._get_text() != text:
            self._set_text(text)

        self._state = state
        self._text = text

        if state in self._env_states:
            var = self._env_states[state]['env_var']
            self._parameter_path.value = os.path.join(var, text)
        else:
            self._parameter_path.value = text

        self._completer_model.setRootPath(
            os.path.abspath(self._abs_path(self._get_text())))

    def _text_edited(self, text):
        """
        Triggered when the path is edited by hand, not when programmatically
        changed.
        """
        if self._text == text:
            return

        if os.path.isabs(text):
            self._change(self._abs, text)
        elif self._state == self._abs:
            self._change(self._rel, text)
        else:
            self._change(self._state, text)
        self.text_changed.emit()

    def _state_edited(self, state):
        """
        Triggered when the state is edited by hand, not when programmatically
        changed.
        """
        if state == self._state:
            return

        text = self._abs_path(self._get_text())

        # TODO(erik): Ideally we should re-implement handling for relative
        # paths so that it does not force the path to be normalized.

        if self._can_change_state(state):
            if state == self._abs:
                text = os.path.abspath(self._abs_path(text))
            elif state == self._rel:
                text, state = self._rel_cwd_path(text)
            elif state in self._env_states:
                text, state = self._rel_env_path(text, state)
        else:
            state = self._state

        self._change(state, text)

    def _dialog_click(self):
        default_path = get_default_path(
            self._abs_path(self._get_text()),
            self._flow_dir_value)

        if not qt_compat2.USES_PYSIDE:
            fq_filename = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select file", default_path,
                ";;".join(self._editor_dict['filter']))
        else:
            fq_filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select file", default_path,
                ";;".join(self._editor_dict['filter']))

        if fq_filename:
            self.dialogChanged.emit(fq_filename)

    def _filename_changed_from_dialog(self, text):
        state = self._state
        if state == self._abs:
            text = self._abs_path(text)
        elif state == self._rel:
            text, state = self._rel_cwd_path(text)
            if state not in self._states:
                # TODO: Should probably try changing to any other state that
                # works (not only try abs) and if no ok state is found, give
                # the user a warning. This is only ever a problem if 'abs'
                # state has been disabled.
                return
        elif state in self._env_states:
            text, state = self._rel_env_path(text, state)
            if state not in self._states:
                # TODO: Should probably try changing to any other state that
                # works (not only try abs) and if no ok state is found, give
                # the user a warning. This is only ever a problem if 'abs'
                # state has been disabled.
                return
        self._change(state, text)


class ParameterEditorFileSaveDialogWidget(ParameterEditorFileDialogWidget):

    def __init__(self, parameter_string, editor_dict, parent=None):
        super().__init__(
            parameter_string, editor_dict, parent)

    def _dialog_click(self):

        default_path = get_default_path(
            self._abs_path(self._get_text()),
            self._flow_dir_value)

        if not qt_compat2.USES_PYSIDE:
            fq_filename = QtWidgets.QFileDialog.getSaveFileName(
                self, "Select file", default_path,
                ";;".join(self._editor_dict['filter']))
        else:
            fq_filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Select file", default_path,
                ";;".join(self._editor_dict['filter']))
        if fq_filename:
            self.dialogChanged.emit(fq_filename)


class ParameterEditorDirectoryDialogWidget(ParameterEditorFileDialogWidget):
    def __init__(self, parameter_string, editor_dict, parent=None):
        super().__init__(
            parameter_string, editor_dict, parent)

    def _dialog_click(self):
        default_path = get_default_path(
            self._abs_path(self._get_text()), self._flow_dir_value)

        selected_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select directory", default_path)

        if selected_dir:
            self.dialogChanged.emit(selected_dir)


class ParameterEditorComboboxWidget(ParameterEditorWidget):
    currentIndexChanged = qt_compat2.Signal(int)

    def __init__(self, parameter_list, editor_dict, parent=None):
        super().__init__(
            parameter_list, editor_dict, parent=parent)
        self._init_combobox()
        use_filter = self._editor_dict.get('filter', False)
        self._filter_combo = sywidgets.ToggleFilterCombobox(
            combobox=self._list_combobox, use_filter=use_filter)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._filter_combo)
        self.setLayout(layout)
        self._options = list(self._editor_dict.get('options', []))
        display = self._editor_dict.get('display')
        self._display_map = {}
        if display is not None and len(display) == len(self._options):
            display = [d.get('text', '') if isinstance(d, dict) else d
                       for d in display]
            self._display_map = dict(zip(self._options, display))
        self._option_map = {v: k for k, v in self._display_map.items()}
        self._init_gui_from_parameters()
        self.currentIndexChanged.connect(
            self._filter_combo.currentIndexChanged)
        self._list_combobox.valueChanged.connect(self._value_changed)
        self._list_combobox.currentIndexChanged[int].connect(
            self.currentIndexChanged)

    def _init_gui_from_parameters(self):
        include_empty = self._editor_dict.get('include_empty', False)
        if include_empty and '' not in self._options:
            self._options.insert(0, '')
        self._add_items(self._options)

    def combobox(self):
        return self._list_combobox

    def _add_new_display_option(self, option):
        if option not in self._display_map:
            str_option = str(option)
            self._option_map[str_option] = option
            self._display_map[option] = str_option

    def _add_items(self, items):
        display = []
        for option in items:
            self._add_new_display_option(option)
            display.append(self._display_map[option])
        self._list_combobox.addItems(display)

    def set_value(self, value):
        text_value = str(value)
        if value in self._options:
            index = self._options.index(value)
        else:
            index = 0
            self._add_new_display_option(value)
            self._list_combobox.insertItem(index, text_value)
            self._list_combobox.setItemData(
                index, QtGui.QBrush(QtCore.Qt.gray), QtCore.Qt.ForegroundRole)
            self._list_combobox.setItemData(
                index, "This item is currently not available.",
                QtCore.Qt.ToolTipRole)

        self._list_combobox.setCurrentIndex(index)

    def _value_changed(self, value):
        text_value = str(value)
        try:
            value = self._option_map[text_value]
        except KeyError:
            pass
        self._parameter_list.value = value
        self.valueChanged.emit(self._parameter_list.value)

    def _init_combobox(self):
        raise NotImplementedError


class ParameterScalarEditorComboboxWidget(ParameterEditorComboboxWidget):

    def _init_combobox(self):
        if not self._editor_dict.get('edit', False):
            self._list_combobox = sywidgets.NonEditableComboBox()
        elif self._parameter_list.type == 'integer':
            self._list_combobox = sywidgets.ValidatedIntComboBox()
        elif self._parameter_list.type == 'float':
            self._list_combobox = sywidgets.ValidatedFloatComboBox()
        else:
            self._list_combobox = sywidgets.ValidatedTextComboBox()


class ParameterFloatEditorComboboxWidget(ParameterScalarEditorComboboxWidget):
    valueChanged = QtCore.Signal(float)


class ParameterIntegerEditorComboboxWidget(
        ParameterScalarEditorComboboxWidget):
    valueChanged = QtCore.Signal(int)


class ParameterListEditorComboboxWidget(ParameterEditorComboboxWidget):
    currentIndexChanged = qt_compat2.Signal(int)
    valueChanged = qt_compat2.Signal(str)

    def __init__(self, parameter_list, editor_dict, parent=None):
        super().__init__(
            parameter_list, editor_dict, parent=parent)

    def _init_gui_from_parameters(self):
        # Treat None in parameter.list as equivalent to empty string, i.e. no
        # selection:
        self._available_items = [
            i if i is not None else '' for i in self._parameter_list.list]
        names = self._parameter_list.value_names
        if names:
            selected = names[0]
        else:
            # Sometimes the list parameter has no value_names, but still has an
            # index. This can be seen as a bug in the list parameter, but we
            # must still deal with it here.
            indexes = self._parameter_list.value
            try:
                selected = self._available_items[indexes[0]]
            except IndexError:
                selected = ''
        self._options = list(self._available_items)
        if selected not in self._options:
            self._options.insert(0, selected or '')

        super()._init_gui_from_parameters()
        # Workaround for case where we replaced explicit None with
        # include_empty.
        try:
            index = self._options.index(selected)
        except ValueError:
            index = -1
        self._list_combobox.setCurrentIndex(index)

    def _value_changed(self, value):
        text_value = str(value)

        if text_value == '' or text_value is None:
            self._parameter_list.list = self._available_items
            self._parameter_list.value_names = []
        else:
            value = text_value
            if text_value not in self._available_items:
                self._parameter_list.list = self._available_items
                try:
                    value = self._option_map[text_value]
                except KeyError:
                    pass
            self._parameter_list.value_names = [value]
        self.valueChanged.emit(self._parameter_list.selected)

    def setCurrentIndex(self, index):
        self._list_combobox.setCurrentIndex(index)

    def clear(self):
        self._list_combobox.clear()
        self._options = []
        self._parameter_list.value_names = []
        self._parameter_list.list = []

    def addItems(self, items):
        self._parameter_list.list = self._parameter_list.list + items
        self._options += items
        self._add_items(items)

    def _init_combobox(self):
        if not self._editor_dict.get('edit', False):
            self._list_combobox = sywidgets.NonEditableComboBox()
        else:
            self._list_combobox = sywidgets.ValidatedTextComboBox()


class ParameterEditorListWidget(ParameterEditorWidget):
    itemChanged = qt_compat2.Signal(QtWidgets.QListWidgetItem)
    _all_buttons = ['All', 'Clear', 'Invert']
    _all_button, _clear_button, _invert_button = _all_buttons
    _all_item_buttons = ['Delete', 'Insert']
    _delete_button, _insert_button = _all_item_buttons
    _standard_item_foreground = QtGui.QStandardItem().foreground()

    def __init__(self, parameter_list, editor_dict, parent=None):
        customization = {
            'selection': '',
            'alternatingrowcolors': True,
            'filter': False,
            'buttons': False,
            'invertbutton': False,
            'mode': False,
            'edit': False}

        passthrough = editor_dict.get('passthrough', False)
        if passthrough:
            editor_dict['mode'] = True

        super().__init__(
            parameter_list, editor_dict, customization, parent)

        # This editor can make use of any extra space it gets.
        policy = self.sizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(policy)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)

        # Ignored customizations.
        # self._customization['buttons']
        # self._customization['invertbutton']
        # TODO: issue a warning.
        use_filter = self._customization['filter']
        self._editable = self._customization['edit']
        self._use_mode = False
        self._use_multi = self._customization['selection'] == 'multi'

        mode_selected = (self._parameter_list._mode_selected,
                         'Use and require selected')
        mode_selected_exists = (self._parameter_list._mode_selected_exists,
                                'Use selected')
        mode_unselected = (self._parameter_list._mode_unselected,
                           'Use unselected')
        mode_passthrough = (self._parameter_list._mode_passthrough,
                            'Use all')
        current_modes = []

        if self._use_multi:
            self._use_mode = self._customization['mode']
            if self._use_mode:
                current_modes = [
                    mode_selected, mode_selected_exists, mode_unselected,
                    mode_passthrough]
            else:
                current_modes = [mode_selected]
            self._mode_widget = sywidgets.ModeComboBox(current_modes)
            if self._use_mode:
                hlayout.addWidget(self._mode_widget)
        else:
            self._mode_widget = sywidgets.ModeComboBox([])

        buttons = []
        if self._use_multi:
            buttons.append(self._all_buttons)
        if self._editable:
            buttons.append(self._all_item_buttons)

        # Widgets
        self._list_widget = sywidgets.SpaceHandlingContextMenuListWidget(
            buttons, self)

        self._filter_widget = sywidgets.ClearButtonLineEdit(
            placeholder='Filter')

        if use_filter:
            if self._use_mode:
                self._filter_button = sywidgets.ToggleFilterButton(
                    filter_widget=self._filter_widget,
                    next_to_widget=self._mode_widget)
                hlayout.addWidget(self._filter_button)
                vlayout.addLayout(hlayout)
            vlayout.addWidget(self._filter_widget)

        vlayout.addWidget(self._list_widget)
        self.setLayout(vlayout)

        # GUI must be initialized from parameters before signals are
        # connected to ensure correct behavior.
        self._init_editor()
        self._init_gui_from_parameters()

        self._list_widget.itemChanged.connect(self._item_changed)
        self._filter_widget.textChanged.connect(self._filter_changed)
        self._list_widget.actionTriggered.connect(self._action_triggered)
        self._mode_widget.itemChanged.connect(self._mode_changed)

    def _init_editor(self):
        if self._use_multi:
            self._list_widget.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection)

        self._list_widget.setAlternatingRowColors(
            bool(self._customization['alternatingrowcolors']))

    def _init_gui_from_parameters(self):
        # Sort the list and put the selected items first.
        selected_items = self._get_and_sort_selected_items()
        if not self._use_multi:
            if len(selected_items) > 0:
                selected_items = [selected_items[0]]
            else:
                selected_items = []

        self._list_widget.blockSignals(True)
        self._check_items(selected_items)
        self._list_widget.blockSignals(False)

    def _mark_item(self, item):
        item.setEditable(self._editable)
        all_items = self._parameter_list.list
        item_text = str(item.text())
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        if item_text not in all_items:
            item.setForeground(QtCore.Qt.gray)
            item.setToolTip("This item is currently not available.")
        else:
            item.setForeground(self._standard_item_foreground)
            item.setToolTip(None)

    def _get_and_sort_selected_items(self):
        """Get and sort selected and non-selected items."""
        all_items = list(self._parameter_list.list)
        value_names = list(self._parameter_list.value_names)
        if (len(value_names) == 0 and
                len(self._parameter_list.value) > 0) and len(all_items) > 0:
            value_names = [self._parameter_list.list[v]
                           for v in self._parameter_list.value]
        selected_items = sorted(self._parameter_list.value_names,
                                key=prim.combined_key)
        not_selected_items = sorted(list(
            set(all_items).difference(set(selected_items))),
                                    key=prim.combined_key)

        self._list_widget.clear()

        for label in selected_items + not_selected_items:
            item = QtGui.QStandardItem(label)
            self._mark_item(item)
            self._list_widget.addItem(item)

        return selected_items

    def _check_items(self, selected_items):
        for row in range(self._list_widget.count()):
            item = self._list_widget.item(row)
            if str(item.text()) in selected_items:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        passthrough = False
        if self._use_multi:
            self._mode_widget.set_selected(
                self._parameter_list._multiselect_mode)
            passthrough = self._parameter_list._passthrough
        self._list_widget.setEnabled(not passthrough)
        self._filter_widget.setEnabled(not passthrough)

    def _item_changed(self, item):
        self._item_state_changed(item)
        self._mark_item(item)

    def _checked_items(self):
        return [item_ for item_ in self._list_widget.items()
                if item_.checkState() == QtCore.Qt.Checked]

    def _set_value_names_from_checked(self):
        self._parameter_list.value_names = [
            str(item_.text()) for item_ in self._checked_items()]

    def _item_state_changed(self, item):
        if not self._use_multi:
            if item.checkState() == QtCore.Qt.Checked:
                # Uncheck all other items
                for item_ in self._checked_items():
                    if item_ is not item:
                        self._list_widget.blockSignals(True)
                        item_.setCheckState(QtCore.Qt.Unchecked)
                        self._list_widget.blockSignals(False)
            elif not self._checked_items():
                # Unchecking items is not possible with single selection
                self._list_widget.blockSignals(True)
                item.setCheckState(QtCore.Qt.Checked)
                self._list_widget.blockSignals(False)

        self._set_value_names_from_checked()
        self.itemChanged.emit(item)

    def _filter_changed(self, text):
        if str(text):
            filter_ = search.fuzzy_free_pattern(text)
            display = [row for row in range(self._list_widget.count())
                       if search.matches(filter_,
                                         self._list_widget.item(row).text())]
        else:
            display = range(self._list_widget.count())

        for row in range(self._list_widget.count()):
            self._list_widget.setRowHidden(row, row not in display)

    def _action_triggered(self, action):
        text = action.text()
        if text in self._all_buttons:
            return self._selection_action_triggered(action)
        elif text in self._all_item_buttons:
            return self._item_action_triggered(action)
        else:
            assert False, 'Unknown action'

    def _item_action_triggered(self, action):
        text = action.text()

        if text == self._delete_button:
            for item_ in self._list_widget.selectedItems():
                if (self._use_multi or
                        item_.checkState() == QtCore.Qt.Unchecked):
                    self._list_widget.removeItem(item_)
            self._set_value_names_from_checked()

        elif text == self._insert_button:
            item = QtGui.QStandardItem('')
            item.setCheckState(QtCore.Qt.Unchecked)
            self._mark_item(item)
            self._list_widget.addItem(item)
        else:
            assert False, 'Unknown action'

    def _selection_action_triggered(self, action):
        text = action.text()
        if text == self._all_button:
            self._all_triggered()
        elif text == self._clear_button:
            self._clear_triggered()
        elif text == self._invert_button:
            self._invert_triggered()
        else:
            assert False, 'Unknown action'

    def _clear_triggered(self):
        for row in range(self._list_widget.count()):
            item = self._list_widget.item(row)
            if not self._list_widget.isRowHidden(row):
                item.setCheckState(QtCore.Qt.Unchecked)

    def _all_triggered(self):
        for row in range(self._list_widget.count()):
            item = self._list_widget.item(row)
            if not self._list_widget.isRowHidden(row):
                item.setCheckState(QtCore.Qt.Checked)

    def _invert_triggered(self):
        for row in range(self._list_widget.count()):
            item = self._list_widget.item(row)
            if not self._list_widget.isRowHidden(row):
                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)

    def _mode_changed(self, mode):
        self._parameter_list._multiselect_mode = mode
        passthrough = self._parameter_list._passthrough
        self._list_widget.setEnabled(not passthrough)
        self._filter_widget.setEnabled(not passthrough)

    def clear(self):
        self._list_widget.blockSignals(True)
        self._list_widget.clear()
        self._parameter_list.list = []
        self._parameter_list.value_names = []
        self._list_widget.blockSignals(False)

    def addItems(self, items):
        self._list_widget.blockSignals(True)
        self._parameter_list.list = self._parameter_list.list + items
        selected_items = self._get_and_sort_selected_items()
        self._check_items(selected_items)
        self._list_widget.blockSignals(False)
        self._filter_changed(self._filter_widget.text())


def lineedit_editor_factory(editor_dict, parameter_model):
    if parameter_model.type == 'integer':
        return ParameterEditorIntegerWidget(
            parameter_model, editor_dict)
    elif parameter_model.type == 'float':
        return ParameterEditorFloatWidget(
            parameter_model, editor_dict)
    else:
        return ParameterEditorTextLineWidget(
            parameter_model, editor_dict)


def combobox_editor_factory(editor_dict, parameter_model):
    if parameter_model.type == 'integer':
        return ParameterIntegerEditorComboboxWidget(
            parameter_model, editor_dict)
    elif parameter_model.type == 'float':
        return ParameterFloatEditorComboboxWidget(
            parameter_model, editor_dict)
    else:
        return ParameterScalarEditorComboboxWidget(
            parameter_model, editor_dict)


def editor_factory(editor_type, editor_dict, parameter_model):
    # TODO(erik): validate that there is a suitable editor for
    # parameter type and inform user otherwise.
    if parameter_model.type == 'boolean':
        _warn_missing_editor(parameter_model.type, editor_type)
        return None
    elif editor_type == "combobox":
        if parameter_model.type == 'list':
            return ParameterListEditorComboboxWidget(
                parameter_model, editor_dict)
        else:
            return combobox_editor_factory(editor_dict, parameter_model)
    elif editor_type == "listview" or editor_type == "basiclist":
        # basiclist is a legacy editor. It has been superseeded by listview
        return ParameterEditorListWidget(
            parameter_model, editor_dict)
    elif editor_type == "filename":
        return ParameterEditorFileDialogWidget(
            parameter_model, editor_dict)
    elif editor_type == "savename":
        return ParameterEditorFileSaveDialogWidget(
            parameter_model, editor_dict)
    elif editor_type == "dirname":
        return ParameterEditorDirectoryDialogWidget(
            parameter_model, editor_dict)
    elif editor_type == "spinbox":
        if parameter_model.type == 'integer':
            return ParameterEditorIntegerWidget(
                parameter_model, editor_dict, spin_buttons=True)
        elif parameter_model.type == 'float':
            return ParameterEditorFloatWidget(
                parameter_model, editor_dict, spin_buttons=True)
        else:
            return None
    elif editor_type == "lineedit":
        return lineedit_editor_factory(editor_dict, parameter_model)
    elif editor_type == 'textedit':
        return ParameterEditorTextAreaWidget(
            parameter_model, editor_dict)
    elif editor_type == 'code':
        return ParameterEditorCodeEditWidget(
            parameter_model, editor_dict)
    elif editor_type == 'table':
        if parameter_model.type == 'json':
            return ParameterEditorJsonTableWidget(
                parameter_model, editor_dict)
    elif editor_type == 'datetime':
        return ParameterEditorDateTimeWidget(
            parameter_model, editor_dict)
    else:
        return None


class ParameterEditorJsonWidget(ParameterEditorWidget):
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, parameter_list, editor_dict, customization=None,
                 parent=None):
        super().__init__(
            parameter_list, editor_dict, customization, parent)

        self._parameter_list = parameter_list
        self._json_lineedit = sywidgets.ValidatedTextLineEdit()
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        self._json_lineedit.clear()
        self._json_lineedit.setBuilder(self._json_validator)
        self._json_lineedit.valueChanged[str].connect(self._value_changed)
        self._json_lineedit.setText(json.dumps(parameter_list.value))

        if parameter_list.description:
            self._json_lineedit.setToolTip(parameter_list.description)
        vlayout.addWidget(self._json_lineedit)
        self.setLayout(vlayout)

    def _json_validator(self, value):
        try:
            json.loads(value)
        except Exception as e:
            raise sywidgets.ValidationError(str(e))
        return value

    def set_value(self, value):
        self._json_lineedit.setText(json.dumps(value))

    def _value_changed(self, value):
        self.valueChanged.emit(json.loads(value))


class ParameterEditorJsonTableWidget(ParameterEditorWidget):
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, parameter_list, editor_dict, customization=None,
                 parent=None):
        super().__init__(
            parameter_list, editor_dict, customization, parent)
        self._parameter_list = parameter_list

        headers = self._editor_dict.get('headers')
        types = self._editor_dict.get('types')
        unique = self._editor_dict.get('unique')

        if headers is not None and types is not None:
            assert len(headers) == len(types)

        if unique is not None:
            assert headers is not None and all(u in headers for u in unique)

        if types is not None:
            assert headers is not None

        if headers is not None:
            assert types is not None

        self._dynamic_cols = headers is None
        if self._dynamic_cols:
            raise NotImplementedError(
                'Dynamic column editor is not implemented')
        self._headers = headers
        self._types = types
        self._unique = unique

        self._table_editor = table_editor.TableWidget(
            self._to_table_data(self._parameter_list.value),
            dynamic_cols=self._dynamic_cols)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)

        self._table_editor.valueChanged[object].connect(self._value_changed)

        if parameter_list.description:
            self._table_editor.setToolTip(parameter_list.description)
        vlayout.addWidget(self._table_editor)
        self.setLayout(vlayout)

    def _validate(self, value):
        return (isinstance(value, list) and len(value) == len(self._headers)
                and len(set(len(rows) for rows in value)) == 1)

    def _to_table_data(self, value):
        # TODO(erik): Fix copy.
        value = json.loads(json.dumps(value))

        if self._dynamic_cols:
            raise NotImplementedError
            return value or []
        else:
            if not self._validate(value):
                value = []

            if value:
                return [[h, t, rows] for h, t, rows in zip(
                    self._headers, self._types, list(zip(*value)))]
            else:
                return [[h, t, []] for h, t in zip(
                    self._headers, self._types)]

    def _from_table_data(self, value):
        # TODO(erik): Fix copy.
        value = json.loads(json.dumps(value))

        if self._dynamic_cols:
            raise NotImplementedError
            return value
        else:
            if value and len(value[0][2]) == 0:
                return []
            return list(zip(*[rows for _, _, rows in value]))

    def set_value(self, value):
        self._table_editor.model().set_data(
            self._to_table_data(value))

    def _value_changed(self, value):
        data = self._from_table_data(value)
        self.valueChanged.emit(data)


class ParameterJsonWidget(ParameterBaseValueWidget):
    valueChanged = qt_compat2.Signal(object)

    def __init__(self, parameter_value, editor=None, parent=None):
        if editor is None:
            editor = ParameterEditorJsonWidget(parameter_value, {})
        super().__init__(
            parameter_value, editor, parent)
        self._editor.valueChanged.connect(self._value_changed)

    def _value_changed(self, value):
        self._parameter_value.value = value
        self.valueChanged.emit(value)


class ParameterListWidget(ParameterWidget):
    def __init__(self, parameter_list, editor=None, parent=None):
        self._parameter_list = parameter_list
        self._list_label = None
        if editor is None:
            editor = ParameterListEditorComboboxWidget(parameter_list, {})
        super().__init__(parameter_list, editor, parent)
        horizontal = isinstance(self._editor,
                                ParameterListEditorComboboxWidget)
        if horizontal:
            layout = QtWidgets.QHBoxLayout()
        else:
            layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if self._parameter_list.label:
            self._list_label = QtWidgets.QLabel(self._parameter_list.label)
            layout.addWidget(self._list_label)
            layout.addItem(QtWidgets.QSpacerItem(10, 1))
            self._list_label.setToolTip(self._parameter_value.description)
        if self._parameter_list.description:
            self._editor.setToolTip(self._parameter_value.description)
            self.setToolTip(self._parameter_list.description)
        layout.addWidget(self._editor)
        self.setLayout(layout)

    def label_widget(self):
        return self._list_label


class ParameterGroupWidget(ParameterView):
    def __init__(self, parameter_group, parent=None, validator=None):
        super().__init__(parameter_group, validator, parent)
        self._parameter_group = parameter_group
        self._tab_widget = None
        vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(vlayout)

    @property
    def label(self):
        return self._parameter_group.label or ''

    def group_layout(self):
        return self.layout()

    def add_page(self, page_widget, name):
        if self._tab_widget is None:
            self._tab_widget = QtWidgets.QTabWidget()
            self.layout().addWidget(self._tab_widget)
        self._tab_widget.addTab(page_widget, name)

    def add_group(self, group_widget):
        vlayout = QtWidgets.QVBoxLayout()
        groupbox = QtWidgets.QGroupBox(group_widget.label)
        groupbox.setLayout(vlayout)
        vlayout.addWidget(group_widget)
        self.layout().addWidget(groupbox)

    def add_widget(self, widget):
        self.layout().addWidget(widget)

    @qt_compat2.Slot(bool)
    def set_enabled(self, value):
        self._groupbox.setEnabled(value)

    @qt_compat2.Slot(bool)
    def set_disabled(self, value):
        self._groupbox.setDisabled(value)

    def needs_stretch(self):
        """
        Returns True if this group contains no vertically expanding widgets.
        """
        if self._tab_widget:
            return False

        layout = self.group_layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            policy = widget.sizePolicy().verticalPolicy()
            if policy == QtWidgets.QSizePolicy.Expanding:
                return False
        return True


class ParameterRootWidget(ParameterGroupWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout().setContentsMargins(0, 0, 0, 0)


class WidgetBuildingVisitor(visitors.IParameterVisitor):
    def __init__(self, validator=None, ports=None):
        self._validator = validator
        self._widget_stack = []
        self._flat_widget_dict = {}
        self._null_root = NullParameterWidget()
        self._ports = ports

    def gui(self):
        return self._parent()

    def widget_dict(self):
        return self._flat_widget_dict

    @contextlib.contextmanager
    def _widget_context(self):
        old_flat_widget_dict = dict(self._flat_widget_dict)
        self._flat_widget_dict.clear()
        yield
        old_flat_widget_dict.update(self._flat_widget_dict)
        self._flat_widget_dict.update(old_flat_widget_dict)

    def _param_widget(self, param, widget_cls):
        if param.editor is None:
            widget = widget_cls(param)
        else:
            editor_widget = editor_factory(
                param.editor['type'],
                param.editor,
                param)
            widget = widget_cls(param, editor_widget)
        return widget

    def visit_root(self, root, controllers=None):

        with self._widget_context():
            widget = ParameterRootWidget(root, validator=self._validator)
            self._push_parent(widget)
            children = root.children()
            for child in children:
                child.accept(self)
            if widget.needs_stretch():
                widget.group_layout().addStretch()

        self._connect_controllers(controllers, widget)
        return widget

    def _connect_controllers(self, controllers, parent):
        # Controller support.
        if controllers is not None:
            widget_dict = self.widget_dict()
            ports = self._ports
            if isinstance(controllers, Iterable):
                for controller in controllers:
                    controller.connect(
                        widget_dict, ports=self._ports, parent=parent)
            else:
                controllers.connect(
                    widget_dict, ports=self._ports, parent=parent)

    def visit_group(self, group, controllers=None):

        with self._widget_context():
            widget = ParameterGroupWidget(group)
            if group.type == 'page':
                self._parent().add_page(widget, group.label)
            else:
                self._parent().add_group(widget)
            self._flat_widget_dict[group.name] = widget
            self._push_parent(widget)
            children = group.children()
            for child in children:
                child.accept(self)
            if widget.needs_stretch():
                widget.group_layout().addStretch()

        self._connect_controllers(controllers, widget)
        self._pop_parent()
        return widget

    def visit_page(self, page):
        return self.visit_group(page)

    def visit_integer(self, param):
        widget = self._param_widget(param, ParameterNumericValueWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_float(self, param):
        widget = self._param_widget(param, ParameterNumericValueWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_string(self, param):
        widget = self._param_widget(param, ParameterStringWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_boolean(self, param):
        widget = self._param_widget(param, ParameterBooleanWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_datetime(self, param):
        widget = self._param_widget(param, ParameterDateTimeWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_json(self, param):
        widget = self._param_widget(param, ParameterJsonWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def visit_list(self, param):
        widget = self._param_widget(param, ParameterListWidget)
        self._flat_widget_dict[param.name] = widget
        self._parent().add_widget(widget)
        return widget

    def _parent(self):
        try:
            return self._widget_stack[-1]
        except IndexError:
            return self._null_root

    def _push_parent(self, widget):
        self._widget_stack.append(widget)

    def _pop_parent(self):
        if len(self._widget_stack) > 1:
            return self._widget_stack.pop()


_depr = object()

def sy_parameters(obj=None, warn=_depr):
    if warn is not _depr:
        sywarn("Argument warn is deprecated and doesn't do anything.")
    if obj is None:
        return models.ParameterRoot(
            gui_visitor=WidgetBuildingVisitor())
    elif isinstance(obj, models.ParameterRoot):
        return obj
    elif isinstance(obj, models.ParameterGroup):
        return obj
    return models.ParameterRoot(
        obj, gui_visitor=WidgetBuildingVisitor())
