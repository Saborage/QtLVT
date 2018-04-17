from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from app.views.widgets.inputs.branch_input_widget import BranchInputWidget
#from app.views.widgets.inputs.line_input_widget import LineInputWidget
from app.views.widgets.inputs.node_input_widget import NodeInputWidget
from app.views.widgets.inputs.slack_input_widget import SlackInputWidget
from app.views.widgets.inputs.user_input_widget import UserInputWidget

class NetworkInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):

        self.layout = QStackedLayout()
        self.layout.addWidget(BranchInputWidget(self))
        #self.layout.addWidget(LineInputWidget(self))
        self.layout.addWidget(NodeInputWidget(self))
        self.layout.addWidget(SlackInputWidget(self))
        self.layout.addWidget(UserInputWidget(self))

        self.layout.setCurrentIndex(0)

        self.setLayout(self.layout)

    def showBranch(self):
        self.layout.setCurrentIndex(0)

    def showNode(self):
        self.layout.setCurrentIndex(1)

    def showSlack(self):
        self.layout.setCurrentIndex(2)

    def showUser(self):
        self.layout.setCurrentIndex(3)
