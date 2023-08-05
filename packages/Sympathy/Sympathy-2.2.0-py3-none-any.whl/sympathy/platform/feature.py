# This file is part of Sympathy for Data.
# Copyright (c) 2020, Combine Control Systems AB
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
import typing as _t
import pkg_resources as _pkg_resources
from Qt import QtCore
from Qt import QtWidgets


# Preference section interface:


class PreferenceSection(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def save(self):
        pass

    def name(self):
        return ''


# Features interface:

class Features(QtCore.QObject):

    changed = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @property
    def name(self) -> str:
        return ""

    @property
    def description(self) -> str:
        return ""

    def start(self):
        pass

    def stop(self):
        pass

    def is_active(self, feature) -> bool:
        return False

    def preference_sections(self) -> _t.List[PreferenceSection]:
        return []

    def message(self) -> str:
        return ""

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()


# Package interface:

def manager() -> Features:
    raise NotImplementedError()


def worker() -> Features:
    raise NotImplementedError()


def license_info() -> dict:
    """
    Return feature license info, similar to version.license_info().
    """
    return {}


# Feature plugins:

_identifier = 'sympathy.feature.plugins'
_features = {True: None, False: None}


def available_features(load=True):
    if _features[load] is None:
        if load:
            plugins = {
                entry_point.name: entry_point.load()
                for entry_point
                in _pkg_resources.iter_entry_points(_identifier)
            }
        else:
            plugins = {
                entry_point.name: entry_point
                for entry_point
                in _pkg_resources.iter_entry_points(_identifier)
            }
        _features[load] = plugins.values()
    return _features[load]


# Utilities:


def satisfies(required):
    return all(any(f.manager().is_active(r)
                   for f in available_features()) for r in required)
