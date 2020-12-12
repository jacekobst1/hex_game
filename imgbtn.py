from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QAbstractButton


class ImgBtn(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImgBtn, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()