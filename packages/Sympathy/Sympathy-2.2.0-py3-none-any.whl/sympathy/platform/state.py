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
"""
Methods for handling global state.
"""
import warnings
import collections
import uuid
from sympathy.platform import node_result
from contextlib import contextmanager

# Ignore a warning from numpy>=1.14 when importing h5py<=2.7.1:
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import h5py


__node_state = None
__cache_state = None
__hdf5_state = None
# __cache_hdf5_state = False


def node_state():
    global __node_state
    if __node_state is None:
        __node_state = NodeState()
    return __node_state


def hdf5_state():
    global __hdf5_state
    if __hdf5_state is None:
        __hdf5_state = Hdf5State()
    return __hdf5_state


# def cache_state():
#     global __cache_state
#     if __cache_state is None:
#         __cache_state = CacheState()
#     return __cache_state


# def cache_hdf5_state():
#     global __cache_hdf5_state
#     __cache_hdf5_state = True


@contextmanager
def state():
    """
    Produce a fresh state to run in.
    The original state is restored when the contextmanager finishes.

    Example:

    >>> with state():
    >>>    pass  # Do something.

    This is required for example when running debug using editor plugin to make
    sure that the current context is not cleared when the new state is set up.
    Otherwise this would lead to files being closed in a very unexpected
    manner.
    """
    global __node_state
    # global __cache_state
    global __hdf5_state
    # global __cache_hdf5_state

    old_node_state = __node_state
    # old_cache_state = __cache_state
    old_hdf5_state = __hdf5_state
    # old_cache_hdf5_state = __cache_hdf5_state

    __node_state = None
    # __cache_state = None
    __hdf5_state = None
    # __cache_hdf5_state = False

    yield

    __node_state = old_node_state
    # __cache_state = old_cache_state
    __hdf5_state = old_hdf5_state
    # __cache_hdf5_state = old_cache_hdf5_state


class Node:
    def __init__(self, instance_id):
        """
        Parameters
        ----------
        instance_id : string
            Full node uuid or arbitrary identifier string
        """
        self._instance_id = instance_id

    @property
    def identifier(self):
        return self._instance_id


class Settings(object):
    def __init__(self, attributes):
        self._attributes = attributes

    def __getitem__(self, key):
        try:
            return self._attributes['node_settings'][key]
        except KeyError:
            try:
                return self._attributes['worker_settings'][key]
            except KeyError:
                return self._attributes[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def values(self):
        tmp = {}
        tmp.update(self._attributes)
        tmp.update(tmp.pop('worker_settings'))
        tmp.update(tmp.pop('node_settings'))


class NodeState(object):
    def __init__(self):
        self.attributes = {}
        self.hdf5 = hdf5_state()
        self.result = None
        # self.cache = cache_state()

    def create(self, **kwargs):
        self.hdf5.create()
        # self.cache.create(**kwargs)
        self.attributes.update(kwargs)
        self.result = node_result.NodeResult()

    def set_attributes(self, **kwargs):
        self.attributes.update(kwargs)

    def clear(self):
        self.hdf5.clear()
        # self.cache.clear()
        self.attributes.clear()
        self.result = None

    def cleardata(self):
        # self.cache.close()
        self.hdf5.clear()

    @property
    def settings(self):
        return Settings(self.attributes)


# class CacheState(object):
#     def __init__(self):
#         self.filestate = None
#         self.session_dir = None

#     def create(self, **kwargs):
#         self.clear()
#         self.session_dir = kwargs.get('session_dir', None)

#     def clear(self):
#         self.close()
#         self.session_dir = None
#         self.filestate = None

#     def add(self, cache):
#         self.filestate = cache

#     def close(self):
#         if self.filestate is not None:
#             try:
#                 self.filestate.cache.close()
#             except ValueError:
#                 # Do not allow exceptions here due to already closed file.
#                 pass

#     def get(self):
#         return self.filestate


class Hdf5State(object):
    # Maximum file handles:
    #     Windows 7-10: 2048 (non-configurable)

    link_lru_cache_len_max = 1600

    def __init__(self):
        # self.filestate contains the port files, opened directly and without
        # links.  These are kept opened and should be fairly limited in number.
        self.filestate = {}
        # self._link_lru_cache contains files opened through links, if a link
        # file is somehow added to filestate instead it will be removed from
        # lru.
        self._link_lru_cache = collections.OrderedDict()

    def create(self):
        self.clear()
        self.filestate = {}
        self._link_lru_cache = collections.OrderedDict()

    def clear(self):
        for filename in list(self.filestate):
            self.close(filename)

        self.clear_lru()

    def clear_lru(self):
        for filename in list(self._link_lru_cache):
            self._close_lru(filename)

    def add(self, filename, group):
        if filename not in self.filestate:
            self.filestate[filename] = group

        self._link_lru_cache.pop(filename, None)

    def open(self, filename, mode):
        if filename in self.filestate:
            hdf5_file = self.filestate[filename]
        else:
            hdf5_file = self._link_lru_cache.get(filename, None)
            if hdf5_file is None:
                hdf5_file = h5py.File(filename, mode)
                if mode == 'r':
                    if (len(self._link_lru_cache) >=
                            self.link_lru_cache_len_max):
                        prev = self._link_lru_cache.popitem(False)[1]
                        self._close_file(prev)
                    self._link_lru_cache[filename] = hdf5_file
                else:
                    assert False, (
                        'Only files for node ports should be opened in write '
                        'mode and the should not be closed.')

        return hdf5_file

    def _close_file(self, hdf5_file, filename=None):
        try:
            file_ = None
            if filename is None and hdf5_file:
                file_ = hdf5_file.file
                if file_:
                    filename = file_.filename
            if filename:
                self.filestate.pop(filename, None)
                self._link_lru_cache.pop(filename, None)
            try:
                if file_:
                    file_.flush()
                    file_.close()
            except ValueError:
                # Do not allow exceptions here due to already closed file.
                pass

        except RuntimeError:
            pass

    def close(self, filename):
        hdf5_file = self.filestate.pop(filename)
        self._close_file(hdf5_file, filename)

    def _close_lru(self, filename):
        hdf5_file = self._link_lru_cache.pop(filename)
        self._close_file(hdf5_file)

    def getlink(self, hdf5_file, entry):
        link = hdf5_file.get(entry, getlink=True)
        if isinstance(link, h5py.ExternalLink):
            link_hdf5_file = self.open(link.filename, 'r')
            return self.get(link_hdf5_file, link.path)
        else:
            dataset = hdf5_file[entry]
            return h5py.ExternalLink(dataset.file.filename,
                                     dataset.name)

    def is_closed(self, filename):
        hdf5_file = None
        if filename in self.filestate:
            hdf5_file = self.filestate[filename]
        else:
            hdf5_file = self._link_lru_cache.get(filename, None)
        if hdf5_file is None:
            res = True
        else:
            res = bool(hdf5_file)
        return res

    def file(self, filename):
        hdf5_file = None
        if filename in self.filestate:
            hdf5_file = self.filestate[filename]
        else:
            hdf5_file = self._link_lru_cache.get(filename, None)
        if hdf5_file is None:
            res = None
        else:
            res = hdf5_file.file
        return res
