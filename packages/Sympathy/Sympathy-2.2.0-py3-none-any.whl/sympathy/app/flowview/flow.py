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
import json
import math
import functools
import time
import logging
import itertools
import os
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtWidgets as QtWidgets
import Qt.QtSvg as QtSvg

from .. import flow
from .. import signals
from .. import user_commands
from .. import appcore
from .. import settings
from .. import common
from .. import themes
from . import grid
from .types import ElementViewInterface
from .textfield import TextFieldView
from .node import NodeView
from .subflow import SubflowView
from .connection import ConnectionView, TransientConnectionView, RoutePointView
from .flowio import FlowInputView, FlowOutputView
from .flowinfo import show_info
from .. import library
from .. windows import library_view
from .. import user_statistics
from sympathy.utils.prim import uri_to_path

_background_color = b'#F5F5F5'
core_logger = logging.getLogger('core')


def filter_nodes(element_list):
    return [
        element for element in element_list
        if flow.Type.is_port_manager(element)]


def filter_nodes_to_model(element_list, filter_valid_structural_change=False):
    models = filter_model_types(elements_models(element_list),
                                flow.Type.main_types)

    if filter_valid_structural_change:
        return [model for model in models if model.is_deletable()]
    return models


def filter_element_views(element_list):
    return [element for element in element_list
            if isinstance(element, ElementViewInterface)]


def filter_element_views_to_model(element_list):
    return [
        element.model for element in element_list
        if isinstance(element, ElementViewInterface)]


def filter_element_model_types(element_list, model_types):
    return [element for element in element_list
            if element.model.type in model_types]


def filter_model_types(model_list, model_types):
    return [model for model in model_list
            if model.type in model_types]


def remove_model_types(model_list, model_types):
    return [model for model in model_list
            if model.type not in model_types]


def elements_models(element_list):
    return [element.model for element in element_list]


def set_selected(item, item_view):
    if item.was_in_subflow:
        item_view.setSelected(True)
        item.was_in_subflow = False


