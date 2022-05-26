
import math
from PySide6 import QtGui, QtCore, QtWidgets

from nodegraph.constants import (
    VIEWER_COLOR_BACKGROUND,
    VIEWER_COLOR_GRID,
    VIEWER_GRID_SIZE,
    VIEWER_GRID_WIDTH,
    VIEWER_GRID_SQUARES,
    VIEWER_GRID_MODE_DOTS,
    VIEWER_GRID_MODE_LINES
)


class NodeScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        # settings
        self._grid_size = VIEWER_GRID_SIZE
        self._grid_width = VIEWER_GRID_WIDTH
        self._grid_squares = VIEWER_GRID_SQUARES
        self._grid_mode = VIEWER_GRID_MODE_LINES

        self._bg_color = VIEWER_COLOR_BACKGROUND
        self._grid_color = VIEWER_COLOR_GRID

        # dark pen
        self._pen_dark =  QtGui.QPen(self._grid_color)
        self._pen_dark.setWidthF(self._grid_width)
        # light pen
        self._pen_light = QtGui.QPen(self._grid_color.lighter(f=75))
        self._pen_light.setWidthF(self._grid_width)
        # dot pen
        self._pen_dot =  QtGui.QPen(self._grid_color.lighter(f=180))
        self._pen_dot.setWidthF(self._grid_width)

        self.setBackgroundBrush(self._bg_color)

    def __repr__(self):
        cls_name = str(self.__class__.__name__)
        return '<{}("{}") object at {}>'.format(
            cls_name, self.viewer(), hex(id(self)))

    def __draw_grid(self, painter, rect):
        """
        draws the grid lines in the scene.

        Args:
            painter (QtGui.QPainter): painter object.
            rect (QtCore.QRectF): rect object.
        """

        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        first_left = left - (left % self._grid_size)
        first_top = top - (top % self._grid_size)

        # compute lines to be drawn
        lines_dark, lines_light = [], []
        # horizontal lines
        for x in range(first_left, right, self._grid_size):
            if (x % (self._grid_size * self._grid_squares) != 0):
                lines_light.append(QtCore.QLineF(x, top, x, bottom))
            else:
                lines_dark.append(QtCore.QLineF(x, top, x, bottom))
        # vertical lines
        for y in range(first_top, bottom, self._grid_size):
            if (y % (self._grid_size * self._grid_squares) != 0):
                lines_light.append(QtCore.QLineF(left, y, right, y))
            else:
                lines_dark.append(QtCore.QLineF(left, y, right, y))
        
        # draw the light lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        # draw the dark lines
        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

    def __draw_dots(self, painter, rect):
        """
        draws the grid dots in the scene.

        Args:
            painter (QtGui.QPainter): painter object.
            rect (QtCore.QRectF): rect object.
        """

        grid_size = self._grid_size

        zoom = self.viewer().get_zoom()
        if zoom < 0:
            grid_size = int(abs(zoom) / 0.3 + 1) * grid_size

        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        painter.setPen(self._pen_dot)

        [painter.drawPoint(int(x), int(y))
         for x in range(first_left, right, grid_size)
         for y in range(first_top, bottom, grid_size)]

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setBrush(self.backgroundBrush())

        if self._grid_mode is VIEWER_GRID_MODE_DOTS:
            self.__draw_dots(painter, rect)

        elif self._grid_mode is VIEWER_GRID_MODE_LINES:
            self.__draw_grid(painter, rect)

        painter.restore()

    def mousePressEvent(self, event):
        selected_nodes = self.viewer().selected_nodes()
        if self.viewer():
            self.viewer().sceneMousePressEvent(event)
        super(NodeScene, self).mousePressEvent(event)
        keep_selection = any([
            event.button() == QtCore.Qt.MiddleButton,
            event.button() == QtCore.Qt.RightButton,
            event.modifiers() == QtCore.Qt.AltModifier
        ])
        if keep_selection:
            for node in selected_nodes:
                node.setSelected(True)

    def mouseMoveEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseMoveEvent(event)
        super(NodeScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseReleaseEvent(event)
        super(NodeScene, self).mouseReleaseEvent(event)

    def viewer(self):
        return self.views()[0] if self.views() else None

    @property
    def grid_mode(self):
        return self._grid_mode

    @grid_mode.setter
    def grid_mode(self, mode=VIEWER_GRID_MODE_LINES):
        self._grid_mode = mode

    @property
    def grid_color(self):
        return self._grid_color

    @grid_color.setter
    def grid_color(self, color=(0, 0, 0)):
        self._grid_color = color
        # self.__set_pens()

    @property
    def background_color(self):
        return self._bg_color

    @background_color.setter
    def background_color(self, color=(0, 0, 0)):
        self._bg_color = color
        self.setBackgroundBrush(QtGui.QColor(*self._bg_color))
