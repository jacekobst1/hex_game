import sys

from PySide2.QtCore import Qt, QPointF, QRect
from PySide2.QtGui import QBrush, QColor, QPen, QTransform, QMouseEvent
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QMenuBar, QMessageBox

from graph import Graph
from hexagon import QHexagonShape


class Player:
    def __init__(self, color: QColor, direction_type: str, name: str):
        self.name = name
        self.__color: QColor = color
        self.__direction_type: str = direction_type
        self.tile_graph = Graph({})

    @property
    def color(self) -> QColor:
        return self.__color

    @property
    def direction_type(self) -> str:
        return self.__direction_type


class Tile:
    def __init__(self, row, col, position, owner):
        self.row = row
        self.col = col
        self.position = position
        self.owner = owner

    def __str__(self):
        return f"|{self.row}, {self.col} - {self.owner.name or 'None'}|"


class MyWin(QGraphicsView):
    def __init__(self):
        super(MyWin, self).__init__()
        self.__window_size = 1000
        self.__game_board_size = 11
        self.__init_color = QColor(255, 255, 255, 255)  # white
        self.__player_1 = Player(QColor(51, 153, 255, 255), 'row', 'Jim')  # blue
        self.__player_2 = Player(QColor(255, 255, 51, 255), 'col', 'Bones')  # yellow
        self.__current_player: Player = None
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

        self.setGeometry(0, 0, self.__window_size, self.__window_size)
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
            self.__tiles = []
            self.__init_paint_tools()
            self.__init_game_board()
            self.__current_player = self.__player_1
            self.__current_player.tile_graph = Graph({})

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
                self.__tiles.append(Tile(row_i, col_i, position, None))
                self.__scene.addPolygon(hexagon_shape, self.__pen, self.__brush).setPos(position)

    def mousePressEvent(self, event: QMouseEvent):
        click_position = self.mapToScene(event.pos())
        selected_tile = self.__scene.itemAt(click_position, QTransform())
        self.__brush.setColor(self.__current_player.color)

        if selected_tile is not None:
            tile_from_list = list([tile for tile in self.__tiles if tile.position == selected_tile.pos()])[0]

            if tile_from_list.owner is None:
                tile_from_list.owner = self.__current_player
                self.__paint_graphic_item(selected_tile, brush=self.__brush)
                self.__handle_graph(tile_from_list)
                self.__check_path()
                self.__change_player()

    def __handle_graph(self, tile):
        self.__current_player.tile_graph.add_vertex(tile)
        friendly_neighbours = []

        for possible_position in self.__possible_neighbours_positions:
            [friendly_neighbours.append(t) for t in self.__tiles
             if t.col == tile.col + possible_position['col_offset'] and
             t.row == tile.row + possible_position['row_offset'] and
             t.owner == self.__current_player]

        for fn in friendly_neighbours:
            self.__current_player.tile_graph.add_edge({fn, tile})

    def __check_path(self):
        player_tiles = list([item for item in self.__tiles if item.owner == self.__current_player])

        if self.__current_player.direction_type == 'col':
            first_dir_tiles = list([item for item in player_tiles if item.col == 0])
            last_dir_tiles = list([item for item in player_tiles if item.col == self.__game_board_size - 1])
        else:
            first_dir_tiles = list([item for item in player_tiles if item.row == 0])
            last_dir_tiles = list([item for item in player_tiles if item.row == self.__game_board_size - 1])

        if len(first_dir_tiles) == 0 or len(last_dir_tiles) == 0:
            return None
        else:
            for ft in first_dir_tiles:
                for lt in last_dir_tiles:
                    if self.__current_player.tile_graph.find_path(ft, lt) is not None:
                        self.__restart_game(f'{self.__current_player.name} wins! Do you want to play again?')
                        break

    def __change_player(self):
        if self.__current_player == self.__player_1:
            self.__current_player = self.__player_2
        else:
            self.__current_player = self.__player_1

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
