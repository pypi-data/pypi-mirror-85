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
"""
Utility functions
"""

import os
import sys
import collections
import logging
import datetime
import unicodedata
import shutil
import contextlib
import uuid

from . import version
from . import settings
from . import qt_support
from sympathy.utils.prim import nativepath, absolute_paths
from sympathy.utils import prim
from sympathy.platform import version_support as vs
from sympathy.utils import process
from sympathy.platform import library as library_platform


core_logger = logging.getLogger('core')

LOG = False
call_level = 0


@contextlib.contextmanager
def bulk_context(flow_):
    flow_.app_core.bulk_operation_requested.emit(flow_)
    yield
    flow_.app_core.bulk_operation_finished.emit(flow_)


class DisplayMessage:
    """
    Message to show in messages view or terminal.
    """
    def source(self):
        raise NotImplementedError

    def id(self):
        raise NotImplementedError

    def title(self):
        raise NotImplementedError

    def notice(self):
        return None

    def warning(self):
        return None

    def error(self):
        return None

    def exception(self):
        return None

    def notice_details(self):
        return None

    def warning_details(self):
        return None

    def error_details(self):
        return None

    def exception_details(self):
        return None

    def node(self):
        return None


class TextMessage(DisplayMessage):

    def __init__(self, title, notice=None, warning=None, source=None):
        self._title = title
        self._notice = notice
        self._warning = warning
        self._source = source or title
        self._id = str(uuid.uuid4())

    def source(self):
        return self._source

    def id(self):
        return self._id

    def title(self):
        return self._title

    def notice(self):
        return self._notice

    def warning(self):
        return self._warning


class ResultMessage(DisplayMessage):
    def __init__(self, title, result, source=None):
        self._title = title
        self._result = result
        self._source = source or title

    def source(self):
        return self._source

    def id(self):
        return self._result.id

    def title(self):
        return self._title

    def notice(self):
        return self._result.stdout

    def warning(self):
        return self._result.stderr

    def _format_exception(self, result_exception):
        data = result_exception.details
        if result_exception.path:
            data = 'Occurred in list index: {}\n{}'.format(
                result_exception.path, data)
        return str(data).strip()

    def error(self):
        exception = self._result.exception
        if exception and exception.node_error:
            return exception.string

    def exception(self):
        exception = self._result.exception
        if exception and not self._result.exception.node_error:
            return exception.string

    def error_details(self):
        exception = self._result.exception
        if exception and exception.node_error:
            return self._format_exception(exception)

    def exception_details(self):
        exception = self._result.exception
        if exception and not self._result.exception.node_error:
            return self._format_exception(exception)


class NodeMessage(ResultMessage):

    def __init__(self, node, result):
        super().__init__(node.name, result, source=node.full_uuid)
        self._node = node

    def title(self):
        return self._node.name

    def node(self):
        return self._node


class OrderedSet(object):

    def __init__(self, items=None):
        if items:
            self._data = dict.fromkeys(items)
        else:
            self._data = {}

    def add(self, item):
        self._data[item] = None

    def remove(self, item):
        del self._data[item]

    def update(self, items):
        for item in items:
            self.add(item)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data.keys())


class Component(object):
    def __init__(self, ctypes=None):
        self._ctypes = ctypes or []
        self._comps = {}

    def register(self, component):
        if self._ctypes:
            ctypes = [ctype for ctype in self._ctypes if
                      isinstance(component, ctype)]
        else:
            ctypes = [None]

        for ctype in ctypes:
            components = self._comps.setdefault(ctype, [])
            if component not in components:
                components.append(component)

    def get(self, ctype=None):
        return list(self._comps.get(ctype, []))


