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
from .. import settings

grid_instance = None

SNAP_RESOLUTIONS = {
    'Grid': 1, 'Subgrid': 0.25
}


class Grid(object):
    def __init__(self):
        self._enabled = False
        self._spacing = settings.instance()['Gui/grid_spacing']
        self._resolution = SNAP_RESOLUTIONS['Grid']
        self.reload_settings()

    def reload_settings(self):
        snap = settings.instance()['Gui/snap_type']
        spacing = settings.instance()['Gui/grid_spacing']

        if snap in SNAP_RESOLUTIONS:
            self._enabled = True
            self._resolution = SNAP_RESOLUTIONS[snap]
        else:
            self._enabled = False

        if spacing:
            self._spacing = spacing

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def spacing(self):
        return self._spacing

    def snap_to_grid(self, point):
        if self._enabled:
            snap = self._spacing * self._resolution
            point.setX(round(point.x() / snap) * snap)
            point.setY(round(point.y() / snap) * snap)
        return point


def create_grid():
    global grid_instance
    if grid_instance is not None:
        raise RuntimeError('Theme already instantiated')
    grid_instance = Grid()


def instance():
    """Returns the global grid instance"""
    if grid_instance is None:
        create_grid()
    return grid_instance
