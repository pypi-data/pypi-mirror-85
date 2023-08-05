# This file is part of Sympathy for Data.
# Copyright (c) 2017 Combine Control Systems AB
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
import re
import copy
import sys
import os
import logging
from collections import OrderedDict

from sympathy.utils import error

core_logger = logging.getLogger('core')

# The base handle this part $(*). Used by config file parser as well.
ENV_REGEX_BASE = r'\$\({}\)'

# The template adds extra paranthesis to group the full expression.
ENV_REGEX_TEMPLATE = r'({})'.format(ENV_REGEX_BASE)

# The regex string base handles $(FILENAME) or $(FILENAME=example.h5).
# Special handling [^\(^\)] to avoid parentheses.
ENV_REGEX_STRING = ENV_REGEX_TEMPLATE.format(r'(((\w+)=([^\(^\)]+))|(\w+))')

ENV_REGEX = re.compile(ENV_REGEX_STRING)
_environment_instance = None


def error_message(msg):
    error.error_message(msg, 'ENVIRONMENT VARIABLE')


def warning_message(msg):
    error.warning_message(msg, 'ENVIRONMENT VARIABLE')


def expanded_node_dict(old_node_dict, workflow_vars):
    node_dict = copy.deepcopy(old_node_dict)
    instance().expand_node_dict(
        node_dict['parameters'], workflow_vars)
    return node_dict


class Environment(object):
    def __init__(self):
        self._shell_variables = {}
        self._global_variables = {}
        self._shell_variables.update(os.environ.items())

    def expand_node_dict(self, node_dict, workflow_vars):
        variables = self.variables(workflow_vars)

        def find_env_params(k, d):
            val = d.get('value')
            if val is not None:
                try:
                    if d['type'] == 'string' and self._string_has_variables(val):
                        yield d
                except TypeError:
                    core_logger.error(
                        'Parameter: %s is of type string but its value is: %s.', k, val)

            for k in d:
                if isinstance(d[k], dict):
                    for i in find_env_params(k, d[k]):
                        yield i

        for node_param in find_env_params('/', node_dict):
            env_var_tuples = self._find_vars(node_param['value'])
            for env_var_tuple in env_var_tuples:
                node_param['value'] = self._expand_string(
                    env_var_tuple, node_param['value'], variables)

    def _get_prioritized_env_value(self, env_var_name, variables):
        for env_dict in variables.values():
            env_value = env_dict.get(env_var_name)
            if env_value is not None:
                return env_value
        return None

    def _find_vars(self, string):
        return ENV_REGEX.findall(string)

    def _string_has_variables(self, string):
        return ENV_REGEX.search(string) is not None

    def expand_string(self, string):
        variables = self.variables()
        env_vars = self._find_vars(string)
        for env_var in env_vars:
            string = self._expand_string(env_var, string, variables)
        return string

    def _expand_string(self, env_var_tuple, string, variables):
        # ['$(FILENAME)', 'FILENAME', '', '', '', 'FILENAME'] or
        # ['$(FILENAME=example.h5)', 'FILENAME=example.h5',
        #  'FILENAME=example.h5', 'FILENAME', 'example.h5', '']
        # en_w_or_wo_d_full -> environment variable with or without default
        # en_w_d_full -> environment variable with default full
        (en_full, en_w_or_wo_d_full, en_w_d_full, en_w_d_name,
            en_d, en_wo_d_name) = env_var_tuple
        env_var_name = en_w_d_name if en_w_d_name else en_wo_d_name
        if sys.platform == 'win32':
            env_value = self.shell_variable(env_var_name.upper(), None)
            if env_value is None:
                env_value = self._get_prioritized_env_value(
                    env_var_name, variables)
        else:
            env_value = self._get_prioritized_env_value(
                env_var_name, variables)

        if env_value is not None:
            # Replace $(FILENAME=example.h5) or $(FILENAME)
            string = string.replace(
                en_full, env_value)

        elif en_d:
            # Use default value $(FILENAME=example.h5) when no
            # FILENAME exist in the environment.
            string = string.replace(
                en_full, en_d)
        else:
            warning_message(
                'Cannot find variable {} in the environment.'.format(
                    env_var_name))
        return string

    def variables(self, workflow_variables=None):
        workflow_variables = workflow_variables or {}

        self._variables = OrderedDict(
            [('shell', self._shell_variables), ('workflow', workflow_variables),
             ('global', self._global_variables)])
        return self._variables

    def prioritized_variables(self, exclude=None):
        prio_dict = {}
        for name, scope_value in reversed(self.variables().items()):
            if exclude is None or name not in exclude:
                prio_dict.update(scope_value)
        return prio_dict

    def variable(self, name, scope):
        return self.variables()[scope].get(name)

    def shell_variable(self, name, scope):
        return self.variable(name, 'shell')

    def shell_variables(self):
        return self.variables()['shell']

    def global_variable(self, name, scope):
        return self.variable(name, 'global')

    def global_variables(self):
        return self.variables()['global']

    def set_variable(self, name, value, scope):
        self.variables()[scope][name] = value

    def set_shell_variable(self, name, value):
        # If shell variable already exist, don't add because it's from
        # env and has precedence.
        if name not in os.environ:
            self.set_variable(name, value, 'shell')

    def set_global_variable(self, name, value):
        self.set_variable(name, value, 'global')

    def set_shell_variables(self, variable_dict):
        self.variables()['shell'] = variable_dict

    def set_global_variables(self, variable_dict):
        self.variables()['global'] = variable_dict


def instance():
    global _environment_instance
    if _environment_instance is None:
        _environment_instance = Environment()
    return _environment_instance
