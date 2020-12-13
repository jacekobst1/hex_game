import math
from PySide2.QtCore import QPointF
from PySide2.QtGui import QPolygonF


class QHexagonShape(QPolygonF):
    """
    polygon with number of sides, a radius, angle of the first point
    hexagon is made with 6 sides
    radius denotes the size of the shape, 
    angle of 
    0 makes a horizontal aligned hexagon (first point points flat), 
    90 makes a vertical aligned hexagon (first point points upwards)
    The hexagon needs the width and height of the current widget or window 
    in order to place itself. 
    the position x and y denote the position relative to the current width and height
    """

    def __init__(self, x, y, radius, angle):
        QPolygonF.__init__(self)

        self.x = x
        self.y = y
        self.sides = 6
        self.radius = radius
        self.angle = angle

        # angle per step
        w = 360 / self.sides

        # add the points of polygon per side
        for i in range(self.sides):
            t = w * i + self.angle

            # horizontal alignment
            x = self.x + self.radius * math.cos(math.radians(t))
            # vertical alignment
            y = self.y + self.radius * math.sin(math.radians(t))

            # add side to polygon
            self.append(QPointF(x, y))
