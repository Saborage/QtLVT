from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class BranchInputWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout(self)

        self.groupbox = QGroupBox("Branch")
        self.btn_add_branch = QPushButton("Add Branch", self)

        self.bislayout = QVBoxLayout(self)

        self.P_layout = QHBoxLayout(self)
        self.phase_label = QLabel(self)
        self.phase_label.setText("Phase :")
        self.phase_input = QComboBox(self)
        self.phase_input.addItem("----")
        
        self.phase_input.addItem("1000")
        self.phase_input.addItem("1001")
        self.phase_input.addItem("0100")
        self.phase_input.addItem("0101")
        self.phase_input.addItem("0010")
        self.phase_input.addItem("0011")
        self.phase_input.addItem("1100")
        self.phase_input.addItem("1101")
        self.phase_input.addItem("1010")
        self.phase_input.addItem("1011")
        self.phase_input.addItem("0110")
        self.phase_input.addItem("0111")
        self.phase_input.addItem("1110")
        self.phase_input.addItem("1111")
        self.P_layout.addWidget(self.phase_label, 1)
        self.P_layout.addWidget(self.phase_input, 2)


        self.bislayout.addLayout(self.P_layout)

        self.R_layout = QHBoxLayout(self)
        self.resistance_label = QLabel(self)
        self.resistance_label.setText("Resistance (R) :")
        self.resistance_edit = QLineEdit()
        self.R_layout.addWidget(self.resistance_label,1)
        self.R_layout.addWidget(self.resistance_edit,2)

        self.bislayout.addLayout(self.R_layout)

        self.Re_layout = QHBoxLayout(self)
        self.react_label = QLabel(self)
        self.react_label.setText("Reactance (X) :")
        self.react_edit = QLineEdit()
        self.Re_layout.addWidget(self.react_label,1)
        self.Re_layout.addWidget(self.react_edit,2)

        self.bislayout.addLayout(self.Re_layout)

        self.groupbox.setLayout(self.bislayout)

        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.btn_add_branch)

        self.setLayout(self.layout)











