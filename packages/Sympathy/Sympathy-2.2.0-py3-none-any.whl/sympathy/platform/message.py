# This file is part of Sympathy for Data.
# Copyright (c) 2016, Combine Control Systems AB
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


class Message(object):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def type(self):
        return self.__class__

    def to_dict(self):
        return {'type': self.__class__.__name__, 'data': self._data}


class DataBlockedMessage(Message):
    def __init__(self, uuid):
        super(DataBlockedMessage, self).__init__(uuid)


class DataReadyMessage(Message):
    def __init__(self, uuid):
        super(DataReadyMessage, self).__init__(uuid)


class DataRequestMessage(Message):
    def __init__(self, uuid):
        super(DataRequestMessage, self).__init__(uuid)


class StatusDataRequestMessage(Message):
    def __init__(self, uuid):
        super(StatusDataRequestMessage, self).__init__(uuid)


class AggConfigUpdateMessage(Message):
    def __init__(self, dict_data):
        super(AggConfigUpdateMessage, self).__init__(dict_data)


class RaiseWindowMessage(Message):
    def __init__(self, uuid):
        super(RaiseWindowMessage, self).__init__(uuid)


class ProgressMessage(Message):
    def __init__(self, value):
        super(ProgressMessage, self).__init__(value)


class ChildNodeProgressMessage(Message):
    def __init__(self, data):
        uuid, progress = data
        super(ChildNodeProgressMessage, self).__init__([uuid, progress])


class StatusMessage(Message):
    def __init__(self, value):
        super(StatusMessage, self).__init__(value)


class ChildNodeDoneMessage(Message):
    def __init__(self, data):
        uuid, node_result_dict = data
        super(ChildNodeDoneMessage, self).__init__([uuid, node_result_dict])


class OutStreamMessage(Message):
    def __init__(self, data):
        identifier, msg = data
        super().__init__([identifier, msg])


class StderrMessage(OutStreamMessage):
    pass


class StdoutMessage(OutStreamMessage):
    pass


class RequestHelpMessage(Message):
    def __init__(self, path):
        super().__init__(path)


class PortDataReadyMessage(Message):
    def __init__(self, value):
        super(PortDataReadyMessage, self).__init__(value)

    @classmethod
    def init_args(cls, uuid, filename, dtype):
        return cls({'uuid': uuid, 'file': filename, 'type': dtype})

    @property
    def filename(self):
        return self._data['file']

    @property
    def dtype(self):
        # Warning! do not confuse with property named type.
        return self._data['type']

    @property
    def uuid(self):
        return self._data['uuid']


def from_dict(msg_dict):
    cls = globals()[msg_dict['type']]
    return cls(msg_dict['data'])
