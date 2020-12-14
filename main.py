import sys

from operator import itemgetter
from PySide2.QtGui import QBrush, QColor, QPen, QTransform, QMouseEvent
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QMenuBar, QMessageBox
from hexagon import QHexagonShape
from PySide2.QtCore import Qt, QPointF, QRect


class Player:
    def __init__(self, color: QColor, direction_type: str):
        self.__color: QColor = color
        self.__direction_type: str = direction_type

    @property
    def color(self) -> QColor:
        return self.__color

    @property
    def direction_type(self) -> str:
        return self.__direction_type


class MyWin(QGraphicsView):
    def __init__(self):
        super(MyWin, self).__init__()
        self.__window_size = 1000
        self.__game_board_size = 11
        self.__init_color = QColor(255, 255, 255, 255)  # white
        self.__player_1 = Player(QColor(51, 153, 255, 255), 'row')  # blue
        self.__player_2 = Player(QColor(255, 255, 51, 255), 'col')  # yellow
        self.__current_player = None
        self.__tiles = []
        self.__possible_neighbours_positions = [
            {'row_offset': -1, 'col_offset': 0},
            {'row_offset': -1, 'col_offset': 1},
            {'row_offset': 0, 'col_offset': -1},
            {'row_offset': 0, 'col_offset': 1},
            {'row_offset': 1, 'col_offset': -1},
            {'row_offset': 1, 'col_offset': 0}
        ]
        self.__scene = QGraphicsScene()

        self.setGeometry(self.__window_size, self.__window_size, self.__window_size, self.__window_size)
        self.setWindowTitle('Hex game')
        self.setScene(self.__scene)

        self.__init_menu()

    def __init_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, self.__window_size, 25))

        new_game_action = menu_bar.addAction('New game')
        new_game_action.triggered.connect(lambda: self.__restart_game('Are you sure you want to start the new game?'))

    def __restart_game(self, text: str):
        if self.__current_player is None or self.__restart_game_prompt(text):
            self.__init_paint_tools()
            self.__init_game_board()
            self.__current_player = self.__player_1

    def __restart_game_prompt(self, text: str) -> bool:
        prompt_window = QMessageBox
        choice = prompt_window.question(self,
                                        'New game',
                                        text,
                                        prompt_window.Yes | prompt_window.No)
        return choice == prompt_window.Yes

    def __init_paint_tools(self):
        self.__brush = QBrush(self.__init_color)
        self.__pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

    def __init_game_board(self):
        hexagon_shape = QHexagonShape(0, 0, 30, 90)
        x_offset = 50
        y_offset = 45
        next_row_x_offset = 25

        for row_i in range(self.__game_board_size):
            current_row_x_offset = row_i * next_row_x_offset
            y = row_i * y_offset
            for col_i in range(self.__game_board_size):
                x = col_i * x_offset + current_row_x_offset
                position = QPointF(x, y)
                self.__tiles.append({
                    'row': row_i,
                    'col': col_i,
                    'position': position,
                    'owner': None
                })
                self.__scene.addPolygon(hexagon_shape, self.__pen, self.__brush).setPos(position)

    def mousePressEvent(self, event: QMouseEvent):
        click_position = self.mapToScene(event.pos())
        selected_tile = self.__scene.itemAt(click_position, QTransform())
        self.__brush.setColor(self.__current_player.color)

        if selected_tile is not None:
            tile_from_list = list([tile for tile in self.__tiles if tile['position'] == selected_tile.pos()])[0]

            if tile_from_list['owner'] is None:
                tile_from_list['owner'] = self.__current_player
                self.__paint_graphic_item(selected_tile, brush=self.__brush)
                self.__compute_result(self.__current_player)
                self.__change_player()

    def __change_player(self):
        if self.__current_player == self.__player_1:
            self.__current_player = self.__player_2
        else:
            self.__current_player = self.__player_1

    def __compute_result(self, player: Player):
        player_tiles = list([item for item in self.__tiles if item['owner'] == player])
        first_dir_tiles = list([item for item in player_tiles if item[player.direction_type] == 0])

        for first_dir_tile in first_dir_tiles:
            possible_tiles = [item for item in player_tiles if item != first_dir_tile]
            route = [first_dir_tile]
            self.__check_neighbours(route, first_dir_tile, possible_tiles)

    def __check_neighbours(self,
                           route: list,
                           tile: dict,
                           possible_tiles: list):
        route.append(tile)
        possible_tiles = [item for item in possible_tiles if item != tile]

        for possible_neighbour_position in self.__possible_neighbours_positions:
            for neighbour_tile in [item for item in possible_tiles
                                        if item['row'] == tile['row'] + possible_neighbour_position['row_offset']
                                        and item['col'] == tile['col'] + possible_neighbour_position['col_offset']]:
                if list([item for item in route if item['row'] == self.__game_board_size - 1]):
                    self.__restart_game('You win! Do you want to play again?')
                self.__check_neighbours(route, neighbour_tile, possible_tiles)

    @staticmethod
    def __paint_graphic_item(graphic_item: QGraphicsPolygonItem,
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