def log_info(f):
    """Decorator - put around a function to log when called."""
    if core_logger.isEnabledFor(logging.INFO):
        return f

    def logged(*args, **kwargs):
        global call_level
        args_to_print = [str(a) for a in args]
        indent = ' ' * (2 * call_level)
        call_level += 1
        core_logger.info(
            '{}@CALLING {}:{}():{} ARGS ({}), {} '.format(
                indent,
                f.func_code.co_filename, f.func_name,
                f.func_code.co_firstlineno + 1, ', '.join(args_to_print),
                kwargs))
        retval = f(*args, **kwargs)
        if hasattr(retval, '__iter__'):
            core_logger.info('{}@RETURNING {}: {}'.format(
                indent, f.func_name, [str(a) for a in retval]))
        else:
            core_logger.info('{}@RETURNING {}: {}'.format(
                indent, f.func_name, str(retval)))
        call_level -= 1
        return retval
    return logged


def log_message(message, data=None, level=logging.INFO):
    if core_logger.isEnabledFor(level):
        core_logger.log(level, message if data is None else '{} {}'.format(
            message, vs.str_(data)))


def log_critical_message(message, data=None):
    log_message(message, data, logging.CRITICAL)


def log_info_message(message, data=None):
    log_message(message, data, logging.INFO)


def log_debug_message(message, data=None):
    log_message(message, data, logging.DEBUG)


def datetime_to_time_string(datetime_):
    return datetime_.strftime('%Y-%m-%d-%H-%M-%S-%f')


def time_string_to_datetime(time_string):
    try:
        return datetime.datetime.now().strptime(time_string,
                                                '%Y-%m-%d-%H-%M-%S-%f')
    except ValueError:
        # Fallback support for old, bad time format which was missing seconds.
        return datetime.datetime.strptime(
            time_string, '%Y-%m-%d-%H-%M-%f')


def now_time_string():
    return datetime_to_time_string(datetime.datetime.now())


def sessions_folder():
    return settings.instance().sessions_folder


def create_session_folder():
    sessions_folder_ = sessions_folder()
    os.environ['SY_TEMP'] = nativepath(sessions_folder_)
    try:
        # Create the temp folder if it does not exist.
        os.makedirs(sessions_folder_)
    except OSError:
        pass

    pid_str = str(os.getpid()).encode('ascii')

    while True:
        # Making sure to create a unique session folder.
        session_folder = os.path.join(sessions_folder_, now_time_string())
        try:
            os.makedirs(session_folder)
        except OSError:
            pass
        else:
            break

    with open(os.path.join(session_folder, 'owner'), 'wb') as f:
        # Create owner file used during cleanup.
        f.write(pid_str)

    os.environ['SY_TEMP_SESSION'] = nativepath(session_folder)
    settings.instance()['session_folder'] = session_folder


def remove_sessions_folder():
    shutil.rmtree(sessions_folder())


def create_default_folder():
    default_folder = settings.instance()['default_folder']
    os.environ['SY_DEFAULT'] = nativepath(default_folder)
    try:
        # Create the default folder if it does not exist.
        os.makedirs(default_folder)
    except OSError:
        pass


def storage_folder(storage=None):
    version_ = 'py{}-{}.{}.{}'.format(
        sys.version_info[0], version.major, version.minor, version.micro)
    if storage is None:
        storage = os.path.normpath(qt_support.data_location())
    return os.path.normpath(os.path.join(storage, version_))


def create_storage_folder(storage=None):
    storage_folder_ = storage_folder(storage)
    try:
        # Create the temp folder if it does not exist.
        os.makedirs(storage_folder_)
    except OSError:
        pass
    settings.instance()['storage_folder'] = storage_folder_
    os.environ['SY_STORAGE'] = nativepath(storage_folder_)


def remove_storage_folders():
    shutil.rmtree(storage_folder())


def icon_path(icon):
    return os.path.join(prim.icons_path(), icon)


def create_install_folder():
    settings.instance()['install_folder'] = prim.sympathy_path()


def setup_resource_folder():
    settings.instance()['resource_folder'] = prim.resources_path()


