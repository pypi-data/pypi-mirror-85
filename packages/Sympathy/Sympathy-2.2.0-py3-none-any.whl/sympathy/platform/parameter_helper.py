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
import logging
import datetime
import json
from collections import OrderedDict

from sympathy.platform import exceptions
from sympathy.utils.event import Event
from sympathy.utils.context import deprecated_warn
from sympathy.platform import state
from sympathy.platform.exceptions import sywarn
from sympathy.utils.prim import combined_key, parse_isoformat_datetime


node_logger = logging.getLogger('node')


class ParameterEntity(object):
    __slots__ = ('_name', '_parameter_dict', 'value_changed')

    def __init__(self, parameter_dict, name, ptype,
                 label=None, description=None, order=None,
                 state_settings=None, gui_visitor=None, **kwargs):
        super(ParameterEntity, self).__init__()
        self._state_settings = (state.node_state().settings
                                if state_settings is None
                                else state_settings)
        self._gui_visitor = gui_visitor
        self._parameter_dict = parameter_dict
        binding = kwargs.get('binding')
        if binding is not None:
            self._binding = binding

        self.name = name
        self.type = ptype
        if order is not None:
            self.order = order
        if label is not None:
            self.label = label
        if description is not None:
            self.description = description
        self.value_changed = Event()

    @property
    def parameter_dict(self):
        return self._parameter_dict

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._parameter_dict['type']

    @type.setter
    def type(self, ptype):
        self._parameter_dict['type'] = ptype

    @property
    def label(self):
        try:
            return self._parameter_dict['label']
        except KeyError:
            return ""

    @label.setter
    def label(self, label):
        self._parameter_dict['label'] = label

    @property
    def description(self):
        try:
            return self._parameter_dict['description']
        except KeyError:
            return ""

    @description.setter
    def description(self, description):
        self._parameter_dict['description'] = description

    @property
    def order(self):
        try:
            return self._parameter_dict['order']
        except KeyError:
            return None

    @order.setter
    def order(self, order):
        self._parameter_dict['order'] = order

    def gui(self):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self.accept(self._gui_visitor)

    def as_dict(self):
        raise NotImplementedError("Must extend this method!")

    def adjust(self, names):
        raise NotImplementedError("adjust is not defined for this type.")

    def equal_to(self, other, as_stored=False):
        """
        Parameters
        ----------
        other: ParameterEntity
            Parameter to compare for equality against self.
        as_stored : bool
            Compare the parameters as they are stored in a .syx file.
            This removes descriptions and other fields that are not considered
            part of the value from the comparison.

        Returns
        -------
        bool
            True if two parameters are equal and False otherwise.
        """
        if as_stored:
            return (
                self.type == other.type and
                self._binding == other._binding)
        else:
            raise NotImplementedError

    def _set_from_parameters(*args, **kwargs):
        raise NotImplementedError

    @property
    def _binding(self):
        return self._parameter_dict.get('binding')

    @_binding.setter
    def _binding(self, value):
        if value is None:
            self._parameter_dict.pop('binding', None)
        else:
            self._parameter_dict['binding'] = value


