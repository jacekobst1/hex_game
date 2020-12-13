import sys

from PySide2.QtGui import QBrush, QColor, QPen, QTransform, QMouseEvent
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem
from hexagon import QHexagonShape
from PySide2.QtCore import Qt, QPointF


class MyWin(QGraphicsView):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setGeometry(1000, 1000, 1000, 1000)
        self.setWindowTitle('Hex game')

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.init_tools()
        self.init_game_board(11)

    def init_tools(self):
        self.brush = QBrush(QColor(255, 255, 255, 255))
        self.pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

    def init_game_board(self, size: int):
        hexagon_shape = QHexagonShape(0, 0, 30, 90)
        x_offset = 50
        y_offset = 45
        next_row_x_offset = 25

        for row_i in range(size):
            current_row_x_offset = row_i * next_row_x_offset
            y = row_i * y_offset
            for col_i in range(size):
                x = col_i * x_offset + current_row_x_offset
                self.scene.addPolygon(hexagon_shape, self.pen, self.brush).setPos(QPointF(x, y))

    def mousePressEvent(self, event: QMouseEvent):
        click_position = self.mapToScene(event.pos())
        selected_tile = self.scene.itemAt(click_position, QTransform())
        self.brush.setColor(QColor(0, 0, 255, 255))
        if selected_tile is not None:
            self.paint_graphic_item(selected_tile, brush=self.brush)
            print(selected_tile.pos())

    def paint_graphic_item(self,
                           graphic_item: QGraphicsPolygonItem,
                           pen: QPen = None,
                           brush: QBrush = None):
        if pen is not None:
            graphic_item.setPen(pen)

        if brush is not None:
            graphic_item.setBrush(brush)

        graphic_item.update()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