def remove_duplicates(items):
    res = []
    for item in items:
        if item not in res:
            res.append(item)
    return res


def _parent_root_flows(flow):
    flows = []
    for flow in flow.parent_flows():
        if flow.is_linked:
            flows.append(flow)
    flows.append(flow)
    return flows


def global_library_paths():
    return _global_paths('Python/library_path')


def library_paths(flow=None):
    install_folder = settings.instance()['install_folder']
    paths = absolute_paths(install_folder, [])
    paths.extend(_global_paths('Python/library_path'))
    if flow:
        paths.extend([p for f in _parent_root_flows(flow)
                      for p in f.library_paths(True)])
    else:
        paths.extend(_flow_paths('Python/workflow_library_paths'))
    return [unicodedata.normalize('NFC', path)
            for path in remove_duplicates(paths)]


def python_paths(flow=None):
    paths = _global_paths('Python/python_path')
    if flow:
        paths.extend([p for f in _parent_root_flows(flow)
                      for p in f.python_paths(True)])
    else:
        paths.extend(_flow_paths('Python/workflow_python_paths'))
    return remove_duplicates(paths)


def _global_paths(global_key):
    settings_ = settings.instance()
    install_folder = settings_['install_folder']
    return absolute_paths(
        install_folder, settings_[global_key])


def _flow_paths(workflow_key):
    settings_ = settings.instance()
    paths = []
    if workflow_key in settings_:
        for workflow_paths in settings_[workflow_key].values():
            for path in workflow_paths:
                if path not in paths:
                    paths.append(path)
    return paths


def library_conflicts_worse(old_conflicts, new_conflicts):
    conflicts = 0
    keys = set(old_conflicts)
    keys.update(new_conflicts)

    for key in keys:
        old_value = old_conflicts.get(key, [])
        new_value = new_conflicts.get(key, [])
        conflicts += len(new_value) - len(old_value)
    return conflicts > 0


def library_conflicts(libraries,
                      parent_flow_libraries=None):
    def no_dups(items):
        items_no_dups = []
        for item in items:
            if item not in items_no_dups:
                items_no_dups.append(item)
        return items_no_dups

    res = {}
    parent_flow_libraries = no_dups(parent_flow_libraries or [])
    libraries = no_dups(libraries)
    packages = [library_platform.package_name(lib) for lib in libraries]
    packages = [p for p in packages if p]
    packages_set = set(packages)
    library_packages = dict(zip(libraries, packages))

    if len(packages_set) < len(packages):
        conflicting = [p for p in sorted(packages_set)
                       if packages.count(p) > 1]
        res.setdefault('internal', []).extend(conflicting)

    old_global_libraries = no_dups(global_library_paths())
    old_libraries = no_dups(library_paths())
    new_libraries = [lib for lib in libraries
                     if lib not in old_libraries]
    new_packages_set = set([library_packages[lib]
                            for lib in new_libraries if
                            lib in library_packages])

    conflicting_flow = []
    conflicting_global = []
    conflicting_parent = []

    for lib in old_libraries:
        package = library_platform.package_name(lib)
        if package and package in new_packages_set:
            if lib in old_global_libraries:
                conflicting_global.append(package)
            else:
                if lib in parent_flow_libraries:
                    conflicting_parent.append(package)
                else:
                    conflicting_flow.append(package)

    if conflicting_global:
        res.setdefault('global', conflicting_global)
    if conflicting_parent:
        res.setdefault('internal', []).extend(conflicting_parent)
    if conflicting_flow:
        res.setdefault('flow', []).extend(conflicting_flow)
    return res


class Enum(object):
    def __init__(self, index, value):
        self._index = index
        self._value = value

    @property
    def name(self):
        return self._value

    @property
    def index(self):
        return self._index

    def __str__(self):
        return self._value


