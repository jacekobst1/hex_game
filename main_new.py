import sys

from PySide2.QtGui import QBrush, QColor, QPen, QTransform, QMouseEvent
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QMenuBar, QMessageBox
from hexagon import QHexagonShape
from PySide2.QtCore import Qt, QPointF, QRect


class MyWin(QGraphicsView):
    def __init__(self):
        super(MyWin, self).__init__()
        self.window_size = 1000
        self.game_board_size = 11
        self.init_color = QColor(255, 255, 255, 255)
        self.player_1 = Player(QColor(51, 153, 255, 255))
        self.player_2 = Player(QColor(255, 255, 51, 255))
        self.scene = QGraphicsScene()

        self.setGeometry(self.window_size, self.window_size, self.window_size, self.window_size)
        self.setWindowTitle('Hex game')
        self.setScene(self.scene)

        self.__init_menu()

    def __init_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, self.window_size, 25))

        new_game_action = menu_bar.addAction('New game')
        new_game_action.triggered.connect(self.__restart_game)

    def __restart_game(self):
        if not hasattr(self, 'brush') or self.__restart_game_prompt():
            self.__init_paint_tools()
            self.__init_game_board()
            self.current_player = self.player_1

    def __restart_game_prompt(self) -> bool:
        prompt_window = QMessageBox
        choice = prompt_window.question(self,
                                        'New game',
                                        'Are you sure you want to start the new game?',
                                        prompt_window.Yes | prompt_window.No)
        return choice == prompt_window.Yes

    def __init_paint_tools(self):
        self.brush = QBrush(self.init_color)
        self.pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

    def __init_game_board(self):
        hexagon_shape = QHexagonShape(0, 0, 30, 90)
        x_offset = 50
        y_offset = 45
        next_row_x_offset = 25

        for row_i in range(self.game_board_size):
            current_row_x_offset = row_i * next_row_x_offset
            y = row_i * y_offset
            for col_i in range(self.game_board_size):
                x = col_i * x_offset + current_row_x_offset
                self.scene.addPolygon(hexagon_shape, self.pen, self.brush).setPos(QPointF(x, y))

    def mousePressEvent(self, event: QMouseEvent):
        click_position = self.mapToScene(event.pos())
        selected_tile = self.scene.itemAt(click_position, QTransform())
        self.brush.setColor(self.current_player.get_color())
        if selected_tile is not None:
            self.__paint_graphic_item(selected_tile, brush=self.brush)
            self.change_player()
            print(selected_tile.pos())

    def change_player(self):
        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

    @staticmethod
    def __paint_graphic_item(graphic_item: QGraphicsPolygonItem,
                             pen: QPen = None,
                             brush: QBrush = None):
        if pen is not None:
            graphic_item.setPen(pen)

        if brush is not None:
            graphic_item.setBrush(brush)

        graphic_item.update()


class Player:
    def __init__(self, color: QColor):
        self.__color = color

    def get_color(self):
        return self.__color


if __name__ == "__main__":
    app = QApplication([])
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
