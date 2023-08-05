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
import os
import copy
import uuid

import Qt.QtCore as QtCore

from . import qt_support
from . import environment_variables

SETTINGS_MAJOR_VERSION = 2
SETTINGS_MINOR_VERSION = 0
SETTINGS_MAINTENANCE_VERSION = 0

settings_instance = None
properties_instance = None

show_message_area_choice = [
    "Automatic",
    "Always",
    "Never",
    "After first message"]

(show_message_area_automatic,
 show_message_area_always,
 show_message_area_never,
 show_message_area_after_first) = show_message_area_choice

session_temp_files_choice = [
    'Keep',
    'Remove when closing flow',
    'Remove when closing application',
    'Remove unused files']

(session_temp_files_keep,
 session_temp_files_remove_flow,
 session_temp_files_remove_application,
 session_temp_files_remove_unused) = session_temp_files_choice

on_start_choice = [
    "Nothing",
    "New flow",
    "Last session's flows"]

(on_start_nothing,
 on_start_new_flow,
 on_start_last_session) = on_start_choice

stored_permanent = set([
    'user_id',
])


def migrate_old_settings(old_settings, new_settings):
    """Modify the old settings to make use of settings that have changed."""
    if old_settings.contains('Gui/library_type'):
        v = old_settings.value('Gui/library_type')
        if v in ['Separated Tag layout', 'Disk layout']:
            new_settings.setValue('Gui/library_separated', True)

    if (old_settings.contains('save_session')
            and old_settings.value('save_session')):
        new_settings.setValue('Gui/on_start', on_start_last_session)
    elif (old_settings.contains('new_flow_on_start')
            and not old_settings.value('new_flow_on_start')):
        new_settings.setValue('Gui/on_start', on_start_nothing)
    else:
        new_settings.setValue('Gui/on_start', on_start_new_flow)


class Properties:

    _sessions_folder_var = 'SY_OVERRIDE_TEMP_PATH'

    @property
    def sessions_folder_override(self):
        return os.environ.get(self._sessions_folder_var)

    @property
    def sessions_folder_override_description(self):
        res = ''
        override = self.sessions_folder_override
        if override:
            res = (
                'Path is controlled by the external environment variable '
                f'SY_OVERRIDE_TEMP_PATH which points to: {override}')
        return res

    @property
    def sessions_folder(self):
        temp_folder = self.sessions_folder_override
        if not temp_folder:
            temp_folder = self['temp_folder']

        env = environment_variables.instance()
        return env.expand_string(temp_folder)

    @sessions_folder.setter
    def sessions_folder(self, value):
        if self.sessions_folder != value:
            self['temp_folder'] = value

    @property
    def session_temp_files(self):
        return self['session_temp_files']

    @session_temp_files.setter
    def session_temp_files(self, value):
        if self.session_temp_files != value:
            self['session_temp_files'] = value


# Default values for settings that will be written to the preferences file.
permanent_defaults = {
    'Debug/graphviz_path': '',
    'Debug/profile_path_type': 'Session folder',
    'Gui/grid_spacing': 25,
    'Gui/library_separated': False,
    'Gui/library_show_hidden': False,
    'Gui/library_matcher_type': 'character',
    'Gui/library_highlighter_type': 'background-color',
    'Gui/library_highlighter_color': '#EECC22',
    'Gui/quickview_popup_position': 'center',
    'Gui/recent_flows': [],
    'Gui/show_message_area': show_message_area_after_first,
    'Gui/show_splash_screen': True,
    'Gui/snap_type': 'Grid',
    'Gui/system_editor': True,
    'Gui/nodeconfig_confirm_cancel': True,
    'Gui/theme': 'Grey',
    'Gui/code_editor_theme': "colorful",
    'Gui/docking_enabled': 'Movable',
    'Gui/flow_connection_shape': 'Spline',
    'Gui/experimental': False,
    'Gui/platform_developer': False,
    'Gui/on_start': on_start_new_flow,
    'Python/library_path': [],
    'Python/recent_library_path': [],
    'Python/python_path': [],
    'MATLAB/matlab_path': '',
    'MATLAB/matlab_jvm': True,
    'autosave': False,
    'ask_for_save': True,
    'environment': [],
    'max_task_chars': 32000,
    'max_temp_folder_age': 3,
    'max_temp_folder_number': 100,
    'max_temp_folder_size': '1 G',
    'session_temp_files':  session_temp_files_remove_unused,
    'session_files': [],
    'temp_folder': os.path.join(
        os.path.normpath(
            qt_support.cache_location()),
        'Sympathy for Data'),
    'default_folder': os.path.join(
        os.path.normpath(
            qt_support.documents_location()),
        'Sympathy for Data'),
    'max_nbr_of_threads': 0,
    'deprecated_warning': True,
    'user_id': str(uuid.uuid4()),
    'send_stats': False,
    'configured_version': '1.0.0',
}


def to_list(value):

    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def to_bool(value):
    if isinstance(value, bool):
        return value
    elif value == 'true':
        return True
    else:
        return False


