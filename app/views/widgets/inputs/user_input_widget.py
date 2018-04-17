from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class UserInputWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout(self)

        self.groupbox = QGroupBox("User")
        self.btn_add_slack = QPushButton("Add User", self)

        self.bislayout = QVBoxLayout(self)

        self.phase_req_layout = QHBoxLayout(self)
        self.phase_req_label = QLabel(self)
        self.phase_req_label.setText("Phase required :")
        self.phase_req_input = QComboBox(self)
        self.phase_req_input.addItem("----")
        self.phase_req_input.addItem("1000")
        self.phase_req_input.addItem("1001")
        self.phase_req_input.addItem("0100")
        self.phase_req_input.addItem("0101")
        self.phase_req_input.addItem("0010")
        self.phase_req_input.addItem("0011")
        self.phase_req_input.addItem("1100")
        self.phase_req_input.addItem("1101")
        self.phase_req_input.addItem("1010")
        self.phase_req_input.addItem("1011")
        self.phase_req_input.addItem("0110")
        self.phase_req_input.addItem("0111")
        self.phase_req_input.addItem("1110")
        self.phase_req_input.addItem("1111")
        self.phase_req_layout.addWidget(self.phase_req_label, 1)
        self.phase_req_layout.addWidget(self.phase_req_input, 2)

        self.bislayout.addLayout(self.phase_req_layout)

        self.vol_max_layout = QHBoxLayout(self)
        self.vol_max_label = QLabel(self)
        self.vol_max_label.setText("Voltage Max (Vmax) :")
        self.vol_max_edit = QLineEdit()
        self.vol_max_layout.addWidget(self.vol_max_label,1)
        self.vol_max_layout.addWidget(self.vol_max_edit,2)

        self.bislayout.addLayout(self.vol_max_layout)

        self.groupbox.setLayout(self.bislayout)

        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.btn_add_slack)

        self.setLayout(self.layout)











