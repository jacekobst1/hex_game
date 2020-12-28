import sys

from PySide2.QtCore import Qt, QPointF, QRect
from PySide2.QtGui import QBrush, QColor, QPen, QTransform, QMouseEvent
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QMenuBar, QMessageBox, \
    QInputDialog

from classes.graph import Graph
from classes.hexagon import QHexagonShape
from classes.player import Player


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
        self.__future_game_board_size = None
        self.__future_players_names = {'first': None, 'second': None}
        self.__init_color = QColor(255, 255, 255, 255)  # white
        self.BLUE = QColor(51, 153, 255, 255)
        self.YELLOW = QColor(255, 255, 51, 255)
        self.BLUE_FAINT = QColor(51, 153, 255, 150)
        self.YELLOW_FAINT = QColor(255, 255, 51, 150)
        self.GREEN = QColor(24, 102, 14, 255)
        self.__player_1 = Player(self.BLUE, 'row', None)
        self.__player_2 = Player(self.YELLOW, 'col', None)
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

        self.setGeometry(2000, 50, self.__window_size, self.__window_size)
        self.setWindowTitle('Hex game')
        self.setScene(self.__scene)

        self.__init_menu()

    def __init_menu(self) -> None:
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, self.__window_size, 25))

        new_game_action = menu_bar.addAction('New game')
        new_game_action.triggered.connect(lambda: self.__restart_game('Are you sure you want to start the new game?'))

        input_dialog = menu_bar.addAction('Set players')
        input_dialog.triggered.connect(lambda: self.get_players_names())

        input_dialog = menu_bar.addAction('Set board size')
        input_dialog.triggered.connect(lambda: self.__board_size_prompt())

    def __restart_game(self, text: str) -> None:
        if self.__current_player is None or self.__restart_game_prompt(text):
            self.__tiles = []
            self.__init_paint_tools()
            self.__init_game_board()
            self.__display_current_player('')
            if self.__player_1.name is None or self.__player_2 is None:
                self.get_players_names()
            self.__change_player()
            self.__current_player.tile_graph = Graph({})
            self.set_players_names()
            self.__display_current_player(self.__current_player.name)

    def __restart_game_prompt(self, text: str) -> bool:
        prompt_window = QMessageBox
        choice = prompt_window.question(self,
                                        'New game',
                                        text,
                                        prompt_window.Yes | prompt_window.No)
        return choice == prompt_window.Yes

    def __player_name_prompt(self, label, player) -> None:
        while True:
            text, ok = QInputDialog.getText(self, "Players' names", label + ':')

            if ok:
                if str(text).strip() != '':
                    self.__future_players_names[player] = text
                    break
            if not ok:
                self.__future_players_names[player] = label
                break

    def __board_size_prompt(self) -> None:
        while True:
            board_size, ok = QInputDialog.getInt(self, 'Board size', 'Specify board size (4-19)',
                                                 minValue=4,
                                                 maxValue=19,
                                                 value=11)

            if ok:
                if 4 <= board_size <= 20:
                    self.__future_game_board_size = board_size
                    break
            if not ok:
                self.__future_game_board_size = 11
                break

    def get_players_names(self) -> None:
        self.__player_name_prompt('First player (blue)', 'first')
        self.__player_name_prompt('Second player (yellow)', 'second')

    def set_players_names(self) -> None:
        self.__player_1.name = self.__future_players_names['first']
        self.__player_2.name = self.__future_players_names['second']

    def __init_paint_tools(self) -> None:
        self.__brush = QBrush(self.__init_color)
        self.__pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

    def __init_game_board(self) -> None:
        self.__game_board_size = self.__future_game_board_size or 11
        self.__scene.clear()
        hexagon_shape = QHexagonShape(0, 0, 30, 90)
        x_offset = 50
        y_offset = 45
        next_row_x_offset = 25

        for row_i in range(self.__game_board_size + 1):
            current_row_x_offset = row_i * next_row_x_offset
            y = row_i * y_offset
            for col_i in range(self.__game_board_size + 1):
                x = col_i * x_offset + current_row_x_offset
                position = QPointF(x, y)
                if row_i == 0 or row_i == self.__game_board_size:
                    self.__scene.addPolygon(hexagon_shape, self.__pen, QBrush(self.BLUE_FAINT)).setPos(position)

                elif col_i == 0 or col_i == self.__game_board_size:
                    self.__scene.addPolygon(hexagon_shape, self.__pen, QBrush(self.YELLOW_FAINT)).setPos(position)

                else:
                    self.__scene.addPolygon(hexagon_shape, self.__pen, self.__brush).setPos(position)
                    tile = Tile(row_i, col_i, position, None)
                    self.__tiles.append(tile)

    def __display_current_player(self, player_name: str) -> None:
        try:
            self.__scene.removeItem(self.__c_label_player)
        except Exception:
            pass

        scale = 1.5
        label_text = 'Current player: '
        self.__c_label_player = self.__scene.addSimpleText('')
        self.__c_label_player.setPos(QPointF(0, -100))
        self.__c_label_player.setScale(scale)
        self.__c_label_player.setText(label_text + (player_name or ''))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        click_position = self.mapToScene(event.pos())
        selected_tile = self.__scene.itemAt(click_position, QTransform())
        self.__brush.setColor(self.__current_player.color)

        if selected_tile is not None:
            tiles_from_list = list([tile for tile in self.__tiles if tile.position == selected_tile.pos()])
            if len(tiles_from_list) == 0:
                return 0
            else:
                tile_from_list = tiles_from_list[0]

            if tile_from_list.owner is None:
                tile_from_list.owner = self.__current_player
                self.__paint_graphic_item(selected_tile, brush=self.__brush)
                self.__handle_graph(tile_from_list, self.__current_player)
                if not self.__check_path():
                    self.__change_player()

    def __handle_graph(self, tile, player) -> None:
        player.tile_graph.add_vertex(tile)

        for possible_position in self.__possible_neighbours_positions:
            for t in self.__tiles:
                if t.col == tile.col + possible_position['col_offset'] and \
                        t.row == tile.row + possible_position['row_offset'] and \
                        t.owner == player:
                    player.tile_graph.add_edge({t, tile})

    def __check_path(self) -> bool:
        player_tiles = list([item for item in self.__tiles if item.owner == self.__current_player])

        if self.__current_player.direction_type == 'col':
            first_dir_tiles = list([item for item in player_tiles if item.col == 1])
            last_dir_tiles = list([item for item in player_tiles if item.col == self.__game_board_size - 1])
        else:
            first_dir_tiles = list([item for item in player_tiles if item.row == 1])
            last_dir_tiles = list([item for item in player_tiles if item.row == self.__game_board_size - 1])

        if len(first_dir_tiles) == 0 or len(last_dir_tiles) == 0:
            return False
        else:
            for ft in first_dir_tiles:
                for lt in last_dir_tiles:
                    if self.__current_player.tile_graph.find_path(ft, lt) is not None:
                        self.__restart_game(f'{self.__current_player.name} wins! Do you want to play again?')
                        return True
        return False

    def __change_player(self) -> None:
        if self.__current_player is None:
            self.__current_player = self.__player_1
        elif self.__current_player == self.__player_1:
            self.__current_player = self.__player_2
        else:
            self.__current_player = self.__player_1
        self.__display_current_player(self.__current_player.name)

    @staticmethod
    def __paint_graphic_item(graphic_item: QGraphicsPolygonItem,
                             pen: QPen = None,
                             brush: QBrush = None) -> None:
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
