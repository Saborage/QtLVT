from collections import OrderedDict
from app.serialization.network_serializable import Serializable
from PyQt5.QtWidgets import *

class QDMNetworkContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    #Initialize
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Add data")
        #self.layout.addWidget(self.wdg_label)
        #self.layout.addWidget(QDMTextEdit("Put information"))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False


class QDMTextEdit(QTextEdit):
    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)