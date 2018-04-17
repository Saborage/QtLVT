from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class NodeInputWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout(self)

        self.groupbox = QGroupBox("Node")
        self.btn_add_node = QPushButton("Add Node", self)

        self.bislayout = QVBoxLayout(self)

        self.user_layout = QHBoxLayout(self)
        self.user_label = QLabel(self)
        self.user_label.setText("User :")
        self.user_edit = QLineEdit()
        self.user_layout.addWidget(self.user_label,1)
        self.user_layout.addWidget(self.user_edit,2)

        self.bislayout.addLayout(self.user_layout)

        self.vol_min_layout = QHBoxLayout(self)
        self.vol_min_label = QLabel(self)
        self.vol_min_label.setText("Voltage Min (Vmin) :")
        self.vol_min_edit = QLineEdit()
        self.vol_min_layout.addWidget(self.vol_min_label,1)
        self.vol_min_layout.addWidget(self.vol_min_edit,2)

        self.bislayout.addLayout(self.vol_min_layout)

        self.vol_max_layout = QHBoxLayout(self)
        self.vol_max_label = QLabel(self)
        self.vol_max_label.setText("Voltage Max (Vmax) :")
        self.vol_max_edit = QLineEdit()
        self.vol_max_layout.addWidget(self.vol_max_label,1)
        self.vol_max_layout.addWidget(self.vol_max_edit,2)

        self.bislayout.addLayout(self.vol_max_layout)



        self.groupbox.setLayout(self.bislayout)

        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.btn_add_node)

        self.setLayout(self.layout)











