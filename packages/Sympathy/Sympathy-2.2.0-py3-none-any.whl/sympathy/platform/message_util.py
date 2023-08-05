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
import base64
import json
from Qt import QtCore
from . import message


class QtMessageReader(QtCore.QObject):
    """
    Reads from qtcp socket.
    """
    received = QtCore.Signal(list)

    def __init__(self, qiodev, parent=None):
        super(QtMessageReader, self).__init__(parent=parent)
        self._buf = [b'']
        self._qiodev = qiodev
        qiodev.readyRead.connect(self._read)

    def _read(self):
        msgs = self.read()
        if msgs:
            self.received.emit(msgs)

    def read(self):
        data = self._qiodev.readAll().data()
        lines = datalines(data, self._buf)
        elems = [decode_json(line) for line in lines]
        msgs = [message.from_dict(elem[2]) for elem in elems]
        return msgs

    def wait(self, time):
        self._qiodev.waitForReadyRead(time)

    def set_block(self, state):
        self._block = self._qiodev.blockSignals(state)


class QtSocketMessageReader(QtCore.QObject):
    """
    Reads from normal python socket.
    """
    received = QtCore.Signal(list)

    def __init__(self, socket, parent=None):
        super(QtSocketMessageReader, self).__init__(parent=parent)
        self._notifier = QtCore.QSocketNotifier(
            socket.fileno(), QtCore.QSocketNotifier.Read, parent=self)
        self._buf = [b'']
        self._socket = socket
        self._notifier.activated.connect(self._read)

    def _read(self, fd):
        msgs = self.read()
        if msgs:
            self.received.emit(msgs)

    def read(self):
        lines = []

        try:
            data = self._socket.recv(4096)
            while data:
                lines.extend(datalines(data, self._buf))
                data = self._socket.recv(4096)
        except Exception:
            pass
        elems = [decode_json(line) for line in lines]
        msgs = [message.from_dict(elem[2]) for elem in elems]
        return msgs


def datalines(data, bufl):
    i = data.rfind(b'\n')
    if i >= 0:
        bufl.append(data[:i])
        sdata = b''.join(bufl)
        bufl[:] = [data[i + 1:]]
        lines = sdata.split(b'\n')
        return [line.strip() for line in lines]
    else:
        bufl.append(data)
    return []


def get_msgs(lines):
    return [decode_json(line) for line in lines]


def decode_json(str_):
    return json.loads(base64.b64decode(str_).decode('ascii'))


def encode_json(dict_):
    return base64.b64encode(json.dumps(dict_).encode('ascii'))
