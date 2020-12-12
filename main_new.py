import sys

from PySide2.QtGui import QBrush, QColor, QPen, QTransform
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from hexagon import QHexagonShape
from PySide2.QtCore import Qt


class MyWin(QGraphicsView):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setStyleSheet(open('style.css').read())

        self.setGeometry(1000, 1000, 1000, 1000)
        self.setWindowTitle('Hex game')

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.selected_tile = None

        self.init_tiles()
        self.init_tools()
        self.init_gameboard()

    def init_tiles(self):
        self.hexagon_shape1 = QHexagonShape(0, 0, 30, 90)
        self.hexagon_shape2 = QHexagonShape(25, 45, 30, 90)

    def init_tools(self):
        self.brush = QBrush(QColor(255, 255, 255, 255))
        self.pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

    def init_gameboard(self):
        self.scene.addPolygon(self.hexagon_shape1, self.pen, self.brush)
        self.scene.addPolygon(self.hexagon_shape2, self.pen, self.brush)
        print(self.scene.items())

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())
        new_selected_tile = self.scene.itemAt(position, QTransform())
        position = self.mapToScene(event.pos())
        print(f"tile selected at position {position}")
        self.brush.setColor(QColor(0, 0, 255, 255))
        if new_selected_tile is not None:
            self.paint_graphic_item(new_selected_tile, brush=self.brush)

    def paint_graphic_item(self, graphic_item, pen=None, brush=None):
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