class ParameterValue(ParameterEntity):
    """docstring for ParameterValue"""
    __slots__ = ('_parameter_dict',)
    _type = None

    def __init__(self, parameter_dict, name, ptype, value,
                 editor=None, **kwargs):
        super(ParameterValue, self).__init__(
            parameter_dict, name, ptype, **kwargs)
        self._parameter_dict = parameter_dict
        self.value = value
        self.editor = editor

    def _check_value_type(self, value):
        if self._type:
            if value is not None and not isinstance(value, self._type):
                if isinstance(value, int) and self._type is float:
                    return
                name = self.name or 'parameter'
                node_logger.warning(
                    'Mismatched type: value of %s parameter "%s" is %s (%s).',
                    self._type.__name__, name, repr(value),
                    type(value).__name__)

    @property
    def value(self):
        return self._parameter_dict['value']

    @value.setter
    def value(self, value):
        self._check_value_type(value)
        self._parameter_dict['value'] = value
        self.value_changed.emit()

    @property
    def editor(self):
        return self._parameter_dict['editor']

    @editor.setter
    def editor(self, item):
        if isinstance(item, Editor):
            item = item.value()
        self._parameter_dict['editor'] = item

    def as_dict(self):
        return ({
            "type": self.type,
            "value": self.value})

    def __str__(self):
        return str({
            "type": self.type,
            "value": self.value})

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            self.value == other.value)

    def _adjust_scalar_combo(self, values):
        if self.editor and self.editor['type'] == 'combobox':
            include_empty = self.editor.get('include_empty', False)
            if isinstance(values, dict):
                options = list(values.keys())
                display = list(values.values())
            else:
                display = None
                options = list(values)
            if include_empty:
                options.insert(0, '')
                if display is not None:
                    display.insert(0, '')
            self.editor['options'] = options
            self.editor['display'] = display

    def _set_from_parameters(self, *args, value=None, **kwargs):
        self.value = value


