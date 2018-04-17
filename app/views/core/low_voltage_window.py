import os
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from resource.icons import resource_rc
from app.views.widgets.network_editor_widget import NetworkEditorWidget
from app.views.widgets.network_input_widget import NetworkInputWidget

class LowVoltageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filename = None
        self.initUI()

    def initUI(self):
        # menu & toolbar
        self.createMenus()
        self.createToolbar()

        # create node editor widget
        nodeeditor = NetworkEditorWidget(self)
        nodeeditor.scene.addHasBeenModifiedListener(self.changeTitle)
        self.setCentralWidget(nodeeditor)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        nodeeditor.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        self.setGeometry(200, 200, 1200, 800)
        self.changeTitle()
        self.setWindowIcon(QIcon(":/icons/blason-poly.jpg"))
        #self.setStyleSheet(open("networkstyle.qss", "r").read())
        self.show()

    # Function for create action
    def createAct(self, icon, name, shortcut, tooltip, callback):
        act = QAction(QIcon(icon),name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    # Function create Menubar
    def createMenus(self):
        # initialize Menu
        menubar = self.menuBar()
        # File Menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.createAct(":/icons/new.png",'&New', 'Ctrl+N', "Create new graph", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(":/icons/load.png",'&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        fileMenu.addAction(self.createAct(":/icons/save.png",'&Save', 'Ctrl+S', "Save file", self.onFileSave))
        fileMenu.addAction(self.createAct(":/icons/saveplus.png",'Save &As...', 'Ctrl+Shift+S', "Save file as...", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(":/icons/quit.png",'E&xit', 'Ctrl+Q', "Exit application", self.close))
        # Edit Menu
        editMenu = menubar.addMenu('&Edit')
        editMenu.addSeparator()
        editMenu.addAction(self.createAct(":/icons/delete.png",'&Delete', 'Del', "Delete selected items", self.onEditDelete))

    # Function create Toolbar
    def createToolbar(self):
        # Controller to create element
        self.creaToolBar = self.addToolBar("Creation")
        self.creaToolBar.addAction(self.createAct(":/icons/node.png",'&Node', '', "Bracket creation", NetworkInputWidget.showNode))
        self.creaToolBar.addAction(self.createAct(":/icons/user.png", '&User', '', "User creation", NetworkInputWidget.showUser))
        self.creaToolBar.addAction(self.createAct(None, '&Line', '', "Line creation", NetworkInputWidget.showBranch))
        # Controller to undo, redo, delete element
        self.conToolBar = self.addToolBar("Control")
        self.conToolBar.addAction(self.createAct(":/icons/undo.png", '&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        self.conToolBar.addAction(self.createAct(":/icons/redo.png", '&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo))
        self.conToolBar.addAction(self.createAct(":/icons/delete.png",'&Delete', 'Del', "Delete selected items", self.onEditDelete))
        # Controller to ctrl+(x,c,v)
        self.xcvToolBar = self.addToolBar("xcv")
        self.xcvToolBar.addAction(self.createAct(":/icons/cut.png", '&Cut', 'Ctrl+X', "Cut to clipboard", self.onEditCut))
        self.xcvToolBar.addAction(self.createAct(":/icons/copy.png", '&Copy', 'Ctrl+C', "Copy to clipboard", self.onEditCopy))
        self.xcvToolBar.addAction(self.createAct(None, '&Paste', 'Ctrl+V', "Paste from clipboard", self.onEditPaste))

    # Change title of the window
    def changeTitle(self):
        title = "GELEC - LowVoltageTool - "
        if self.filename is None:
            title += "New"
        else:
            title += os.path.basename(self.filename)
        if self.centralWidget().scene.has_been_modified:
            title += "*"
        self.setWindowTitle(title)
    # Stop event when is saved
    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    # Function return the central widget when scene has been modified
    def isModified(self):
        return self.centralWidget().scene.has_been_modified

    # Generate a pop-up to ask if we have saved
    def maybeSave(self):
        if not self.isModified():
            return True
        res = QMessageBox.warning(self, "About to loose your work?",
                "The document has been modified.\n Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
              )
        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False
        return True

    # Show position to mouse in the statut bar
    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    # Generate a new scene
    def onFileNew(self):
        if self.maybeSave():
            self.centralWidget().scene.clear()
            self.filename = None
            self.changeTitle()

    # Load a file with a scene
    def onFileOpen(self):
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(self, 'Open graph from file')
            if fname == '':
                return
            if os.path.isfile(fname):
                self.centralWidget().scene.loadFromFile(fname)
                self.filename = fname
                self.changeTitle()

    # Save the scene's file
    def onFileSave(self):
        if self.filename is None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)
        return True

    # Choice where save
    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file')
        if fname == '':
            return False
        self.filename = fname
        self.onFileSave()
        return True

    # Undo action
    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    # Redo action
    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    # Delete selection of elements in scene
    def onEditDelete(self):
        self.centralWidget().scene.grScene.views()[0].deleteSelected()

    # Cut an element selected
    def onEditCut(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=True)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    # Copy an element selected
    def onEditCopy(self):
        data = self.centralWidget().scene.clipboard.serializeSelected(delete=False)
        str_data = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(str_data)

    # Paste the element
    def onEditPaste(self):
        raw_data = QApplication.instance().clipboard().text()
        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print("Pasting of not valid json data!", e)
            return
        # check if the json data are correct
        if 'nodes' not in data:
            print("JSON does not contain any nodes!")
            return
        self.centralWidget().scene.clipboard.deserializeFromClipboard(data)
