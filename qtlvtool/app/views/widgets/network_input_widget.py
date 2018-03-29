from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class NetworkInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.label = QLabel("Inputs",self)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.label)