class ParameterInteger(ParameterValue):
    _type = int

    def __init__(self, parameter_dict, name, value=0, **kwargs):
        super(ParameterInteger, self).__init__(
            parameter_dict, name, "integer", value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_integer(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)


class ParameterFloat(ParameterValue):
    _type = float

    def __init__(self, parameter_dict, name, value=0, **kwargs):
        super(ParameterFloat, self).__init__(
            parameter_dict, name, "float", value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_float(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)


class ParameterString(ParameterValue):
    _type = str

    def __init__(self, parameter_dict, name, value="", **kwargs):
        super(ParameterString, self).__init__(
            parameter_dict, name, "string", value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_string(self)

    def adjust(self, values):
        self._adjust_scalar_combo(values)


class ParameterBoolean(ParameterValue):
    _type = bool

    def __init__(self, parameter_dict, name, value=False, **kwargs):
        super(ParameterBoolean, self).__init__(
            parameter_dict, name, "boolean", value, **kwargs)

    def accept(self, visitor):
        return visitor.visit_boolean(self)


class ParameterDateTime(ParameterValue):
    _type = datetime.datetime

    def __init__(self, parameter_dict, name, value=False, from_definition=True,
                 **kwargs):
        if not from_definition:
            value = parse_isoformat_datetime(value)
        super(ParameterDateTime, self).__init__(
            parameter_dict, name, "datetime", value, from_definition=True,
            **kwargs)

    @property
    def value(self):
        return parse_isoformat_datetime(self._parameter_dict['value'])

    @value.setter
    def value(self, value):
        self._check_value_type(value)
        self._parameter_dict['value'] = value.isoformat()
        self.value_changed.emit()

    def accept(self, visitor):
        return visitor.visit_datetime(self)

    def _set_from_parameters(cls, *args, value=None, from_definition=True,
                             **kwargs):
        if not from_definition:
            value = parse_isoformat_datetime(value)
        return super(ParameterDateTime, cls)._set_from_parameters(
            *args, value=value, from_definition=from_definition, **kwargs)


class ParameterJson(ParameterValue):
    _type = object

    def __init__(self, parameter_dict, name, value=None, **kwargs):
        super(ParameterJson, self).__init__(
            parameter_dict, name, "json", value, **kwargs)

    @property
    def editor(self):
        return self._parameter_dict.get('editor')

    @editor.setter
    def editor(self, item):
        if isinstance(item, Editor):
            item = item.value()
        self._parameter_dict['editor'] = item

    def accept(self, visitor):
        return visitor.visit_json(self)

    def adjust(self, values):
        pass

    def equal_to(self, other, as_stored=False):
        return (
            super(ParameterValue, self).equal_to(
                other, as_stored=as_stored) and
            json.loads(json.dumps(self.value)) == json.loads(
                json.dumps(other.value)))


class ParameterList(ParameterEntity):
    """ParameterList"""
    # Only for access by views.
    _mode_selected = 'selected'
    _mode_selected_exists = 'selected_exists'
    _mode_unselected = 'unselected'
    _mode_passthrough = 'passthrough'

    def __init__(self, parameter_dict, name, plist=None, value=None,
                 from_definition=True, editor=None, **kwargs):
        super().__init__(parameter_dict, name, 'list', **kwargs)
        self.editor = editor
        self._multiselect_mode = kwargs.get('mode', self._mode_selected)
        self._passthrough = kwargs.pop('passthrough', False)
        if kwargs.pop('_old_list_storage', False):
            self._parameter_dict['_old_list_storage'] = True

        list_ = kwargs.get('list')
        if from_definition:
            if plist is not None and list_ is not None:
                raise ValueError(
                    "Only one of the arguments 'list' and 'plist' may be "
                    "used at a time.")
            elif plist is None:
                plist = list_ or []
            if not isinstance(plist, list):
                plist = list(plist)
            self._parameter_dict['list'] = plist
        else:
            self._parameter_dict['list'] = list_

        value_names = kwargs.get('value_names')
        if from_definition:
            if value is None and value_names is None and self.list:
                # When a list has been specified, but neither value nor
                # value_names are specified, select first element. This is
                # for backwards compatibility.
                value = [0]
            if value is not None and value_names is not None:
                sywarn("Only one of the arguments 'value' and 'value_names' "
                       "may be used at a time")
            if value_names:
                value = [self.list.index(v)
                         for v in value_names if v in self.list]
            elif value:
                try:
                    value_names = [self.list[i] for i in value]
                except IndexError:
                    value = []
                    value_names = []
            else:
                value = []
                value_names = []
            self._parameter_dict['value'] = value
            self._parameter_dict['value_names'] = value_names
        else:
            if value:
                try:
                    value_names_ = [self.list[i] for i in value]
                except IndexError:
                    value_names_ = None
                except TypeError:
                    value_names_ = None
                    value = []
                # Choose value_names_ only if value_names is empty
                if value_names_ and not value_names:
                    value_names = value_names_
                else:
                    value = [self.list.index(v)
                             for v in value_names if v in self.list]
            self._parameter_dict['value'] = value
            self._parameter_dict['value_names'] = value_names


    def selected_names(self, names):
        """
        Return the selected names depending on the multselect mode,
        the actual selection (self.value_names) and the supplied names.

        names should be a list or iterable containing the relevant
        names. Typically this would be the names that are used to
        set self.list in adjust_parameters, the argument makes it
        possible to return different names when iterating over a
        structure where the relevant names change.
        """
        res = []
        if self._multiselect_mode == self._mode_selected:
            res = self.value_names
            missing = set(res).difference(names)
            if missing:
                name = self.label or self.name
                raise exceptions.SyDataError(
                    'Names that should exist for "{}" are missing: "{}"'
                    .format(
                        name,
                        ', '.join(sorted(missing, key=combined_key))))
        elif self._multiselect_mode == self._mode_selected_exists:
            res = [name for name in self.value_names if name in names]
        elif self._multiselect_mode == self._mode_unselected:
            res = [name for name in names if name not in self.value_names]
        elif self._multiselect_mode == self._mode_passthrough:
            res = names
        else:
            assert False, 'selected_names got unknown mode.'

        order = dict(zip(names, range(len(names))))
        return sorted(res, key=lambda x: order[x])

    @property
    def _old_list_storage(self):
        return self._parameter_dict.get('_old_list_storage', False)

    @property
    def _passthrough(self):
        return self._multiselect_mode == self._mode_passthrough

    @_passthrough.setter
    def _passthrough(self, passthrough_):
        if passthrough_:
            self._multiselect_mode = self._mode_passthrough

    # Only for access by views.
    @property
    def _multiselect_mode(self):
        return self._parameter_dict.get('mode')

    # Only for access by views.
    @_multiselect_mode.setter
    def _multiselect_mode(self, value):
        self._parameter_dict['mode'] = value
        self.value_changed.emit()

    @property
    def editor(self):
        return self._parameter_dict.get('editor')

    @editor.setter
    def editor(self, item):
        if isinstance(item, Editor):
            item = item.value()
        self._parameter_dict['editor'] = item

    def accept(self, visitor):
        return visitor.visit_list(self)

    def adjust(self, names):
        self.list = names

    def equal_to(self, other, as_stored=False):
        equal = (
            super().equal_to(other, as_stored=as_stored) and
            self.value_names == other.value_names and
            self._multiselect_mode == other._multiselect_mode)
        if self._old_list_storage or other._old_list_storage:
            equal &= self.list == other.list
        return equal

    def _set_from_parameters(self, *args, plist=None, value=None, **kwargs):
        self.list = plist
        self.value = value

    @property
    def selected(self):
        """Return the first selected item in the value list,
        does not support multi-select."""
        try:
            return self.value_names[0]
        except IndexError:
            return None

    @selected.setter
    def selected(self, item):
        if item is None:
            self.value_names = []
        else:
            self.value_names = [item]

    @property
    def value(self):
        return [self.list.index(v) for v in self.value_names if v in self.list]

    @value.setter
    def value(self, value):
        assert isinstance(value, list), 'Guard against accidental iterators.'

        value_names = [self.list[i] for i in value]
        self.value_names = value_names

    @property
    def value_names(self):
        try:
            return self._parameter_dict['value_names'][:]
        except KeyError:
            # This can happen during initiation of the parameter.
            return []

    @value_names.setter
    def value_names(self, value_names):
        self._parameter_dict['value_names'] = value_names[:]
        self._parameter_dict['value'] = [
            self.list.index(v) for v in value_names
            if v in self._parameter_dict['list']]
        self.value_changed.emit()

    @property
    def list(self):
        return self._parameter_dict['list'][:]

    @list.setter
    def list(self, plist):
        if not isinstance(plist, list):
            plist = list(plist)

        self._parameter_dict['list'] = plist[:]
        # Update self.value:
        self.value_names = self.value_names


def update_list_dict(parameter_dict):
    res = {}
    ParameterList(res, '<name>', from_definition=False, **parameter_dict)
    parameter_dict.update(res)


class ParameterGroup(ParameterEntity):
    def __init__(self, parameter_dict, name, ptype="group", **kwargs):
        super(ParameterGroup, self).__init__(
            parameter_dict, name, ptype, **kwargs)
        self._subgroups = OrderedDict()
        self._parameter_dict = parameter_dict

    def trigger_value_changed(self):
        self.value_changed.emit()

    def add_handler_to_subgroup(self, subgroup):
        if (hasattr(subgroup, 'value_changed') and
                isinstance(subgroup.value_changed, Event)):
            subgroup.value_changed.add_handler(self.trigger_value_changed)

    def _create_group(self, value_class, name=None, **kwargs):
        if name in self._parameter_dict:
            # If the parameter_dict contains the key
            # it will be used instead of creating a new.
            self._subgroups[name] = value_class(
                self._parameter_dict[name], name,
                gui_visitor=self._gui_visitor)
        elif name in self._subgroups:
            deprecated_warn('Set of existing group ({})'.format(name),
                            '3.0.0')
        else:
            self._parameter_dict[name] = OrderedDict()
            self._subgroups[name] = value_class(
                self._parameter_dict[name], name,
                gui_visitor=self._gui_visitor, **kwargs)
        self.add_handler_to_subgroup(self._subgroups[name])
        return self._subgroups[name]

    def create_group(self, name, label="", order=None):
        return self._create_group(
            ParameterGroup, name=name, label=label, order=order)

    def create_page(self, name, label="", order=None):
        return self._create_group(
            ParameterPage, name=name, label=label, order=order)

    def set_integer(self, name, value=0, label="",
                    description="", order=None, **kwargs):
        self._set_value(ParameterInteger, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_float(self, name, value=0.0, label="",
                  description="", order=None, **kwargs):
        self._set_value(ParameterFloat, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_string(self, name, value="", label="",
                   description="", order=None, **kwargs):
        self._set_value(ParameterString, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_boolean(self, name, value=False, label="",
                    description="", order=None, **kwargs):
        self._set_value(ParameterBoolean, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_json(self, name, value=None, label="",
                 description="", order=None, **kwargs):
        self._set_value(ParameterJson, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_datetime(self, name, value=None, label="",
                     description="", order=None, **kwargs):
        if value is None:
            value = datetime.datetime.now()
        self._set_value(ParameterDateTime, name, value=value, label=label,
                        description=description, order=order, **kwargs)

    def set_list(self, name, plist=None, value=None, label="",
                 description="", order=None, **kwargs):
        return self._set_value(
            ParameterList, name, plist=plist, value=value,
            label=label, description=description, order=order,
            state_settings=self._state_settings, **kwargs)

    def set_custom(self, custom_handler, name, **kwargs):
        sywarn("Custom parameters are no longer supported!")

    def value_or_default(self, name, default):
        try:
            return self._subgroups[name].value
        except KeyError:
            return default

    def value_or_empty(self, name):
        return self.value_or_default(name, '')

    def keys(self):
        nextorder = self._nextorder()

        return sorted(
            self._subgroups.keys(),
            key=lambda sub: (nextorder if self._subgroups[sub].order is None
                             else self._subgroups[sub].order))

    def _nextorder(self):
        orders = [item.order
                  for item in self._subgroups.values()]
        orders = [order for order in orders if order is not None]
        if orders:
            return max(orders) + 1
        return 0

    def children(self):
        nextorder = self._nextorder()

        return sorted(
            self._subgroups.values(),
            key=lambda sub: nextorder if sub.order is None else sub.order)

    def reorder(self):
        items = self._subgroups.values()
        if items:
            nextorder = self._nextorder()
            orders = [nextorder if item.order is None else item.order
                      for item in items]

            for i, (order, item) in enumerate(sorted(
                    zip(orders, items), key=lambda x: x[0])):
                item.order = i
                if isinstance(item, ParameterGroup):
                    item.reorder()

    def gui(self, controllers=None):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self._gui_visitor.visit_group(
            self, controllers=controllers)

    def accept(self, visitor):
        return visitor.visit_group(self)

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            set(self.keys()) == set(other.keys()) and
            all(self[k].equal_to(other[k], as_stored=True)
                for k in self.keys()))

    def _set_value(self, value_class, name=None, **kwargs):
        param = self._subgroups.get(name)
        if param is None:
            pdict = {}
            self._parameter_dict[name] = pdict
            param = value_class(
                pdict, name, gui_visitor=self._gui_visitor, **kwargs)
            self._subgroups[name] = param
        else:
            param._set_from_parameters(name=name, **kwargs)
            deprecated_warn('Set of existing parameter ({})'.format(name),
                            '3.0.0')
        self.add_handler_to_subgroup(param)
        return param

    def _set_from_parameters(self, *args, value=None, **kwargs):
        self.value = value

    def _dict(self):
        return self._parameter_dict

    def __delitem__(self, name):
        del self._parameter_dict[name]
        del self._subgroups[name]

    def __getitem__(self, name):
        return self._subgroups[name]

    def __setitem__(self, name, value):
        self._parameter_dict[name] = value._parameter_dict
        self._subgroups[name] = value

    def __iter__(self):
        for name in self.keys():
            yield name

    def __contains__(self, name):
        return name in self._subgroups

    def __str__(self):
        return str(self._parameter_dict)


class ParameterPage(ParameterGroup):
    def __init__(self, parameter_dict, name, **kwargs):
        super(ParameterPage, self).__init__(
            parameter_dict, name, "page", **kwargs)

    def accept(self, visitor):
        return visitor.visit_page(self)


class ParameterRoot(ParameterGroup):
    _binding_mode_internal = 'internal'
    _binding_mode_external = 'external'

    def __init__(self, parameter_data=None, **kwargs):

        if parameter_data is None:
            parameter_dict = OrderedDict()
        elif isinstance(parameter_data, ParameterGroup):
            parameter_dict = parameter_data.parameter_dict
            if isinstance(parameter_data, ParameterRoot):
                parameter_dict = parameter_data.parameter_dict
        else:
            parameter_dict = parameter_data
        super(ParameterRoot, self).__init__(parameter_dict, "root", **kwargs)
        ParameterBuilder(self).build()

    def accept(self, visitor):
        return visitor.visit_root(self)

    def gui(self, controllers=None):
        if self._gui_visitor is None:
            raise ValueError('Gui visitor must be set before building GUI.')
        return self._gui_visitor.visit_root(
            self, controllers=controllers)

    @property
    def _binding_mode(self):
        return self._parameter_dict.get('binding_mode')

    @_binding_mode.setter
    def _binding_mode(self, value):
        if value is None:
            self._parameter_dict.pop('binding_mode', None)
        else:
            assert value in [
                self._binding_mode_internal, self._binding_mode_external]
            self._parameter_dict['binding_mode'] = value

    def equal_to(self, other, as_stored=False):
        return (
            super().equal_to(other, as_stored=as_stored) and
            self._binding_mode == other._binding_mode)


class ParameterBuilder(object):
    """ParameterBuilder"""
    def __init__(self, parameter_group):
        super(ParameterBuilder, self).__init__()
        self._parameter_group = parameter_group

    def build(self):
        for name, value in self._parameter_group._dict().items():
            if isinstance(value, dict):
                self._factory(name, value)

    def _factory(self, name, value_dict):
        ptype = value_dict['type']
        if ptype == "group":
            new_group = self._parameter_group.create_group(name)
            # Build groups recursively
            ParameterBuilder(new_group).build()
        elif ptype == "page":
            new_page = self._parameter_group.create_page(name)
            # Build groups recursively
            ParameterBuilder(new_page).build()
        elif ptype == "integer":
            self._parameter_group.set_integer(
                name, from_definition=False, **value_dict)
        elif ptype == "float":
            self._parameter_group.set_float(
                name, from_definition=False, **value_dict)
        elif ptype == "string":
            self._parameter_group.set_string(
                name, from_definition=False, **value_dict)
        elif ptype == "boolean":
            self._parameter_group.set_boolean(
                name, from_definition=False, **value_dict)
        elif ptype == "datetime":
            self._parameter_group.set_datetime(
                name, from_definition=False, **value_dict)
        elif ptype == "json":
            self._parameter_group.set_json(
                name, from_definition=False, **value_dict)
        elif ptype == "list":
            self._parameter_group.set_list(
                name, from_definition=False, **value_dict)
        elif ptype == "custom":
            sywarn("Custom parameters are no longer supported!")
        else:
            assert isinstance(ptype, str)
            # Assume that we have encountered a parameter type that was added
            # in a later Sympathy version.
            node_logger.debug(
                'Ignoring parameter: "%s" of unknown type: "%s". '
                'This might cause unintended behavior. To be safe, use the '
                'most recent Sympathy version used to configure the node.',
                name, ptype)


class Editor(object):
    def __init__(self, editor1=None, editor2=None):
        self.attr = OrderedDict()
        if editor1 is not None:
            self.attr.update(editor1.attr)
        if editor2 is not None:
            self.attr.update(editor2.attr)

    def set_type(self, etype):
        self.attr['type'] = etype

    def set_attribute(self, attribute, value):
        self.attr[attribute] = value

    def __setitem__(self, key, value):
        self.attr[key] = value

    def __getitem__(self, key):
        return self.attr[key]

    def value(self):
        return self.attr


class Editors(object):
    @staticmethod
    def _bounded_editor(min_, max_):
        editor = Editor()
        editor.set_attribute('min', min_)
        editor.set_attribute('max', max_)
        return editor

    @staticmethod
    def _decimal_editor(decimals):
        editor = Editor()
        editor.set_attribute('decimals', decimals)
        return editor

    @staticmethod
    def lineedit_editor(placeholder=None):
        editor = Editor()
        editor.set_type('lineedit')
        if placeholder is not None:
            editor.set_attribute('placeholder', placeholder)
        return editor

    @staticmethod
    def textedit_editor():
        editor = Editor()
        editor.set_type('textedit')
        return editor

    @staticmethod
    def table_editor(headers, types, unique=None):
        """
        Table editor with fixed headers.

        Parameters
        ----------
        headers : list of str
        types : list of str
        """
        assert headers and types, 'headers and types are required'

        headers = list(headers)
        types = list(types)

        assert len(headers) == len(types), (
            'headers and types must have the same length')

        assert len(headers) == len(set(headers)), (
            'header names cannot repeat')

        if unique:
            unique = list(unique)
            assert headers and all(u in headers for u in unique), (
                'unique columns must be among headers')

        editor = Editor()
        editor.set_type('table')
        editor.set_attribute('headers', headers)
        editor.set_attribute('types', types)
        editor.set_attribute('unique', unique)
        return editor

    @staticmethod
    def code_editor(language='python'):
        editor = Editor()
        editor.set_type('code')
        editor.set_attribute('language', language)
        return editor

    @staticmethod
    def bounded_lineedit_editor(min_, max_, placeholder=None):
        return Editor(Editors.lineedit_editor(placeholder),
                      Editors._bounded_editor(min_, max_))

    @staticmethod
    def spinbox_editor(step):
        editor = Editor()
        editor.set_type('spinbox')
        editor.set_attribute('step', step)
        return editor

    @staticmethod
    def bounded_spinbox_editor(min_, max_, step):
        editor = Editor(Editors.spinbox_editor(step),
                        Editors._bounded_editor(min_, max_))
        return editor

    @staticmethod
    def decimal_spinbox_editor(step, decimals):
        editor = Editor(
            Editors.spinbox_editor(step),
            Editors._decimal_editor(decimals))
        return editor

    @staticmethod
    def bounded_decimal_spinbox_editor(min_, max_, step, decimals):
        editor = Editor(
            Editors.bounded_spinbox_editor(min_, max_, step),
            Editors._decimal_editor(decimals))
        return editor

    @staticmethod
    def filename_editor(filter_pattern=None, states=None):
        editor = Editor()
        editor.set_type('filename')
        editor.set_attribute('filter', filter_pattern or ['Any files (*)'])
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def savename_editor(filter_pattern=None, states=None):
        editor = Editor()
        editor.set_type('savename')
        editor.set_attribute('filter', filter_pattern or ['Any files (*)'])
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def directory_editor(states=None):
        editor = Editor()
        editor.set_type('dirname')
        editor.set_attribute('states', states)
        return editor

    @staticmethod
    def list_editor(**kwargs):
        editor = Editor()
        editor.set_type('listview')
        editor.set_attribute('edit', False)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def selectionlist_editor(selection, **kwargs):
        editor = Editors.list_editor()
        editor.set_attribute('selection', selection)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def multilist_editor(**kwargs):
        editor = Editors.list_editor()
        editor.set_attribute('selection', 'multi')
        editor.set_attribute('filter', True)
        editor.set_attribute('mode', True)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def combo_editor(options=None, include_empty=False, **kwargs):
        if options is None:
            options = []
        if isinstance(options, dict):
            display = list(options.values())
            options = list(options.keys())
        else:
            display = None
        editor = Editor()
        editor.set_type('combobox')
        editor.set_attribute('options', options)
        editor.set_attribute('display', display)
        editor.set_attribute('include_empty', include_empty)
        editor.set_attribute('edit', False)
        editor.set_attribute('filter', False)
        editor.attr.update(kwargs)
        return editor

    @staticmethod
    def datetime_editor(date_format=None, **kwargs):
        editor = Editor()
        editor.set_type('datetime')
        editor.set_attribute('date_format', date_format)
        editor.attr.update(kwargs)
        return editor
