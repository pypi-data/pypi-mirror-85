# This file is part of Sympathy for Data.
# Copyright (c) 2015 Combine Control Systems AB
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
This module contains functionality for working with the undo stacks of
sympathy flows.

A flow can have linked subflows in multiple files and we have to track whether
there has been any changes to each of those files. On the other hand we also
want to present a single undo stack for such a flow hierarchy.

This is solved by letting each flow have two undo stacks. One containing all
the undo commands for the entire flow hierarchy (flow.undo_stack()), and one
containing the undo commands that affect a specific syx-file
(flow.file_undo_stack()).

All commands should be pushed to the normal undo stack and are automatically
relayed to the correct file undo stack.
"""
import Qt.QtCore as QtCore
import Qt.QtWidgets as QtWidgets


class WrappedCommand(QtWidgets.QUndoCommand):
    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.setText(cmd.text())
        self._cmd = cmd
        self._first_time = True

    def redo(self):
        if not self._cmd.valid:
            return

        file_undo_stack = self._cmd.flow().file_undo_stack()
        clean_before = file_undo_stack.isClean()
        if self._first_time:
            self._first_time = False
            file_undo_stack.push(self._cmd)
        else:
            file_undo_stack.redo()
        clean_after = file_undo_stack.isClean()
        if clean_before != clean_after:
            self._cmd.flow().propagate_clean_changed()

    def undo(self):
        if not self._cmd.valid:
            return

        file_undo_stack = self._cmd.flow().file_undo_stack()
        clean_before = file_undo_stack.isClean()
        file_undo_stack.undo()
        clean_after = file_undo_stack.isClean()
        if clean_before != clean_after:
            self._cmd.flow().propagate_clean_changed()

    def isObsolete(self):
        return self._cmd.isObsolete()


class UndoStackWrapper(QtWidgets.QUndoStack):
    def push(self, cmd):
        wrapped_cmd = WrappedCommand(cmd)
        if cmd.valid:
            super().push(wrapped_cmd)


class FlowUndoMixin(object):
    clean_changed = QtCore.Signal(bool)
    undo_index_changed = QtCore.Signal()
    subflow_clean_changed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._undo_stack = None
        self._file_undo_stack = None
        self._signals_connected = False

    def undo_stack(self):
        """
        Return the top flow undo stack for this flow.

        This is where you should push commands.
        """
        if self._undo_stack is None:
            if self._flow is None:
                self._undo_stack = UndoStackWrapper(parent=self)
            else:
                self._undo_stack = self._flow.undo_stack()

        return self._undo_stack

    def file_undo_stack(self):
        """
        Return the top undo stack for this workflow file.

        Used internally to keep track of the clean state of each file in a
        workflow with linked subflows. Don't push commands to this undo stack.
        """
        if self._file_undo_stack is None:
            if self._flow is None or self._is_linked:
                self.set_file_undo_stack(QtWidgets.QUndoStack(parent=self))
            else:
                self.set_file_undo_stack(self._flow.file_undo_stack())

        return self._file_undo_stack

    def set_file_undo_stack(self, undo_stack):
        """
        Set the undo stack for this workflow file.

        Used when a flow object changes file. E.g. when a subflow becomes
        linked.
        """
        if self._file_undo_stack is not None and self._signals_connected:
            self._file_undo_stack.indexChanged.disconnect(self._emit_undo_index_changed)
            self._file_undo_stack.cleanChanged.disconnect(self.clean_changed)
            self._signals_connected = False
        self._file_undo_stack = undo_stack

        # If it's the same undo stack as in parent workflow we don't want to
        # connect these signals, but leave that up to the parent workflow.
        if (self._flow is None or
                undo_stack is not self._flow.file_undo_stack()):
            self._signals_connected = True
            self._file_undo_stack.indexChanged.connect(self._emit_undo_index_changed)
            self._file_undo_stack.cleanChanged.connect(self.clean_changed)

    def _emit_undo_index_changed(self, *args, **kwargs):
        self.undo_index_changed.emit()

    def set_clean(self, clean=True):
        """
        Mark if the flow is in a clean state (it has been saved).

        If clean is False, the clean index is set to -1, so no amount of
        undo/redo will get you to a clean state. This is useful e.g. when
        restoring a file from backup.
        """
        if clean:
            self.file_undo_stack().setClean()
        else:
            self.file_undo_stack().resetClean()
        self.propagate_clean_changed()

    def is_clean(self):
        """Return False if there are unsaved changes, and True otherwise."""
        return self.file_undo_stack().isClean()

    def subflows_are_clean(self):
        """
        Return False if there are unsaved changes in this flow or any subflow,
        and True otherwise.
        """
        is_clean = self.is_clean()
        for flow_ in self.all_subflows():
            if not flow_.is_clean():
                is_clean = False
                break
        return is_clean

    def propagate_clean_changed(self):
        """Tell all parent flows that this flow has changed."""
        flow = self.flow
        while flow is not None:
            # Any value emitted with this signal would have to match the return
            # value of subflows_are_clean to be useful. We can't guarantee that
            # since we don't know if other subflows are clean so better to not
            # emit any value at all.
            flow.subflow_clean_changed.emit()
            flow = flow.flow
