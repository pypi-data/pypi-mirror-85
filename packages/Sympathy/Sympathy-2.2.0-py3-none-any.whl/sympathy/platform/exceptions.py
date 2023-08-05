# This file is part of Sympathy for Data.
# Copyright (c) 2014, Combine Control Systems AB
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
"""Exceptions for use in Sympathy nodes."""
import sys
import warnings
import traceback
# import linecache


# def _show_warning(message, category, filename, lineno, file=None, line=None):
#     """Function hook to show warning with better unicode support."""
#     if file is None:
#         file = sys.stderr
#     try:
#         print(_formatwarning(message, category, filename, lineno, line),
#               file=file)
#     except IOError:
#         pass

# warnings.showwarning = _show_warning


# def _formatwarning(message, category, filename, lineno, line=None):
#     """Function to format a warning with better unicode support."""
#     s = u'{}:{}: {}: {}'.format(filename, lineno, category.__name__,
#                                 message)
#     line = linecache.getline(filename, lineno) if line is None else line
#     if line:
#         line = line.strip()
#         s += u'\n  {}'.format(line)
#     return s


def sywarn(message, stack=False, stacklevel=2):
    """Notify the user of a node error."""
    if stack:
        with warnings.catch_warnings():
            warnings.simplefilter('always')
            warnings.warn(message, stacklevel=stacklevel)
    else:
        print(message, file=sys.stderr)


class SyError(Exception):
    pass


class NoDataError(SyError):
    """Raised when trying to access data on an input port which has no data."""
    pass


class SyNodeError(SyError):
    """
    An error occurred in the node. See the specific error message for details.
    For further information, please refer to the node's documentation.
    """

    def __init__(self, msg, details=""):
        """
        First argument should be a short description of the error. details
        argument can be an arbitrarily long string describing the error
        in more detail.
        """
        super(SyNodeError, self).__init__(msg)
        self._details = details

    @property
    def help_text(self):
        """Detailed help text."""
        return self._details


class SyDataError(SyNodeError):
    """
    Used to indicate that something is wrong with the data that this node
    received.
    """
    def __init__(self, msg, details=""):
        """Same arguments as SyNodeError.__init__()."""
        super(SyDataError, self).__init__(
            msg, details or "Error in input data.")


class SyColumnTypeError(SyError):
    pass


class SyConfigurationError(SyNodeError):
    """
    Used to indicate an error in the node's configuration.
    """
    def __init__(self, msg, details=""):
        """Same arguments as SyNodeError.__init__()."""
        super(SyConfigurationError, self).__init__(
            msg, details or "Error in node configuration.")


class SyUserCodeError(SyNodeError):
    """
    Used to indicate an error in the user-supplied code for this node.
    """
    def __init__(self, exc_info, msg=None):
        """
        First argument should be a tuple with three elements such as the tuple
        returned from sys.exc_info(). Optional argument msg can be used to
        change the default short error description.
        """
        etype, value, tb = exc_info
        if msg is None:
            msg = "Error in user-supplied code: {}".format(exc_info[1])
        details = "".join(traceback.format_exception(etype, value, tb))
        self._brief = "".join(traceback.format_exception_only(etype, value))
        super(SyUserCodeError, self).__init__(msg, details)

    @property
    def brief_help_text(self):
        return self._brief


class FlowError(SyError):
    pass


class ReadSyxFileError(FlowError):
    """
    Exception used when a syx file could not be read from disk for any reason.

    The cause property should be a short sentence about why the file wasn't
    loaded aimed at the average user. The details property should be aimed at
    an advanced user who tries to find and remedy the problem.
    """
    def __init__(self, cause, details):
        super(ReadSyxFileError, self).__init__()
        self._cause = cause
        self._details = details

    @property
    def cause(self):
        return self._cause

    @property
    def details(self):
        return self._details

    def __str__(self):
        return self._cause


class LibraryError(SyError):
    pass


class NoLibraryError(LibraryError):
    def __init__(self, lib):
        super(NoLibraryError, self).__init__()
        self._lib = lib

    def __str__(self):
        return 'NoLibraryError({})'.format(self._lib)


class ConflictingFlowLibrariesError(LibraryError):
    def __init__(self, libs):
        super(ConflictingFlowLibrariesError, self).__init__()
        self._libs = libs

    def __str__(self):
        return 'ConflictingFlowLibrariesError({})'.format(self._libs)

    @property
    def help_text(self):
        return ('Workflow libraries: {} are in conflict with those of other '
                'libraries'.format(
                    ', '.join(self._libs)))


class ConflictingGlobalLibrariesError(LibraryError):
    def __init__(self, libs):
        super(ConflictingGlobalLibrariesError, self).__init__()
        self._libs = libs or []

    @property
    def libs(self):
        return self._libs

    def __str__(self):
        return 'ConflictingGlobalLibrariesError({})'.format(self._libs)

    @property
    def help_text(self):
        return ('Workflow libraries: {} are in conflict with those of global '
                'libraries'.format(
                    ', '.join(self._libs)))


class ConflictingInternalLibrariesError(LibraryError):
    def __init__(self, libs):
        super(ConflictingInternalLibrariesError, self).__init__()
        self._libs = libs

    def __str__(self):
        return 'ConflictingInternalLibrariesError({})'.format(self._libs)

    @property
    def help_text(self):
        return ('Workflow libraries: {} are in conflict with those of its '
                'internal libraries'.format(
                    ', '.join(self._libs)))


class LinkLoopError(ReadSyxFileError):
    pass


class SyListIndexError(SyError):
    def __init__(self, index, exc_info=None):
        super(SyListIndexError, self).__init__(index)
        self.exc_info = exc_info
        self.index = index


class SyChildError(SyError):
    def __init__(self):
        super(SyChildError, self).__init__()
