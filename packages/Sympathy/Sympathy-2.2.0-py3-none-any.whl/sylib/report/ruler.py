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
from sympathy.api import qt2 as qt
QtGui = qt.QtGui
QtWidgets = qt.QtWidgets
QtCore = qt.QtCore


class Ruler(QtWidgets.QWidget):
    # Inspired by the (quite buggy) example from
    # https://kernelcoder.wordpress.com/2010/08/25/how-to-insert-ruler-scale-type-widget-into-a-qabstractscrollarea-type-widget/  # noqa

    HORIZONTAL = 0
    VERTICAL = 1
    WIDTH = 25

    _SCALE_COLOR = QtGui.QColor(175, 175, 175)
    _BACKGROUND_COLOR = QtGui.QColor(200, 200, 200)
    _POINTER_COLOR = QtGui.QColor(100, 100, 100)
    _TEXT_COLOR = QtGui.QColor(125, 125, 125)
    _BOUNDS_COLOR = QtGui.QColor(50, 50, 50)
    _PAPER_LINE_COLOR = QtGui.QColor(0, 0, 0)
    _A4_X = 540
    _A4_Y = 779
    _1_CM_IN_PIXELS = 27
    _1_MM_IN_PIXELS = 3


    def __init__(self, ruler_type, parent=None):
        super(Ruler, self).__init__(parent)
        self._type = ruler_type
        self._cursor_pos = QtCore.QPoint(0, 0)
        self.setMouseTracking(True)
        self.setFont(QtGui.QFont("Arial", 7))

    def minimumSizeHint(self):
        return QtCore.QSize(self.WIDTH, self.WIDTH)

    def set_cursor_pos(self, cursor_pos):
        self._cursor_pos = cursor_pos
        self.update()

    def mouseMoveEvent(self, event):
        self._cursor_pos = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._draw_rectangle(painter)
        self._draw_scale(painter, self._1_MM_IN_PIXELS, 0.4, False)
        self._draw_scale(painter, self._1_CM_IN_PIXELS, 0.8, True)
        self._draw_mouse_line(painter)
        self._draw_paper_scale(painter)

    def _draw_rectangle(self, painter):
        painter.fillRect(self.rect(), self._BACKGROUND_COLOR)
        painter.setPen(QtGui.QPen(self._TEXT_COLOR, 2))
        painter.drawRect(
            self.rect().left() + 1, self.rect().top() + 1,
            self.rect().width() - 2, self.rect().height() - 2)

    def _draw_scale(self, painter, step, length, numbered):
        is_horizontal = self.HORIZONTAL == self._type
        start = self.rect().left() if is_horizontal else self.rect().top()
        end = self.rect().right() if is_horizontal else self.rect().bottom()
        is_horizontal = self.HORIZONTAL == self._type
        for i, current in enumerate(range(start, end, step)):
            x1 = current if is_horizontal else self.rect().right()
            x2 = current if is_horizontal else self.rect().left()
            y1 = self.rect().top() if is_horizontal else current
            y2 = self.rect().bottom() if is_horizontal else current
            if is_horizontal:
                offset = (y2 - y1) * (1 - length)
                y1 += offset
            else:
                offset = (x2 - x1) * (1 - length)
                x1 += offset
            painter.setPen(self._SCALE_COLOR)
            painter.drawLine(QtCore.QLine(x1, y1, x2, y2))
            if numbered:
                txt_path = QtGui.QPainterPath()
                x = x1 + 1 if is_horizontal else x2 + 2
                y = y2 - 2 if is_horizontal else y1 + 8
                txt_path.addText(x, y, self.font(), str(i))
                painter.setPen(self._TEXT_COLOR)
                painter.drawPath(txt_path)

    def _draw_paper_scale(self, painter):
        pen = QtGui.QPen(self._PAPER_LINE_COLOR)
        pen.setWidth(2)
        painter.setPen(pen)
        font = self.font()
        font.setPointSize(10)
        painter.setFont(font)

        if self._type == self.HORIZONTAL:
            x = self._A4_X + self._1_CM_IN_PIXELS
            start_point = QtCore.QPoint(x, self.rect().top())
            end_point = QtCore.QPoint(x, self.rect().bottom())
            text_pos = QtCore.QPoint(x + 2, 12)
            rotation = 0
        if self._type == self.VERTICAL:
            y = self._A4_Y + self._1_CM_IN_PIXELS
            start_point = QtCore.QPoint(self.rect().left(), y)
            end_point = QtCore.QPoint(self.rect().right(), y)
            text_pos = QtCore.QPoint(y + 2, -13)
            rotation = 90

        painter.drawLine(start_point, end_point)
        painter.rotate(rotation)
        painter.drawText(text_pos, 'A4')

    def _draw_mouse_line(self, painter):
        painter.setPen(self._POINTER_COLOR)
        x, y = self._cursor_pos.x(), self._cursor_pos.y()
        if self._type == self.HORIZONTAL:
            start_point = QtCore.QPoint(x, self.rect().top())
            end_point = QtCore.QPoint(x, self.rect().bottom())
        else:
            start_point = QtCore.QPoint(self.rect().left(), y)
            end_point = QtCore.QPoint(self.rect().right(), y)
        painter.drawLine(start_point, end_point)
