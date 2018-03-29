from PyQt5.QtCore import pyqtProperty, Qt, QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout,
        QItemEditorCreatorBase, QItemEditorFactory, QTableWidget,
        QTableWidgetItem, QWidget)


class ColorListEditor(QComboBox):
    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)

        self.populateList()

    def getColor(self):
        color = self.itemData(self.currentIndex(), Qt.DecorationRole)
        return color

    def setColor(self, color):
        self.setCurrentIndex(self.findData(color, Qt.DecorationRole))

    color = pyqtProperty(QColor, getColor, setColor, user=True)

    def populateList(self):
        for i, colorName in enumerate(QColor.colorNames()):
            color = QColor(colorName)
            self.insertItem(i, colorName)
            self.setItemData(i, color, Qt.DecorationRole)


class ColorListItemEditorCreator(QItemEditorCreatorBase):
    def createWidget(self, parent):
        return ColorListEditor(parent)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        factory = QItemEditorFactory()
        factory.registerEditor(QVariant.Color, ColorListItemEditorCreator())
        QItemEditorFactory.setDefaultFactory(factory)

        self.createGUI()

    def createGUI(self):
        tableData = [
            ("Alice", QColor('aliceblue')),
            ("Neptun", QColor('aquamarine')),
            ("Ferdinand", QColor('springgreen'))
        ]

        table = QTableWidget(3, 2)
        table.setHorizontalHeaderLabels(["Name", "Hair Color"])
        table.verticalHeader().setVisible(False)
        table.resize(150, 50)

        for i, (name, color) in enumerate(tableData):
            nameItem = QTableWidgetItem(name)
            colorItem = QTableWidgetItem()
            colorItem.setData(Qt.DisplayRole, color)
            table.setItem(i, 0, nameItem)
            table.setItem(i, 1, colorItem)

        table.resizeColumnToContents(0)
        table.horizontalHeader().setStretchLastSection(True)

        layout = QGridLayout()
        layout.addWidget(table, 0, 0)
        self.setLayout(layout)

        self.setWindowTitle("Color Editor Factory")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())