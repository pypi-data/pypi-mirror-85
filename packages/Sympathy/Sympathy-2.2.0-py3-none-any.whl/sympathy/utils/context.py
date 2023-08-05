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
import contextlib
import inspect
import functools

from ..platform.exceptions import NoDataError, sywarn
from ..platform import state
from . import tag
from builtins import DeprecationWarning


# Copied from six
def reraise(tp, value, tb=None):
    try:
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None
        tb = None


# Copied from: https://www.python.org/dev/peps/pep-0257/
def trim_doc(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    inf = float('inf')
    indent = inf
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < inf:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def indent_doc(docstring, n=4):
    return '\n'.join(['{}{}'.format(' ' * n, line) if line.strip() else ''
                      for line in docstring.splitlines()])


def inherit_doc(cls):
    """
    Classes decorated will inherit missing __doc__ on methods from the first
    parent along the mro that provides it.
    """

    def method_doc(fname, f, mro):

        for cls_ in mro:
            f_ = getattr(cls_, fname, None)

            if f_ is not None and f_.__doc__ is not None:
                f.__func__.__doc__ = f_.__doc__
                break
        return f

    for fname, f in inspect.getmembers(cls, predicate=inspect.ismethod):
        method_doc(fname, f, cls.mro())

    return cls


def join_doc(*docs, **kwargs):
    """
    Join docstrings (docs) producing a new docstring as the result
    Separator can be passed as sep in kwargs (default = '\n\n').
    """
    sep = kwargs.get('sep', '\n\n')
    return sep.join(trim_doc(doc) for doc in docs)


def deprecated(message=''):
    raise DeprecationWarning(message)


def warn_deprecated(message=''):

    settings = state.node_state().attributes.get('worker_settings', {})

    try:
        warn = settings['deprecated_warning']
    except KeyError:
        warn = True

    if warn:
        sywarn(message)


def deprecated_function(version, repl=''):
    """
    Using this decorator on a function marks it as deprecated and scheduled for
    removal in set version.

    Calling the function will result in a warning printed if the setting to
    print warnings is active.
    If repl (replacement message) is provided that message be included.
    """

    def owrapper(func):
        name = func.__name__
        module = func.__module__

        @functools.wraps(func)
        def iwrapper(*args, **kwargs):
            deprecated_warn(
                "{}.{}".format(module, name),
                version, repl)
            return func(*args, **kwargs)
        return iwrapper
    return owrapper


def deprecated_method(version, repl=''):
    """
    Using this decorator on a method marks it as deprecated and scheduled for
    removal in set version.

    Calling the  method will result in a warning printed if the setting to
    print warnings is active.
    If repl (replacement message) is provided that message be included.
    """

    def owrapper(func):
        name = func.__name__
        module = func.__module__

        @functools.wraps(func)
        def iwrapper(self, *args, **kwargs):
            cls = type(self).__name__
            deprecated_warn("{}.{}.{}".format(module, cls, name),
                            version, repl)
            return func(self, *args, **kwargs)
        return iwrapper
    return owrapper


def format_deprecated_warn(msg, version, repl='', help=False):
    """
    Calling the method will return in a warning message about the node
    in question being scheduled for removal.

    If repl (replacement message) is provided that message be included.
    """
    help_msg = ''.join([
        "\nPlease use {} instead.".format(repl) if repl else "",
        "\n\nTo disable deprecation warnings, uncheck:\nPreferences "
        "-> Advanced -> Display warnings for deprecated nodes."
        if help else ""])

    return (
        "{} is deprecated and will be removed in version {}.{}".format(
            msg,
            version,
            help_msg))


def deprecated_warn(msg, version, repl=''):
    """
    Calling the  method will result in a warning printed if the setting to
    print warnings is active.

    If repl (replacement message) is provided that message be included.
    """
    warn_deprecated(format_deprecated_warn(msg, version, repl))


def deprecated_node(version, repl=''):
    """
    Using this decorator on a node marks it as deprecated and scheduled for
    removal in set version.

    Using the node will result in a warning printed if the setting to
    print deprecation warnings is active.
    If repl (replacement message) is provided that message be included.

    Deprecated nodes are automatically hidden.
    """
    def wrapper(cls):
        cls.tags = tag.Tags(tag.TagBuilder().Hidden.Deprecated)
        cls.deprecated = (cls.name, version, repl)
        return cls
    return wrapper


def nested(*args):
    return contextlib.nested(*args)


class PortDummy(object):
    """
    PortDummy is returned instead of a real data type if there is no data on
    the port.

    To test if you got a real data type or only got a :class:`PortDummy` object
    use the :meth:`is_valid` method::

        input_table = node_context.input['input']
        if input_table.is_valid():
            # Data available
        else:
            # No data available, trying to use input_table will raise a
            # NoDataError.

    Accessing any other member of a :class:`PortDummy` object will raise a
    NoDataError which tells the user what to do.
    """
    def __init__(self, exc_info):
        self._exc_info = exc_info

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __getattr__(self, key):
        self.raise_error()

    def __getitem__(self, key):
        self.raise_error()

    def __setitem__(self, key, value):
        self.raise_error()

    def __iter__(self):
        self.raise_error()

    def __len__(self):
        self.raise_error()

    def close(self):
        pass

    def raise_error(self):
        raise NoDataError(
            'Port creation caused an error and the broken port is '
            'now accessed.')

    @staticmethod
    def is_valid():
        return False


class InputPortDummy(PortDummy):
    def raise_error(self):
        raise NoDataError(
            'Could not create input port. Try connecting the input '
            'and running all previous nodes first')


class OutputPortDummy(PortDummy):
    def raise_error(self):
        raise NoDataError(
            'Could not create output port. You may not have permission to '
            'write it. This could be caused by files being locked by viewers '
            'or configuration GUIs of subsequent nodes.')


class ErrorPortDummy(PortDummy):

    def raise_error(self):
        reraise(*self._exc_info)


def with_files(function, files):
    """
    Call the function with the files opened.
    Files are received as a list opened in the order they occur in the
    input.
    """
    return function(files)


def original(func):
    """
    Wrapper to track of if func has been overridden.
    If is_original(object.func) returns False then it has been.
    """
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    inner.__doc__ = func.__doc__
    inner.original = True
    return inner


def is_original(func):
    return getattr(func, 'original', False)
