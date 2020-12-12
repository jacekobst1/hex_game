# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QStackedWidget, QHBoxLayout

from imgbtn import ImgBtn


class MyWin(QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()

        self.setGeometry(800, 800, 1000, 1000)
        self.setWindowTitle('Hex game')

        self.init_ui()

    def init_ui(self):
        self.label = QLabel(self)
        self.label.setText('To jest label')
        self.label.move(50, 50)

        self.btn1 = QPushButton(self)
        self.btn1.setIcon(QIcon('hexagon.png'))
        self.btn1.setIconSize(QSize(24,24))

        self.btn1.clicked.connect(self.clicked)

        pic = QLabel(self)
        pic.setPixmap(QPixmap("hexagon.png"))
        pic.move(34, 35)
        pic.show()

        self.layout = QHBoxLayout(self)
        self.button = ImgBtn(QPixmap("hexagon.png.png"))
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)


    def clicked(self):
        self.label.setText('Kliknięto')


if __name__ == "__main__":
    app = QApplication([])
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