class FlowView(ElementViewInterface, QtWidgets.QGraphicsView):
    """The flow is where the nodes etc. live"""

    selection_changed = QtCore.Signal()
    selected_nodes_changed = QtCore.Signal(flow.Node)
    edit_subflow_requested = QtCore.Signal(flow.Flow)
    inserting_text_field = QtCore.Signal()
    normal_editing = QtCore.Signal()
    state_changed = QtCore.Signal()
    help_requested = QtCore.Signal(str)
    # _finish_move = QtCore.Signal()

    def __init__(self, model, app_core, parent=None):
        super(FlowView, self).__init__(parent)
        self._model = model
        self._app_core = app_core
        self._node_views = []
        self._subflow_views = []
        self._text_field_views = []
        self._route_point_views = []
        self._nodes = {}
        self._subflows = {}
        self._node_signals = signals.SignalHandler()
        self._connections = {}
        self._init()
        self._init_actions()
        self._init_signalling()
        self._init_views()
        self._init_state_machine()
        self._init_context_menu()
        self._init_background()
        QtCore.QTimer.singleShot(0, self.zoom_fit_all)

    def _init(self):
        self._pan_pos = None
        self._item_cursor = None
        self._flow_cursor = None
        self._source_port = None
        self._transient_connection = None
        self.setSceneRect(QtCore.QRectF())
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.TextAntialiasing |
                            QtGui.QPainter.HighQualityAntialiasing |
                            QtGui.QPainter.SmoothPixmapTransform)
        self._scene = FlowScene(flow_view=self)
        self.setScene(self._scene)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)
        self.setOptimizationFlag(
            QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(
            QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.grabGesture(QtCore.Qt.PinchGesture)

        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.centerOn(self.sceneRect().center())

    def _init_actions(self):
        theme = themes.get_active_theme()
        self._show_info_action = self._create_action(
            'Properties', slot=self._show_info)
        self._settings_action = self._create_action(
            'Settings', slot=self._show_settings)
        self._create_subflow_action = self._create_action(
            'Create Subflow', slot=self._create_subflow)
        self._create_lambda_action = self._create_action(
            'Create Lambda', slot=self._create_lambda)
        self._insert_subflow_action = self._create_action(
            'Insert Subflow as Link...', slot=self._handle_insert_subflow)
        self._create_flow_input_action = self._create_action(
            'Create', slot=self._create_flow_input)
        self._create_flow_output_action = self._create_action(
            'Create', slot=self._create_flow_output)
        self._paste_action = self._create_action(
            'Paste', icon=theme.paste, slot=self.handle_paste_at_context_menu)

    def _create_action(self, text, icon=None, slot=None):
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(icon))
        if slot is not None:
            action.triggered.connect(slot)
        return action

    def _init_signalling(self):
        self._node_signals.connect(
            self._model,
            self._model.node_created[flow.NodeInterface],
            self._handle_node_created)

        self._node_signals.connect(
            self._model,
            self._model.node_removed[flow.NodeInterface],
            self._handle_node_removed)

        self._node_signals.connect(
            self._model,
            self._model.subflow_created[flow.NodeInterface],
            self._handle_subflow_created)

        self._node_signals.connect(
            self._model,
            self._model.subflow_removed[flow.NodeInterface],
            self._handle_subflow_removed)

        self._node_signals.connect(
            self._model,
            self._model.flow_input_created[flow.NodeInterface],
            self._handle_flow_input_created)

        self._node_signals.connect(
            self._model,
            self._model.flow_input_removed[flow.NodeInterface],
            self._handle_flow_input_removed)

        self._node_signals.connect(
            self._model,
            self._model.flow_output_created[flow.NodeInterface],
            self._handle_flow_output_created)

        self._node_signals.connect(
            self._model,
            self._model.flow_output_removed[flow.NodeInterface],
            self._handle_flow_output_removed)

        self._node_signals.connect(
            self._model,
            self._model.connection_created[flow.Connection],
            self._handle_connection_created)

        self._node_signals.connect(
            self._model,
            self._model.connection_removed[flow.Connection],
            self._handle_connection_removed)

        self._node_signals.connect(
            self._model,
            self._model.text_field_created[flow.TextField],
            self._handle_text_field_created)

        self._node_signals.connect(
            self._model,
            self._model.text_field_removed[flow.TextField],
            self._handle_text_field_removed)

        self._node_signals.connect(
            self._model, self._model.route_point_added,
            self._handle_route_point_added)

        self._node_signals.connect(
            self._model, self._model.route_point_removed,
            self._handle_route_point_removed)

        self._node_signals.connect(
            self._model, self._model.flow_updated,
            self._init_views)

        self._node_signals.connect(
            self._model, self._model.icon_changed,
            self._init_background)

        self._scene.selectionChanged.connect(self._handle_selection_changed)

    def close(self):
        self.remove()

    def remove(self):
        self.blockSignals(True)
        self._scene.selectionChanged.disconnect(self._handle_selection_changed)
        self._node_signals.disconnect_all()
        for node_view in list(self._nodes.values()):
            node_view.remove()
        for node_view in list(self._connections.values()):
            node_view.remove()
        self._scene.remove()
        self.blockSignals(False)

    def _enable_actions(self):
        self._create_flow_input_action.setEnabled(
            self._model.can_create_flow_input())
        self._create_flow_output_action.setEnabled(
            self._model.can_create_flow_output())

    def _init_context_menu(self):
        self._context_menu_pos = None
        self._context_menu = QtWidgets.QMenu(parent=self)
        self._context_menu.addAction(self._paste_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._create_subflow_action)
        self._context_menu.addAction(self._create_lambda_action)
        self._context_menu.addAction(self._insert_subflow_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._settings_action)
        ports_menu = self._context_menu.addMenu('Ports')
        input_menu = ports_menu.addMenu('Input')
        output_menu = ports_menu.addMenu('Output')
        input_menu.addAction(self._create_flow_input_action)
        output_menu.addAction(self._create_flow_output_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._show_info_action)

    @QtCore.Slot()
    def _init_views(self):
        self.blockSignals(True)
        while len(self._connections) > 0:
            connection = self._connections.keys()[0]
            self._handle_connection_removed(connection)
        while len(self._subflow_views) > 0:
            self._handle_subflow_removed(self._subflow_views[0].model)
        while len(self._node_views) > 0:
            self._handle_node_removed(self._node_views[0].model)
        self._connections.clear()
        self._node_views = []
        self._subflow_views = []
        self._subflows.clear()
        self._nodes.clear()
        self._scene.clear()
        self.blockSignals(False)

        for e in self._model.elements():
            if e.type == flow.Type.Node:
                self._handle_node_created(e)
            elif e.type == flow.Type.Flow:
                self._handle_subflow_created(e)
            elif e.type == flow.Type.FlowInput:
                self._handle_flow_input_created(e)
            elif e.type == flow.Type.FlowOutput:
                self._handle_flow_output_created(e)
            elif e.type == flow.Type.TextField:
                self._handle_text_field_created(e)

        for c in self._model.connections():
            self._handle_connection_created(c)

    def _init_state_machine(self):
        self._state_machine = QtCore.QStateMachine(parent=self)

        self._normal_edit_state = QtCore.QState(self._state_machine)
        self._insert_text_field_state = QtCore.QState(self._state_machine)
        self._normal_edit_state.addTransition(
            self.inserting_text_field, self._insert_text_field_state)
        self._insert_text_field_state.addTransition(
            self.normal_editing, self._normal_edit_state)

        self._state_machine.setInitialState(self._normal_edit_state)

        self._normal_edit_state.entered.connect(self.state_changed)
        self._normal_edit_state.entered.connect(self._on_normal_edit)
        self._insert_text_field_state.entered.connect(self.state_changed)
        self._insert_text_field_state.entered.connect(
            self._on_insert_text_field)

        self._state_machine.start()

    def _init_background(self):
        self._renderers = []

        background = self._model.background
        if background:
            self._renderers.append(QtSvg.QSvgRenderer(uri_to_path(background)))

    @QtCore.Slot()
    def _show_info(self):
        show_info(self._model)

    @QtCore.Slot()
    def _show_settings(self):
        self._model.settings()

    def _cursor_point(self):
        top_right = self._context_menu_pos or self.mapToScene(
            self.mapFromGlobal(QtGui.QCursor.pos()))
        size = self._model.size
        center = top_right - QtCore.QPointF(size.height() / 2,
                                            size.width() / 2)
        return center

    def _create_flow(self, factory):
        cmd = factory(
            position=self._cursor_point(), flow=self._model)
        self._model.undo_stack().push(cmd)

    @QtCore.Slot()
    def _create_subflow(self):
        self._create_flow(user_commands.CreateSubflowCommand)

    @QtCore.Slot()
    def _create_lambda(self):
        self._create_flow(user_commands.CreateLambdaCommand)

    def _create_flowio(self, factory):
        cmd = factory(
            flow=self._model, position=self._cursor_point())
        self._model.undo_stack().push(cmd)

    def _handle_insert_subflow(self):
        try:
            flow_filename = self._model.root_or_linked_flow_filename
            if flow_filename:
                directory = os.path.dirname(flow_filename)
            else:
                directory = settings.instance()['default_folder']
            result = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Open flow', directory, 'Sympathy flow (*.syx)')
            if isinstance(result, tuple):
                filename = result[0]
            else:
                filename = result

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)
            self._app_core.set_validate_enabled(False)
            cmd = user_commands.InsertSubflowLinkCommand(
                filename=filename,
                flow_=self._model, position=self._context_menu_pos)
            self._model.undo_stack().push(cmd)
        finally:
            self._app_core.set_validate_enabled(True)
            QtWidgets.QApplication.restoreOverrideCursor()

        if cmd.valid:
            cmd.created_element().validate()

    @QtCore.Slot()
    def _create_flow_input(self):
        self._create_flowio(user_commands.CreateFlowInputCommand)

    @QtCore.Slot()
    def _create_flow_output(self):
        self._create_flowio(user_commands.CreateFlowOutputCommand)

    def _common_node_creation(self, node, node_view):
        self._node_views.append(node_view)
        self._nodes[node] = node_view
        self._scene.addItem(node_view)
        self._node_signals.connect(
            node, node_view.connection_start_requested[object],
            self._handle_connection_start_requested)
        self._node_signals.connect(
            node, node_view.connection_end_requested[object],
            self._handle_connection_end_requested)
        self._node_signals.connect(
            node, node_view.open_add_context_requested[
                QtWidgets.QGraphicsSceneMouseEvent],
            self._handle_add_context_requested)
        set_selected(node, node_view)
        self._node_signals.connect(
            node, node_view.cut_requested[ElementViewInterface],
            self.handle_cut)
        self._node_signals.connect(
            node, node_view.copy_requested[ElementViewInterface],
            self.handle_copy_from_node)
        self._node_signals.connect(
            node, node_view.delete_requested[ElementViewInterface],
            self.handle_delete)

    @QtCore.Slot(flow.TextField)
    def _handle_text_field_created(self, text_field):
        text_view = TextFieldView(text_field)
        self._text_field_views.insert(0, text_view)
        self._nodes[text_field] = text_view
        self._scene.addItem(text_view)
        self._node_signals.connect(
            text_field,
            text_view.cut_requested[ElementViewInterface],
            self.handle_cut)
        self._node_signals.connect(
            text_field,
            text_view.copy_requested[ElementViewInterface],
            self.handle_copy_from_node)
        self._node_signals.connect(
            text_field,
            text_view.delete_requested[ElementViewInterface],
            self.handle_delete)
        set_selected(text_field, text_view)
        self._node_signals.connect(
            text_field,
            text_view.request_reorder,
            self._handle_text_field_order)
        self._handle_text_field_order(None)

    # @QtCore.Slot(str)
    # Issue where sender always is None,
    # see TextFieldView._handle_color_changed
    def _handle_text_field_order(self, direction):
        if len(self._text_field_views) <= 1:
            return
        if direction:
            cmd = user_commands.TextFieldOrderCommand(
                self._model, self.sender()._model, direction)
            self._model.undo_stack().push(cmd)
        else:
            self._model.reorder_text_fields()

    @QtCore.Slot(flow.TextField)
    def _handle_text_field_removed(self, text_field):
        text_view = self._nodes[text_field]
        del self._text_field_views[self._text_field_views.index(text_view)]
        self._handle_node_removed(text_field)

    def _handle_route_point_added(self, route_point):
        route_point_view = RoutePointView(route_point)
        assert route_point not in self._nodes
        self._route_point_views.append(route_point_view)
        self._nodes[route_point] = route_point_view
        self._scene.addItem(route_point_view)

        self._node_signals.connect(
            route_point,
            route_point_view.delete_requested[ElementViewInterface],
            self.handle_delete)

        self._node_signals.connect(
            route_point,
            route_point_view.cut_requested[ElementViewInterface],
            self.handle_cut)

        self._node_signals.connect(
            route_point,
            route_point_view.copy_requested[ElementViewInterface],
            self.handle_copy_from_node)

        set_selected(route_point, route_point_view)

    def _handle_route_point_removed(self, route_point):
        route_point_view = self._nodes[route_point]
        self._route_point_views.remove(route_point_view)
        self._handle_node_removed(route_point)

    @QtCore.Slot(flow.NodeInterface)
    def _handle_node_created(self, node):
        assert node not in self._nodes
        user_statistics.user_created_node(node)
        node_view = NodeView(node)
        self._common_node_creation(node, node_view)
        self._node_signals.connect(
            node, node_view.create_subflow_from_selection_requested,
            self._handle_create_subflow_from_selection_requested)
        self._node_signals.connect(
            node, node_view.help_requested[str],
            self.help_requested[str])

    @QtCore.Slot(flow.NodeInterface)
    def _handle_node_removed(self, node):
        self.blockSignals(True)
        node_view = self._nodes[node]
        self._node_signals.disconnect_all(node)
        if node_view:
            node_view.remove()
            if node_view in self._scene.items():
                self._scene.removeItem(node_view)
            del self._nodes[node]
            if node_view in self._node_views:
                del self._node_views[self._node_views.index(node_view)]
        self.blockSignals(False)

    @QtCore.Slot(flow.NodeInterface)
    def _handle_subflow_created(self, subflow):
        assert subflow not in self._nodes
        user_statistics.user_created_subflow(subflow)
        subflow_view = SubflowView(subflow)
        self._subflow_views.append(subflow_view)
        self._subflows[subflow] = subflow_view
        self._nodes[subflow] = subflow_view
        self._node_views.append(subflow_view)
        self._scene.addItem(subflow_view)

        self._node_signals.connect(
            subflow, subflow_view.connection_start_requested[object],
            self._handle_connection_start_requested)
        self._node_signals.connect(
            subflow, subflow_view.connection_end_requested[object],
            self._handle_connection_end_requested)
        self._node_signals.connect(
            subflow, subflow_view.open_add_context_requested[
                QtWidgets.QGraphicsSceneMouseEvent],
            self._handle_add_context_requested)
        self._node_signals.connect(
            subflow, subflow_view.edit_subflow_requested[flow.Flow],
            self.edit_subflow_requested)
        self._node_signals.connect(
            subflow, subflow_view.help_requested[str],
            self.help_requested[str])

        self._node_signals.connect(
            subflow,
            subflow_view.cut_requested[ElementViewInterface],
            self.handle_cut)
        self._node_signals.connect(
            subflow,
            subflow_view.copy_requested[ElementViewInterface],
            self.handle_copy)
        self._node_signals.connect(
            subflow,
            subflow_view.delete_requested[ElementViewInterface],
            self.handle_delete)

        self._node_signals.connect(
            subflow,
            subflow_view.create_subflow_from_selection_requested,
            self._handle_create_subflow_from_selection_requested)

        set_selected(subflow, subflow_view)

    @QtCore.Slot(flow.NodeInterface)
    def _handle_subflow_removed(self, subflow):
        subflow_view = self._nodes[subflow]
        del self._subflows[subflow]
        del self._subflow_views[self._subflow_views.index(subflow_view)]
        self._handle_node_removed(subflow)

    @QtCore.Slot(object)
    def _handle_connection_start_requested(self, port_view):
        self._transient_connection = TransientConnectionView(
            port_view.connection_position(), parent=self)
        self.scene().addItem(self._transient_connection)
        self._source_port = port_view.model
        if port_view.model.type == flow.Type.OutputPort:
            for node_view in self._node_views:
                for input_ in node_view.input_port_views():
                    input_.highlight(self._model.connection_is_allowed(
                        self._source_port, input_.model))
        elif port_view.model.type == flow.Type.InputPort:
            for node_view in self._node_views:
                for output_ in node_view.output_port_views():
                    output_.highlight(self._model.connection_is_allowed(
                        output_.model, self._source_port))

    @QtCore.Slot(object)
    def _handle_connection_end_requested(self, port_view):
        source_port = self._source_port
        self._remove_transient_connection()
        if port_view and port_view.model and self._source_port:
            source, destination = flow.connection_direction(
                self._source_port, port_view.model)
            cmd = user_commands.CreateConnectionCommand(
                source, destination, self._model)
            self._model.undo_stack().push(cmd)

            user_statistics.user_created_connection(
                source, destination)

            self._source_port = None
        for node_view in self._node_views:
            for input_ in node_view.input_port_views():
                if input_.model is not source_port:
                    input_.highlight(False)
            for output_ in node_view.output_port_views():
                if output_.model is not source_port:
                    output_.highlight(False)

    @QtCore.Slot(QtWidgets.QGraphicsSceneMouseEvent)
    def _handle_add_context_requested(self, event=None):
        self.normal_edit()
        start_port = None
        if event is None:
            pos = QtGui.QCursor.pos()
            view_pos = self.mapFromGlobal(pos)
            scene_pos = self.mapToScene(view_pos)
            view_port_rect = self.viewport().rect()
            if not view_port_rect.contains(view_pos):
                scene_pos = self.mapToScene(view_port_rect.center())
            scene_pos.setX(int(round(scene_pos.x() / 25) * 25) - 25)
            scene_pos.setY(int(round(scene_pos.y() / 25) * 25) - 25)
        else:
            start_port = self._source_port
            scene_pos = event.scenePos()

        view_rect = self.rect()
        settings_ = settings.instance()
        popup_position = settings_['Gui/quickview_popup_position']

        if self._transient_connection is not None or event is None:
            dialog = library_view.QuickSearchDialog(
                self._app_core.library_root(), self._model, start_port,
                scene_pos, 'Search for nodes:', self)
            dialog.show()
            dialog.adjustSize()

            if popup_position == 'center':
                x_pos = view_rect.center().x() - dialog.width() / 2.
            elif popup_position == 'left':
                x_pos = view_rect.width() * 0.05
            else:
                x_pos = view_rect.width() * 0.95 - dialog.width()

            popup_pos = self.mapToGlobal(QtCore.QPoint(
                x_pos, view_rect.top() + view_rect.height() * 0.05))
            dialog.move(popup_pos)
            dialog.resize(dialog.width(), view_rect.height() * 0.9)
            dialog.focus_filter()
            dialog.show()
            dialog.item_accepted.connect(self._handle_close_add_context)
            dialog.rejected.connect(functools.partial(
                self._handle_connection_end_requested, None))

    @QtCore.Slot(object, object, QtCore.QPointF)
    def _handle_close_add_context(self, result, start_port, position):
        if isinstance(result, library.LibraryNode):
            node_identifier = result.node_identifier
            if start_port is not None:
                # subtract 50 from x position if node gets connected from input
                if start_port.type == flow.Type.InputPort:
                    position.setX(position.x() - 50)
                # approx. fix the y offset of the port and "snap" node to grid
                position.setX(int(round(position.x() / 25) * 25))
                position.setY(int(round(position.y() / 25) * 25) - 25)
            grid.instance().snap_to_grid(position)
            cmd = user_commands.CreateLibraryElementCommand(
                node_id=node_identifier, position=position, flow=self._model)
            self._model.undo_stack().push(cmd)
            node = cmd.created_element()
            # that is a very hackish way, timer could be too short
            # TODO: better implementation to make sure the function is only
            # called after the _handle_node_created slot was called
            if start_port is not None:
                QtCore.QTimer.singleShot(5, functools.partial(
                    self._handle_add_connection_to_node, node, start_port))
        else:
            self._handle_connection_end_requested(None)

    @QtCore.Slot(object, object)
    def _handle_add_connection_to_node(self, node, start_port):
        node_view = self._nodes[node]
        if start_port.type == flow.Type.InputPort:
            port_views = node_view.output_port_views()
        elif start_port.type == flow.Type.OutputPort:
            port_views = node_view.input_port_views()

        for port_view in port_views:
            end_port = port_view.model
            if end_port.datatype.match(start_port.datatype):
                self._handle_connection_end_requested(port_view)
                return

    @QtCore.Slot(flow.Connection)
    def _handle_connection_created(self, connection):
        start_node = self._nodes[connection.source.node]
        end_node = self._nodes[connection.destination.node]
        start_port = start_node.output_port_view(connection.source)
        end_port = end_node.input_port_view(connection.destination)
        connection_view = ConnectionView(connection,
                                         start_port.connection_position(),
                                         end_port.connection_position(),
                                         parent=self)
        self._scene.addItem(connection_view)
        self._connections[connection] = connection_view
        self._node_signals.connect(
            connection, start_port.position_changed[QtCore.QPointF],
            connection_view.set_start_position)
        self._node_signals.connect(
            connection, end_port.position_changed[QtCore.QPointF],
            connection_view.set_end_position)
        self._node_signals.connect(
            connection, self.selection_changed,
            connection_view.selection_changed)
        self._node_signals.connect(
            connection,
            connection_view.delete_requested[ElementViewInterface],
            self.handle_delete)

        for route_point in connection.route_points:
            self._handle_route_point_added(route_point)

        # self._update_all_ports()

    @QtCore.Slot(flow.Connection)
    def _handle_connection_removed(self, connection):
        connection_view = self._connections[connection]
        for route_point in connection.route_points:
            self._handle_route_point_removed(route_point)

        self._node_signals.disconnect_all(connection)

        if connection_view in self._scene.items():
            self._scene.removeItem(connection_view)
        del self._connections[connection]
        # self._update_all_ports()

    # def _update_all_ports(self):
    #     for node in self._node_views:
    #         for port in itertools.chain(node.input_port_views(),
    #                                     node.output_port_views()):
    #             port.notify_position_changed()

    @QtCore.Slot(flow.FlowInput)
    def _handle_flow_input_created(self, flow_input):
        input_view = FlowInputView(flow_input)
        self._common_node_creation(flow_input, input_view)

    @QtCore.Slot(flow.FlowInput)
    def _handle_flow_input_removed(self, flow_input):
        self._handle_node_removed(flow_input)

    @QtCore.Slot(flow.FlowOutput)
    def _handle_flow_output_created(self, flow_output):
        output_view = FlowOutputView(flow_output)
        self._common_node_creation(flow_output, output_view)

    @QtCore.Slot(flow.FlowOutput)
    def _handle_flow_output_removed(self, flow_output):
        self._handle_node_removed(flow_output)

    @QtCore.Slot()
    def _handle_create_subflow_from_selection_requested(self):
        selected_items = self.scene().selectedItems()
        if len(selected_items) == 0:
            return
        # if any node is executing => return

        element_list = filter_nodes_to_model(selected_items)
        # Never include any IO-ports when creating a sub-flow.
        element_list = [e for e in element_list if e.type not in (
            flow.Type.FlowInput, flow.Type.FlowOutput, flow.Type.RoutePoint)]
        positions = [n.sceneBoundingRect().center() for n in selected_items
                     if n.model in element_list]

        x_mean = sum([p.x() for p in positions]) / len(positions)
        y_mean = sum([p.y() for p in positions]) / len(positions)

        cmd = user_commands.CreateSubflowFromSelectionCommand(
            QtCore.QPointF(x_mean, y_mean), element_list, self._model)
        self._model.undo_stack().push(cmd)

    def _get_selected_items(self, node=None):
        selected_items = self.scene().selectedItems()
        if len(selected_items) == 0:
            if node:
                selected_items = [node]
            else:
                return []
        return selected_items

    def _handle_copy(self, node=None):
        selected_items = self._get_selected_items(node)
        element_list = filter_nodes_to_model(selected_items)
        if element_list:
            user_commands.copy_element_list_to_clipboard(
                self._model, element_list)

    @QtCore.Slot(ElementViewInterface)
    def handle_copy_from_node(self, node):
        self._handle_copy(node)

    @QtCore.Slot()
    def handle_copy(self):
        self._handle_copy()

    @QtCore.Slot(list)
    def select_movables(self, elements):
        for element in elements:
            movable = self._nodes.get(element)
            if movable:
                movable.setSelected(True)

    @QtCore.Slot()
    def handle_paste_at_context_menu(self):
        self._handle_paste(self._cursor_point())

    def _visible_area(self):
        return QtCore.QRectF(
            self.mapToScene(0, 0),
            self.mapToScene(self.viewport().width(), self.viewport().height()))

    @QtCore.Slot()
    def handle_paste_at_cursor(self):
        top_right = self.mapToScene(self.mapFromGlobal(QtGui.QCursor.pos()))
        size = self._model.size
        center = top_right - QtCore.QPointF(size.height() / 2,
                                            size.width() / 2)
        rect = self._visible_area()
        rect.translate(-25, -25)  # The rectangle is offset for unknon reason.
        if rect.contains(center):
            self._handle_paste(center)
            self.zoom_fit_paste()

    @QtCore.Slot()
    def _handle_paste(self, pos):
        """
        Paste elements from clipboard at pos.

        Parameters
        ----------
        pos : QtCore.QPointF
            Position (in scene coordinates) where the elements in
            clipboard should be pasted.
        """
        clipboard = QtWidgets.QApplication.clipboard()
        data = clipboard.mimeData()
        if data.hasFormat(appcore.AppCore.mime_type_flow()):
            command = user_commands.PasteElementListCommand(
                self._model,
                str(data.data(appcore.AppCore.mime_type_flow()).data(),
                    'ascii'),
                pos, self._app_core)
            self._model.undo_stack().push(command)
            created_elements = command.created_top_level_elements()
            self._scene.clearSelection()
            self.select_movables(created_elements)
        else:
            core_logger.error('Unhandled Mime type...')

    def _selected_items_to_remove(self, node):
        selection = self._get_selected_items(node)
        selected_items = filter_nodes_to_model(
            selection, filter_valid_structural_change=True)

        if not selected_items:
            # Only connections selected:
            selected_items = filter_model_types(
                elements_models(selection),
                [flow.Type.Connection])
        else:
            if not all(
                    s.type == flow.Type.RoutePoint
                    for s in selected_items):
                selected_items = remove_model_types(
                    selected_items, [flow.Type.RoutePoint])
        return selected_items

    def _handle_cut(self, node=None):
        selected_items = self._selected_items_to_remove(node)

        if selected_items:
            self._model.undo_stack().push(user_commands.CutElementListCommand(
                self._model, selected_items, self._cursor_point()))

    @QtCore.Slot()
    def handle_cut(self):
        self._handle_cut()

    @QtCore.Slot(ElementViewInterface)
    def handle_cut_from_node(self, node):
        self._handle_cut(node)

    def _handle_delete(self, node=None):
        selected_items = self._selected_items_to_remove(node)
        if not selected_items:
            return

        dirty_subflows = []
        for item in selected_items:
            if (item.type == flow.Type.Flow and item.is_linked
                    and not item.subflows_are_clean()):
                dirty_subflows.append(item)
        if dirty_subflows:
            try:
                common.ask_about_saving_flows(
                    dirty_subflows, include_root=True, discard=True)
            except common.SaveCancelled:
                return

        self._model.undo_stack().push(
            user_commands.RemoveElementListCommand(
                selected_items, self._model))

    @QtCore.Slot()
    def handle_delete(self):
        self._handle_delete()

    @QtCore.Slot(ElementViewInterface)
    def handle_delete_from_node(self, node):
        self._handle_delete(node)

    def handle_selection_tool(self):
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    def handle_panning_tool(self):
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    @QtCore.Slot()
    def handle_stop(self):
        self._model.abort()

    @QtCore.Slot()
    def handle_reload(self):
        self._model.reload()

    @QtCore.Slot()
    def handle_execute_all(self):
        self._model.execute_node(None)

    def event(self, event):
        event_type = event.type()
        if event_type == QtCore.QEvent.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

    def focusOutEvent(self, event):
        self._end_pan()

    def wheelEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            self.setTransformationAnchor(
                QtWidgets.QGraphicsView.AnchorViewCenter)
            if event.delta() > 0:
                # Zoom in
                self.scale(1.1, 1.1)
            else:
                # Zoom out
                self.scale(0.9, 0.9)
            event.accept()
            return True
        else:
            event.ignore()
            return super(FlowView, self).wheelEvent(event)

    def gestureEvent(self, event):
        pinch = event.gesture(QtCore.Qt.PinchGesture)
        if pinch.state() == QtCore.Qt.GestureUpdated:
            scale_delta = 1.0 + pinch.scaleFactor() - pinch.lastScaleFactor()
            self.setTransformationAnchor(
                QtWidgets.QGraphicsView.AnchorViewCenter)
            self.scale(scale_delta, scale_delta)
            tr = self.transform()
            if tr.m11() < 0:
                tr.setMatrix(-tr.m11(), 0, 0, 0, -tr.m22(), 0, 0, 0, 1)
                self.setTransform(tr)
        event.accept(QtCore.Qt.PinchGesture)
        return True

    def drawBackground(self, painter, rect):
        theme = themes.get_active_theme()
        painter.fillRect(rect, theme.background_color)

        view = self._visible_area()
        offset = view.width() / (len(self._renderers) + 1)
        svg_view = QtCore.QRectF(0, 0, offset, offset)
        svg_view.moveCenter(view.center())
        svg_view.moveLeft(view.left() + offset / 2)

        painter.save()
        painter.setOpacity(0.1)

        for renderer in self._renderers:
            renderer.render(painter, svg_view)
            svg_view.translate(offset, 0)

        painter.restore()

        if grid.instance().enabled:
            painter.setWorldMatrixEnabled(True)
            scale = self.transform().m11()
            if scale < 0.2:
                return
            painter.setPen(
                QtGui.QPen(theme.grid_color,
                           0.4 / scale, QtCore.Qt.SolidLine))

            spacing = int(grid.instance().spacing)
            x = math.floor(rect.left() / spacing) * spacing
            top, bottom = rect.top(), rect.bottom()
            left, right = rect.left(), rect.right()
            for x in range(int(left / spacing) * spacing,
                           int(right), spacing):
                painter.drawLine(x, top, x, bottom)
            for y in range(int(top / spacing) * spacing,
                           int(bottom), spacing):
                painter.drawLine(left, y, right, y)

    def _handle_zoom_to_node(self, node):
        self._scene.clearSelection()
        try:
            node_view = self._nodes[node]
        except KeyError:
            return
        node_view.setSelected(True)
        self.zoom_fit_selection()

    def _limit_zoom(self):
        # Limit zoom to maximum "normal" size.
        if self.transform().m11() > 1.0:
            transform_ = self.transform()
            old_scale = transform_.m11()
            transform_.scale(1.0 / old_scale, 1.0 / old_scale)
            self.setTransform(transform_)

    @QtCore.Slot()
    def zoom_fit_all(self):
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        rect = self._scene.itemsBoundingRect()
        self.fitInView(rect, QtCore.Qt.KeepAspectRatio)
        self._limit_zoom()

    @QtCore.Slot()
    def zoom_in(self):
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.scale(1.1, 1.1)

    @QtCore.Slot()
    def zoom_out(self):
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.scale(0.9, 0.9)

    @QtCore.Slot()
    def zoom_restore(self):
        transform = self.transform()
        transform.reset()
        self.setTransform(transform)

    def _zoom_fit(self, items):
        if len(items) == 0:
            return
        r = items[0]
        for i in items:
            r = r.united(i)
        self.fitInView(r, QtCore.Qt.KeepAspectRatio)
        self._limit_zoom()

    def _selected_items(self):
        return [i.sceneBoundingRect() for i in self.scene().selectedItems()
                if not isinstance(i, ConnectionView)]

    @QtCore.Slot()
    def zoom_fit_paste(self):
        rect = self._visible_area()
        items = [i for i in self._selected_items() if not rect.contains(i)]
        if len(items):
            self._zoom_fit(items + [rect])

    @QtCore.Slot()
    def zoom_fit_selection(self):
        self._zoom_fit(self._selected_items())

    @QtCore.Slot()
    def select_all(self):
        for view in itertools.chain(self._node_views,
                                    self._subflow_views,
                                    self._text_field_views,
                                    self._route_point_views):
            view.setSelected(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(self._app_core.mime_type_node()):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def dragMoveEvent(self, event):
        super(FlowView, self).dragMoveEvent(event)
        event.acceptProposedAction()

    def dropEvent(self, event):
        position = grid.instance().snap_to_grid(self.mapToScene(event.pos()))
        if (event.mimeData().hasFormat(self._app_core.mime_type_node()) and not
           (event.isAccepted() and self._scene_.itemAt(
               position, QtGui.QTransform()))):
            node_identifier = json.loads(
                str(event.mimeData().data(
                    self._app_core.mime_type_node()).data(), 'ascii'))[0]

            event.setAccepted(True)
            cmd = user_commands.CreateLibraryElementCommand(
                node_id=node_identifier, position=position, flow=self._model)
            self._model.undo_stack().push(cmd)
        else:
            event.setAccepted(False)

    @QtCore.Slot()
    def _handle_selection_changed(self):
        # Ensure that items with changed selection are redrawn.
        self.selection_changed.emit()
        # Find first selected node to show the corresponding active output.
        first_selected_node = [n for n in self.scene().selectedItems()
                               if isinstance(n, NodeView)]
        if len(first_selected_node) > 0:
            self.selected_nodes_changed.emit(first_selected_node[0].model)
        else:
            self.selected_nodes_changed.emit(None)

    def contextMenuEvent(self, event):
        if self.itemAt(event.pos()):
            super().contextMenuEvent(event)
        else:
            clipboard = QtWidgets.QApplication.clipboard()
            data = clipboard.mimeData()
            pos = self.mapToGlobal(event.pos())
            mime_type_flow = appcore.AppCore.mime_type_flow()
            self._paste_action.setEnabled(data.hasFormat(mime_type_flow))
            self._context_menu_pos = self.mapToScene(event.pos())
            self._enable_actions()
            self._settings_action.setEnabled(self._model.is_configurable())
            self._context_menu.exec_(pos)

    @QtCore.Slot(bool)
    def toggle_insert_text_field(self, enable):
        if enable:
            self.insert_text_field()
        else:
            self.normal_edit()

    @QtCore.Slot()
    def insert_text_field(self):
        self.inserting_text_field.emit()

    def _on_insert_text_field(self):
        self.set_flow_cursor(QtCore.Qt.CrossCursor)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    @QtCore.Slot()
    def insert_node_via_popup(self):
        self._handle_add_context_requested()

    @QtCore.Slot()
    def normal_edit(self):
        self.normal_editing.emit()

    def _on_normal_edit(self):
        self.set_flow_cursor()
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    @property
    def is_inserting_text_field(self):
        return (self._insert_text_field_state in
                self._state_machine.configuration())

    @property
    def is_moving(self):
        return False

    def _start_pan(self, pos):
        self._pan_pos = pos
        self.set_flow_cursor(QtCore.Qt.ClosedHandCursor)

    def _move_pan(self, pos):
        offset = self._pan_pos - pos
        self._pan_pos = pos
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().value() + offset.y())
        self.horizontalScrollBar().setValue(
            self.horizontalScrollBar().value() + offset.x())

    def _end_pan(self):
        self._pan_pos = None
        self.set_flow_cursor()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.is_inserting_text_field:
                self._text_field_start_pos = self.mapToScene(event.pos())
        elif event.button() == QtCore.Qt.RightButton:
            if self._transient_connection:
                self._handle_connection_end_requested(None)
            else:
                # If right mouse button was pressed on an unselected item,
                # select the item and deselect everything else.
                item = self.itemAt(event.pos())
                if item is not None:
                    # We have to go through one or more parents to find the
                    # actual owner of the data model for the item.
                    while item.parentItem() is not None:
                        item = item.parentItem()
                    # If the item is not selected we deselect everything else
                    # and only select the item itself.
                    if item is not None and not item.isSelected():
                        self.scene().clearSelection()
                        item.setSelected(True)
                        self._handle_selection_changed()
                # In this case we need a workaround for Qt deselecting all
                # items. See https://bugreports.qt.io/browse/QTBUG-10138
                # for details.
                event.accept()
                return
        elif event.button() == QtCore.Qt.MidButton:
            self._start_pan(event.pos())
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._transient_connection:
            self._transient_connection.set_end_position(
                self.mapToScene(event.pos()))
        if self._pan_pos is not None:
            if event.buttons() & QtCore.Qt.MidButton:
                self._move_pan(event.pos())
            else:
                self._end_pan()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self._end_pan()
        super().mouseReleaseEvent(event)

        if self.is_inserting_text_field:
            pos1 = grid.instance().snap_to_grid(self._text_field_start_pos)
            pos2 = grid.instance().snap_to_grid(self.mapToScene(event.pos()))
            top, bottom = sorted([pos1.y(), pos2.y()])
            left, right = sorted([pos1.x(), pos2.x()])
            width = max(right - left, 100)
            height = max(bottom - top, 50)

            self._model.undo_stack().push(
                user_commands.CreateTextFieldCommand(
                    QtCore.QRect(left, top, width, height), self._model))

            self._text_field_start_pos = QtCore.QPoint(0, 0)
            self.normal_edit()

    def set_flow_cursor(self, cursor=None):
        """
        Set a cursor for the entire flow view. This will override any
        current item cursor. Omitting the cursor argument or passing None means
        that the default cursor is used.

        Cursors in the flow area should only be set with this method or
        set_item_cursor. Setting it directly with setCursor can result in
        the cursor not updating.
        """
        self._flow_cursor = cursor
        self._update_cursor()

    def set_item_cursor(self, cursor=None):
        """
        Set the cursor for the currently hovered item. The item is responsible
        for resetting this to the default cursor again. Omitting the cursor
        argument or passing None means that the default cursor is used.

        Cursors in the flow area should only be set with this method or
        set_flow_cursor. Setting it directly with setCursor can result in
        the cursor not updating.
        """
        self._item_cursor = cursor
        self._update_cursor()

    def _update_cursor(self):
        if self._flow_cursor is not None:
            new_cursor = self._flow_cursor
        elif self._item_cursor is not None:
            new_cursor = self._item_cursor
        else:
            new_cursor = QtCore.Qt.ArrowCursor
        self.setCursor(new_cursor)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self._handle_connection_end_requested(None)
        return super().keyPressEvent(event)

    def _remove_transient_connection(self):
        if self._transient_connection is not None:
            self.scene().removeItem(self._transient_connection)
            self._transient_connection = None

    @QtCore.Slot()
    def preferences_updated(self):
        settings_ = settings.instance()
        grid.instance().reload_settings()
        self.update()