def make_enum(name, *fields):
    """
    Generate a new enum class inheriting from EnumBase.
    The class has the following properties:

    New instances can be created using the provided names.
    numbered and named namames must be strings.

    On successive constructions with the same name, the same instance is always
    returned.
    """
    return collections.namedtuple(
        name, fields)(*[Enum(i, field) for i, field in enumerate(fields)])


def post_execution():
    """Perform temporary folder clean-up after the application has finished."""
    def date_list(file_list):
        return sorted((
            time_string_to_datetime(
                os.path.basename(f_name)),
            f_name) for f_name in file_list)

    def size_list(file_list):
        result = []
        for date, f_name in file_list:
            size = 0
            for root_, dirs_, files_ in os.walk(f_name):
                try:
                    size += sum([os.stat(os.path.join(root_, f)).st_size
                                 for f in files_])
                    result.append((f_name, size))
                except OSError:
                    pass
        return result

    def has_backups(session_folder):
        backup_folder = os.path.join(session_folder, 'backups')
        if os.path.isdir(backup_folder):
            for filename in os.listdir(backup_folder):
                if filename.endswith('.syx'):
                    return True
        return False

    settings_ = settings.instance()
    sessions_folder_ = sessions_folder()
    if not os.path.exists(sessions_folder_):
        return

    max_folders = settings_['max_temp_folder_number']

    folders = [os.path.join(sessions_folder_, d)
               for d in os.listdir(sessions_folder_)]
    folders = [d for d in folders
               if os.path.basename(d).startswith('20')
               and os.path.isdir(d) and not has_backups(d)]

    remove_dirs = folders
    # Remove folders with dates older than today minus the given age limit.
    dates = date_list(folders)
    if (settings_.session_temp_files == settings.session_temp_files_keep
            and not settings_.get('clear_caches')):
        date_limit = (datetime.datetime.now() -
                      datetime.timedelta(settings_['max_temp_folder_age']))

        if max_folders:
            keep = dates[-max_folders:]
            remove = dates[:-max_folders]
        else:
            keep = dates
            remove = []

        expired = 0
        for date, fname in keep:
            if date < date_limit:
                expired += 1
            else:
                break

        if expired:
            remove += keep[:expired]
            keep = keep[expired:]

        # Remove folders with if the specified size limit is exceded.
        max_size = settings_['max_temp_folder_size']
        size_limit = int(max_size[:-1])
        modifier = max_size[-1]
        if modifier in ('k', 'K'):
            size_limit *= 1024
        elif modifier in ('M', 'm'):
            size_limit *= 1024 ** 2
        elif modifier in ('G', 'g'):
            size_limit *= 1024 ** 3

        cumulative_size = 0
        remove_dirs = [fname for date, fname in remove]
        for fname, size in reversed(size_list(keep)):
            cumulative_size += size
            if cumulative_size >= size_limit:
                remove_dirs.append(fname)

    remove_own_session = False
    session_folder = os.path.abspath(settings.instance()['session_folder'])

    for dir_name in remove_dirs:
        try:
            owner = os.path.join(dir_name, 'owner')
            if prim.samefile(session_folder, dir_name):
                remove_own_session = True
            else:
                if process.expire(owner, 10):
                    shutil.rmtree(dir_name, ignore_errors=True)
                elif process.age(dir_name) > 10 and not os.path.exists(owner):
                    shutil.rmtree(dir_name, ignore_errors=True)
        except Exception:
            pass

    if remove_own_session or (
            settings_.session_temp_files !=
            settings.session_temp_files_keep):
        shutil.rmtree(session_folder, ignore_errors=True)
    else:
        try:
            os.remove(os.path.join(session_folder, 'owner'))
        except Exception:
            pass

    storage_folder = settings_['storage_folder']

    if settings_.get('clear_caches'):
        if storage_folder:
            shutil.rmtree(storage_folder, ignore_errors=True)

    if settings_.get('clear_settings'):
        settings_.clear()
