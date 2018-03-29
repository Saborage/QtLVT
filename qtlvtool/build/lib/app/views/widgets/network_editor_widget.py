from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from app.views.elements.scenes.network_scene import Scene
from app.views.elements.network_node import Node
from app.views.elements.network_edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
from app.views.graphics.network_graphics_view import QDMGraphicsView
from app.views.widgets.network_input_widget import NetworkInputWidget
from app.views.widgets.network_output_widget import NetworkOutputWidget


class NetworkEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'networkstyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        # splitter window
        topright = NetworkInputWidget(self)
        bottomright = NetworkOutputWidget(self)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(topright)
        splitter1.addWidget(bottomright)

        # crate graphics scene
        self.scene = Scene()

        # self.grScene = self.scene.grScene
        self.addNodes()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.view)
        splitter2.addWidget(splitter1)
        self.layout.addWidget(splitter2)
        self.setLayout(self.layout)


    def addNodes(self):
        node1 = Node(self.scene, "Slack Node", inputs=[], outputs=[1,5])
        node2 = Node(self.scene, "Node 1", inputs=[1,2,3], outputs=[1,2,3])
        node3 = Node(self.scene, "Node 2", inputs=[1,2,3], outputs=[1,2,3])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[2], edge_type=EDGE_TYPE_DIRECT)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_DIRECT)


    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.grScene.addRect(-100, -100, 200, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))


        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)


        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)


        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)


    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))