class FlowScene(QtWidgets.QGraphicsScene):
    """Scene holding all the items"""

    def __init__(self, flow_view=None):
        super(FlowScene, self).__init__(flow_view)
        self._minimum_size = QtCore.QRectF(0, 0, 4000, 4000)
        self.setSceneRect(self._minimum_size)
        self._last_change = None
        self.changed.connect(self._adjust_scene_size)
        self._view = flow_view

    def remove(self):
        self.changed.disconnect(self._adjust_scene_size)

    def flow_view(self):
        return self._view

    def _adjust_scene_size(self):
        t = time.monotonic()
        if self._last_change is not None and t - self._last_change < 1.0:
            return
        self._last_change = t
        try:
            bounding_rect = self.itemsBoundingRect()
        except Exception:
            # Workaround for rare crash when resizing a loaded flow.
            # See issue #2007.
            return
        scene_rect = self.sceneRect()
        shrink_rect = scene_rect.adjusted(
            200, 200, -200, -200).united(self._minimum_size)
        grow_rect = scene_rect.adjusted(100, 100, -100, -100)
        if shrink_rect.contains(bounding_rect):
            self.setSceneRect(shrink_rect)
        elif not grow_rect.contains(bounding_rect):
            self.setSceneRect(
                scene_rect.adjusted(-100, -100, 100, 100).united(
                    bounding_rect))
