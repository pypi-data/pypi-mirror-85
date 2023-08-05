# This file is part of Sympathy for Data.
# Copyright (c) 2013, 2018, Combine Control Systems AB
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
import importlib
import sys
import os
import distutils.version
from . import version_support as vs

USES_PYSIDE = True


def _mpl():
    import matplotlib
    return matplotlib


def _mpl_version():
    return distutils.version.LooseVersion(_mpl().__version__).version[:3]


class QtBackend(object):
    """Abstract interface class to define the backend functionality."""
    def use_matplotlib_qt(self):
        raise NotImplementedError('use_matplotlib_qt')

    def use_ipython_qt(self):
        raise NotImplementedError('use_ipython_qt')


class PySideBackend(QtBackend):
    def __init__(self):
        super(PySideBackend, self).__init__()

    def use_matplotlib_qt(self):
        import Qt
        import matplotlib
        binding = Qt.__binding__
        if _mpl_version() < [2, 2, 0]:
            matplotlib.rcParams['backend.qt4'] = binding

        if binding in ['PySide2', 'PyQt5']:
            matplotlib.use('Qt5Agg')
            matplotlib.rcParams['backend'] = 'Qt5Agg'
        elif binding in ['PyQt', 'PySide']:
            matplotlib.use('Qt4Agg')
            matplotlib.rcParams['backend'] = 'Qt4Agg'
        else:
            assert False, 'Unknown Qt api.'
        os.environ['QT_API'] = binding.lower()

    def use_ipython_qt(self):
        import Qt
        os.environ['QT_API'] = Qt.__binding__.lower()


if USES_PYSIDE:
    backend = PySideBackend()
    import Qt
    from Qt import QtCore
    from Qt import QtGui
    from Qt import QtWidgets

    try:
        QtCore.QStringListModel
    except AttributeError:
        try:
            QtCore.QStringListModel = sys.modules[
                f'{Qt.__binding__}.QtCore'].QStringListModel
        except Exception:
            pass
else:
    raise Exception('No Qt4 backend available')
    backend = QtBackend()


def import_module(module_name):
    return importlib.import_module(
        vs.str_('{}{}'.format('Qt.', module_name)))


Signal = QtCore.Signal
Slot = QtCore.Slot
Property = QtCore.Property
