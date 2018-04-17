from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QtCore import *

class QLineWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.createTable()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID Branch","ID Node\nParent","ID Node\nChild","Q branch\n[vAr]","Q loss\n[Var]"])