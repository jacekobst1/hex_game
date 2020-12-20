from PySide2.QtGui import QColor

from classes.graph import Graph


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
