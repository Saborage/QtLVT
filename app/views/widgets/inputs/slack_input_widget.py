from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SlackInputWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout(self)

        self.groupbox = QGroupBox("Slack")
        self.btn_add_slack = QPushButton("Add Slack", self)

        self.bislayout = QVBoxLayout(self)

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

        self.bislayout.addLayout(self.vol_min_layout)

        self.groupbox.setLayout(self.bislayout)

        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.btn_add_slack)

        self.setLayout(self.layout)











