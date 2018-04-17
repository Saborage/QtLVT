from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.views.widgets.tabs.vnode_widget import VNodeWidget
from app.views.widgets.tabs.iline_widget import ILineWidget
from app.views.widgets.tabs.pline_widget import PLineWidget
from app.views.widgets.tabs.qline_widget import QLineWidget


class NetworkOutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.tabs_widget = QTabWidget(self)

        self.tab1 = VNodeWidget(self)
        self.tab2 = ILineWidget(self)
        self.tab3 = PLineWidget(self)
        self.tab4 = QLineWidget(self)

        self.tabs_widget.addTab(self.tab1, "V node")
        self.tabs_widget.addTab(self.tab2, "I line")
        self.tabs_widget.addTab(self.tab3, "P line")
        self.tabs_widget.addTab(self.tab4, "Q line")

        self.btn_load_flow = QPushButton("Do Load Flow",self)
        self.btn_load_flow.clicked.connect(self.on_click)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.tabs_widget)
        self.vbox.addWidget(self.btn_load_flow)

    @pyqtSlot()
    def on_click(self):
        print("Simulation de loadflow")

