from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QDataWidgetMapper, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QWidget)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # Set up the model.
        self.setupModel()

        # Set up the widgets.
        nameLabel = QLabel("Na&me:")
        nameEdit = QLineEdit()
        addressLabel = QLabel("&Address:")
        addressEdit = QTextEdit()
        ageLabel = QLabel("A&ge (in years):")
        ageSpinBox = QSpinBox()
        self.nextButton = QPushButton("&Next")
        self.previousButton = QPushButton("&Previous")
        nameLabel.setBuddy(nameEdit)
        addressLabel.setBuddy(addressEdit)
        ageLabel.setBuddy(ageSpinBox)

        # Set up the mapper.
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(nameEdit, 0)
        self.mapper.addMapping(addressEdit, 1)
        self.mapper.addMapping(ageSpinBox, 2)

        # Set up connections and layouts.
        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)
        self.mapper.currentIndexChanged.connect(self.updateButtons)

        layout = QGridLayout()
        layout.addWidget(nameLabel, 0, 0, 1, 1)
        layout.addWidget(nameEdit, 0, 1, 1, 1)
        layout.addWidget(self.previousButton, 0, 2, 1, 1)
        layout.addWidget(addressLabel, 1, 0, 1, 1)
        layout.addWidget(addressEdit, 1, 1, 2, 1)
        layout.addWidget(self.nextButton, 1, 2, 1, 1)
        layout.addWidget(ageLabel, 3, 0, 1, 1)
        layout.addWidget(ageSpinBox, 3, 1, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Simple Widget Mapper")
        self.mapper.toFirst()

    def setupModel(self):
        self.model = QStandardItemModel(5, 3, self)
        names = ("Alice", "Bob", "Carol", "Donald", "Emma")
        addresses = ("<qt>123 Main Street<br/>Market Town</qt>",
                     "<qt>PO Box 32<br/>Mail Handling Service"
                     "<br/>Service City</qt>",
                     "<qt>The Lighthouse<br/>Remote Island</qt>",
                     "<qt>47338 Park Avenue<br/>Big City</qt>",
                     "<qt>Research Station<br/>Base Camp<br/>Big Mountain</qt>")
        ages = ("20", "31", "32", "19", "26")

        for row, name in enumerate(names):
            item = QStandardItem(name)
            self.model.setItem(row, 0, item)
            item = QStandardItem(addresses[row])
            self.model.setItem(row, 1, item)
            item = QStandardItem(ages[row])
            self.model.setItem(row, 2, item)

    def updateButtons(self, row):
        self.previousButton.setEnabled(row > 0)
        self.nextButton.setEnabled(row < self.model.rowCount() - 1)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())