# Types for settings that will be written to the preferences file.
# None means, value returned as is.
permanent_types = {
    'Debug/graphviz_path': None,
    'Debug/profile_path_type': None,
    'Gui/geometry': None,
    'Gui/grid_spacing': int,
    'Gui/library_separated': to_bool,
    'Gui/library_show_hidden': to_bool,
    'Gui/library_matcher_type': None,
    'Gui/library_highlighter_type': None,
    'Gui/library_highlighter_color': None,
    'Gui/quickview_popup_position': None,
    'Gui/recent_flows': to_list,
    'Gui/show_message_area': None,
    'Gui/show_splash_screen': to_bool,
    'Gui/snap_type': None,
    'Gui/system_editor': to_bool,
    'Gui/code_editor_theme': None,
    'Gui/theme': None,
    'Gui/window_state': None,
    'Gui/nodeconfig_confirm_cancel': to_bool,
    'Gui/docking_enabled': None,
    'Gui/flow_connection_shape': None,
    'Gui/experimental': to_bool,
    'Gui/platform_developer': to_bool,
    'Gui/on_start': None,
    'Python/library_path': to_list,
    'Python/recent_library_path': to_list,
    'Python/python_path': to_list,
    'MATLAB/matlab_path': None,
    'MATLAB/matlab_jvm': to_bool,
    'ask_for_save': to_bool,
    'autosave': to_bool,
    'environment': to_list,
    'max_task_chars': int,
    'max_temp_folder_age': int,
    'max_temp_folder_number': int,
    'max_temp_folder_size': None,
    'session_files': to_list,
    'session_temp_files': None,
    'temp_folder': None,
    'default_folder': None,
    'max_nbr_of_threads': int,
    'config_file_version': None,
    'deprecated_warning': to_bool,
    'user_id': None,
    'send_stats': to_bool,
    'configured_version': None,
}


# These settings will be available in worker processes.
worker_settings = [
    'Gui/code_editor_theme',
    'Gui/show_message_area',
    'Gui/nodeconfig_confirm_cancel',
    'MATLAB/matlab_path',
    'MATLAB/matlab_jvm',
    'default_folder',
    'session_folder',
    'deprecated_warning',
    'Debug/graphviz_path',
    'max_task_chars',
]


def get_worker_settings():
    """
    Return a dictionary with all the settings that should be exposed to the
    worker.
    """
    return {k: instance()[k] for k in worker_settings}


class Settings(Properties):

    def __init__(self, ini_file_name=None):
        super(Settings, self).__init__()
        self._file_name = ini_file_name
        self._permanent_storage = None
        self._temporary_storage = {}
        self._error = False
        self._init()

    def _init(self):
        if self._file_name:
            self.set_ini_file(self._file_name)
        else:
            self._permanent_storage = QtCore.QSettings(
                QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope,
                'Combine', 'Sympathy')
            if not os.path.exists(self._permanent_storage.fileName()):
                old_storage = QtCore.QSettings(
                    QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope,
                    'Sysess', 'Sympathy_1.3')
                if os.path.exists(old_storage.fileName()):
                    print('Copying settings from older version:',
                          old_storage.fileName())
                    migrate_old_settings(old_storage, self._permanent_storage)
                    for k in old_storage.allKeys():
                        if k in permanent_defaults:
                            self._permanent_storage.setValue(k, old_storage.value(k))
                self._permanent_storage.sync()

            if len(self._permanent_storage.allKeys()) == 0:
                self._update_version()

            self._error = not self._check_version()
        for key in stored_permanent:
            if not self._permanent_storage.contains(key):
                self._set_permanent(key, permanent_defaults[key])

    def _check_version(self):
        version = self._permanent_storage.value(
            'config_file_version', '0.0.0').split('.')
        major_version = int(version[0])
        minor_version = int(version[1])
        # maintenance_version = int(version[2])
        version_is_supported = ((major_version == SETTINGS_MAJOR_VERSION) and
                                (minor_version <= SETTINGS_MINOR_VERSION))
        if (version_is_supported):
            self._update_version()

        return version_is_supported

    def _update_version(self):
        self['config_file_version'] = '{}.{}.{}'.format(
            SETTINGS_MAJOR_VERSION,
            SETTINGS_MINOR_VERSION,
            SETTINGS_MAINTENANCE_VERSION)

    def set_ini_file(self, file_name):
        self._error = False
        self._file_name = file_name

        new_file = os.path.exists(file_name)

        self._permanent_storage = QtCore.QSettings(
            self._file_name, QtCore.QSettings.IniFormat)
        if new_file:
            self._update_version()
        else:
            self._error = not self._check_version()

    def keys(self):
        return (self._permanent_storage.allKeys() +
                self._temporary_storage.keys())

    def clear(self):
        self._permanent_storage.clear()
        self._temporary_storage.clear()
        self._error = False
        self._update_version()

    def error(self):
        return self._error

    def file_name(self):
        return self._file_name

    def __contains__(self, key):
        if key in permanent_defaults:
            return True
        elif key in permanent_types and self._permanent_storage.contains(key):
            return True
        return key in self._temporary_storage

    def __getitem__(self, key):
        if key in permanent_types:
            if self._permanent_storage.contains(key):
                value = self._permanent_storage.value(key)
                type_ = permanent_types.get(key)
                if type_:
                    return type_(value)
                return value
            elif key in permanent_defaults:
                return copy.copy(permanent_defaults[key])
            raise KeyError('Settings instance does not have key: "{}"'.
                           format(key))
        else:
            try:
                return copy.copy(self._temporary_storage[key])
            except KeyError:
                raise KeyError('Settings instance does not have key: "{}"'.
                               format(key))

    def _set_permanent(self, key, value):
        self._permanent_storage.setValue(key, value)
        self._permanent_storage.sync()

    def __setitem__(self, key, value):
        if key in permanent_types:
            current = self.get(key)
            if current is None or current != value:
                self._set_permanent(key, value)
        else:
            self._temporary_storage[key] = value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def sync(self):
        self._permanent_storage.sync()


def create_settings(fq_ini_filename=None):
    global settings_instance
    if settings_instance is not None:
        raise RuntimeError('Settings already instantiated.')
    if fq_ini_filename is None:
        settings_instance = Settings()
    else:
        settings_instance = Settings(fq_ini_filename)


def instance():
    if settings_instance is None:
        create_settings()
    return settings_instance
