#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

Refactoring for python 3.11 in June 2024

@author: Raymond NGUYEN THANH
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from editarea import MyEditArea
from colorbar import MyColorBar
from spritebar import SpriteBar

from editmode import EditMode

# MSYS2 Shell : pyrcc5 -o resources.py qtspriteedit.qrc
import  resources

class MyAbout(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create widgets
        self.l1 = QtWidgets.QLabel("PyQtSpriteEdit version 0.2")
        self.l1.setAlignment(QtCore.Qt.AlignCenter)
        self.l2 = QtWidgets.QLabel("Raymond NGUYEN THANH")
        self.l2.setAlignment(QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton("OK")
        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.l2)
        hBox1 = QtWidgets.QHBoxLayout()
        hBox1.addStretch()
        hBox1.addWidget(self.button)
        hBox1.addStretch()
        layout.addLayout(hBox1)
        # Set dialog layout
        self.setLayout(layout)
        self.resize(250, 100)
        self.setWindowTitle('About PyQtSpriteEdit')
        # Add button signal to greetings slot
        self.button.clicked.connect(self.accept)

class NewSpriteDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(256)
        self.setMinimumHeight(156)
        self.imageWidth = 0
        self.imageHeight = 0

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.addButton("Ok", QtWidgets.QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton("Cancel", QtWidgets.QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.accepted.connect(self.onAccept)
        self.buttonBox.rejected.connect(self.onCancel)

        fm = self.fontMetrics()
        rect1 = fm.boundingRect('Width')
        rect2 = fm.boundingRect('Height')

        labelWidth = rect1.width() if rect1.width()>rect2.width() else rect1.width()

        imageFrame = QtWidgets.QGroupBox('Image')
        imageFrame.setStyleSheet(
                'QGroupBox {'
                 'border: 1px solid rgb(120,120,120);'
                 'border-radius: 4px;'
                 'margin-top: 6px;}'
                 'QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'left: 7px;'
                 'padding: -10px 5px 0px 5px;}')

        vBoxLayout = QtWidgets.QVBoxLayout()
        vBoxLayout1 = QtWidgets.QVBoxLayout()

        hBoxLayout1 = QtWidgets.QHBoxLayout()
        widthLabel = QtWidgets.QLabel('Width')
        widthLabel.setMinimumWidth(labelWidth)
        widthLabel.setMaximumWidth(labelWidth)
        self.widthEdit = QtWidgets.QSpinBox()
        self.widthEdit.setValue(32)
        self.widthEdit.setMinimumWidth(64)
        hBoxLayout1.addStretch()
        hBoxLayout1.addWidget(widthLabel,0,QtCore.Qt.AlignmentFlag.AlignLeft)
        hBoxLayout1.addWidget(self.widthEdit,0,QtCore.Qt.AlignmentFlag.AlignLeft)
        hBoxLayout1.addStretch()

        hBoxLayout2 = QtWidgets.QHBoxLayout()
        heightLabel = QtWidgets.QLabel('Height')
        heightLabel.setMinimumWidth(labelWidth)
        heightLabel.setMaximumWidth(labelWidth)
        self.heightEdit = QtWidgets.QSpinBox()
        self.heightEdit.setValue(32)
        self.heightEdit.setMinimumWidth(64)
        hBoxLayout2.addStretch()
        hBoxLayout2.addWidget(heightLabel,0,QtCore.Qt.AlignmentFlag.AlignLeft)
        hBoxLayout2.addWidget(self.heightEdit,0,QtCore.Qt.AlignmentFlag.AlignLeft)
        hBoxLayout2.addStretch()

        vBoxLayout1.addStretch()
        vBoxLayout1.addLayout(hBoxLayout1)
        vBoxLayout1.addLayout(hBoxLayout2)
        vBoxLayout1.addStretch()

        imageFrame.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft or QtCore.Qt.AlignmentFlag.AlignVCenter)
        imageFrame.setLayout(vBoxLayout1)

        vBoxLayout.addWidget(imageFrame)
        vBoxLayout.addWidget(self.buttonBox)

        self.setLayout(vBoxLayout)
        self.setWindowTitle('New Sprite')

    def onAccept(self):
        self.imageWidth = int(self.widthEdit.text())
        self.imageHeight = int(self.heightEdit.text())
        self.accept()

    def onCancel(self):
        self.imageWidth = 0
        self.imageHeight = 0
        self.reject()


class MyWindow(QtWidgets.QMainWindow):
    ''' Application window  '''

    filename = ""
    spriteBarX = 16

    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def newFile(self):
        """ Create new sprite image """
        self.filename = ""
        d = NewSpriteDlg(self)
        d.setModal(True)
        if d.exec_():
            print(f'{d.imageWidth},{d.imageHeight}')
            self.spritebar.newSprite( d.imageWidth, d.imageHeight)
            self.editarea.setEditSprite(self.spritebar.getCurSrpite())
            self.repaint()

    def openFile(self):
        """ Load a sprite image """
        inputfilename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".",
                                                       "Images (*.png)")
        if inputfilename:
            tmpName = str(inputfilename)
            if tmpName.upper().endswith(".PNG"):
                self.editarea.resetSelect()
                self.filename = inputfilename
                self.spritebar.loadSprite(self.filename)
                self.editarea.setEditSprite(self.spritebar.getCurSrpite())
                self.repaint()

    def saveAsFile(self):
        inputfilename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', ".",
                                                       "Images (*.png)")
        if inputfilename:
            tmpName = str(inputfilename)
            if not tmpName.upper().endswith(".PNG"):
                inputfilename.append(".png")
            self.filename = inputfilename
            self.spritebar.saveAsSprite(self.filename)

    def saveFile(self):
        self.spritebar.saveSprite()

    def unCheckAllToolBarBtns(self):
        self.selectRectModeAction.setChecked(False)
        self.pencilModeAction.setChecked(False)
        self.lineModeAction.setChecked(False)
        self.rectangleModeAction.setChecked(False)
        self.ellipseModeAction.setChecked(False)
        self.fillerModeAction.setChecked(False)

    def setSelectEditMode(self):
        self.unCheckAllToolBarBtns()
        self.selectRectModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.SELECT)

    def setPencilEditMode(self):
        self.unCheckAllToolBarBtns()
        self.pencilModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.PENCIL)

    def setLineEditMode(self):
        self.unCheckAllToolBarBtns()
        self.lineModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.POLYLINE)

    def setRectangleEditMode(self):
        self.unCheckAllToolBarBtns()
        self.rectangleModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.RECTANGLE)

    def setEllipseEditMode(self):
        self.unCheckAllToolBarBtns()
        self.ellipseModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.ELLIPSE)

    def setFillEditMode(self):
        self.unCheckAllToolBarBtns()
        self.fillerModeAction.setChecked(True)
        self.editarea.setEditMode(EditMode.FILL)

    def undoEdit(self):
        self.editarea.doUndo()
        self.repaint()

    def cutEdit(self):
        self.editarea.doCutRect()
        self.repaint()

    def copyEdit(self):
        self.editarea.doCopyRect()
        self.repaint()

    def pasteEdit(self):
        self.editarea.doPasteRect()
        self.repaint()

    def updateFileName(self, path):
        self.filename = path

    def mirrorHorizontalImage(self):
        self.editarea.doMirrorHorizontal()

    def mirrorVerticalImage(self):
        self.editarea.doMirrorVertical()

    def rotate90ClockImage(self):
        self.editarea.doRotate90Clock()

    def rotate90AntiClockImage(self):
        self.editarea.doRotate90AntiClock()

    def aboutMe(self):
        d = MyAbout(self)
        d.show()

    def updateCursorPosDisplay(self, x, y):
        self.statusBar().showMessage(f"cursor : ({x},{y})")
        self.repaint()

    def spriteChanged(self):
        self.editarea.setEditSprite(self.spritebar.getCurSrpite())

    def initUI(self):
        self.x = -1
        self.y = -1
        self.filename = ""
        self.statusBar()

        # ------------------------------------------------
        # Menu Actions

        # File Menu Actions
        newAction = QtWidgets.QAction(QtGui.QIcon(':res/document-new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)

        openAction = QtWidgets.QAction(QtGui.QIcon(':res/document-open.png'), 'Open',
                             self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)

        saveAction = QtWidgets.QAction(QtGui.QIcon(':res/document-save.png'), 'Save',
                             self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QtWidgets.QAction(QtGui.QIcon(':res/document-save-as.png'),
                               'Save As...', self)
        saveAsAction.setShortcut('Ctrl+S')
        saveAsAction.setStatusTip('Save As current file')
        saveAsAction.triggered.connect(self.saveAsFile)

        exitAction = QtWidgets.QAction(QtGui.QIcon(':res/process-stop.png'), '&Exit',
                             self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Edit Menu Actions
        undoAction = QtWidgets.QAction(QtGui.QIcon(':res/edit-undo.png'), 'Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.setStatusTip('Undo')
        undoAction.triggered.connect(self.undoEdit)

        cutAction = QtWidgets.QAction(QtGui.QIcon(':res/edit-cut.png'), 'Cut', self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.setStatusTip('Cut')
        cutAction.triggered.connect(self.cutEdit)

        copyAction = QtWidgets.QAction(QtGui.QIcon(':res/edit-copy.png'), 'Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy')
        copyAction.triggered.connect(self.copyEdit)

        pasteAction = QtWidgets.QAction(QtGui.QIcon(':res/edit-paste.png'), 'Paste',
                              self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.setStatusTip('Paste')
        pasteAction.triggered.connect(self.pasteEdit)

        # --
        mirrorHorizontalAction = QtWidgets.QAction(
            QtGui.QIcon(':res/mirror_horizontal.png'), 'Mirror Horizontal',
            self)
        mirrorHorizontalAction.triggered.connect(self.mirrorHorizontalImage)

        mirrorVerticalAction = QtWidgets.QAction(
            QtGui.QIcon(':res/mirror_vertical.png'), 'Mirror Vertical', self)
        mirrorVerticalAction.triggered.connect(self.mirrorVerticalImage)

        rotate90ClockAction = QtWidgets.QAction(
            QtGui.QIcon(':res/rotate_90_clockwise.png'),
            'Rotate 90° clockwise', self)
        rotate90ClockAction.triggered.connect(self.rotate90ClockImage)

        rotate90AntiClockAction = QtWidgets.QAction(
            QtGui.QIcon(':res/rotate_90_anticlockwise.png'),
            'Rotate 90° counter-clockwise', self)
        rotate90AntiClockAction.triggered.connect(self.rotate90AntiClockImage)

        aboutAction = QtWidgets.QAction(QtGui.QIcon(':res/help-browser.png'), 'About',
                              self)
        aboutAction.triggered.connect(self.aboutMe)

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(openAction)
        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(exitAction)
        self.editMenu = menubar.addMenu('&Edit')
        self.editMenu.addAction(undoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(cutAction)
        self.editMenu.addAction(copyAction)
        self.editMenu.addAction(pasteAction)

        self.imageMenu = menubar.addMenu('Image')
        self.imageMenu.addAction(mirrorHorizontalAction)
        self.imageMenu.addAction(mirrorVerticalAction)
        self.imageMenu.addAction(rotate90ClockAction)
        self.imageMenu.addAction(rotate90AntiClockAction)

        self.aboutMenu = menubar.addMenu('?')
        self.aboutMenu.addAction(aboutAction)

        # ------------------------------------------------
        # Toolbar Actions
        self.selectRectModeAction = QtWidgets.QAction(QtGui.QIcon(':res/SelectRect.png'),
                                       'Select', self)
        self.selectRectModeAction.setStatusTip('Select Tool')
        self.selectRectModeAction.setCheckable(True)
        self.selectRectModeAction.triggered.connect(self.setSelectEditMode)

        self.pencilModeAction = QtWidgets.QAction(QtGui.QIcon(':res/Pencil.png'),
                                   'Pencil', self)
        self.pencilModeAction.setStatusTip('Pencil Tool')
        self.pencilModeAction.setCheckable(True)
        self.pencilModeAction.triggered.connect(self.setPencilEditMode)

        self.lineModeAction = QtWidgets.QAction(QtGui.QIcon(':res/DrawLine.png'), 'Draw Line',
                                 self)
        self.lineModeAction.setStatusTip('Draw Line Tool')
        self.lineModeAction.setCheckable(True)
        self.lineModeAction.triggered.connect(self.setLineEditMode)

        self.rectangleModeAction = QtWidgets.QAction(QtGui.QIcon(':res/DrawRectangle.png'),
                                      'Draw Rectangle', self)
        self.rectangleModeAction.setStatusTip('Draw Rectangle Tool')
        self.rectangleModeAction.setCheckable(True)
        self.rectangleModeAction.triggered.connect(self.setRectangleEditMode)

        self.ellipseModeAction = QtWidgets.QAction(QtGui.QIcon(':res/DrawEllipse.png'),
                                    'Draw Ellipse', self)
        self.ellipseModeAction.setStatusTip('Draw Ellipse Tool')
        self.ellipseModeAction.setCheckable(True)
        self.ellipseModeAction.triggered.connect(self.setEllipseEditMode)

        self.fillerModeAction = QtWidgets.QAction(QtGui.QIcon(':res/Filler.png'), 'Fill', self)
        self.fillerModeAction.setStatusTip('Fill Tool')
        self.fillerModeAction.setCheckable(True)
        self.fillerModeAction.triggered.connect(self.setFillEditMode)

        # --
        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.selectRectModeAction)
        self.toolbar.addAction(self.pencilModeAction)
        self.toolbar.addAction(self.lineModeAction)
        self.toolbar.addAction(self.rectangleModeAction)
        self.toolbar.addAction(self.ellipseModeAction)
        self.toolbar.addAction(self.fillerModeAction)

        # --
        self.editarea : MyEditArea = MyEditArea(self)
        w, h = self.editarea.computeSize()
        self.editarea.resize(w, h)

        self.spriteBarX = w + 16
        self.spriteBarY = 16 + menubar.height()+self.toolbar.height()

        self.colorbar = MyColorBar(self)
        self.colorbar.loadPalette()

        self.editarea.foregroundColor = self.colorbar.selectedForeColor.color
        self.editarea.backgroundColor = self.colorbar.selectedBackColor.color

        self.editarea.cursorPosChanged.connect(self.updateCursorPosDisplay)

        self.editarea.pipetForeColor.connect(self.colorbar.changeForeColor)
        self.editarea.pipetBackColor.connect(self.colorbar.changeBackColor)

        self.colorbar.foreColorChanged.connect(self.editarea.changeForeColor)
        self.colorbar.backColorChanged.connect(self.editarea.changeBackColor)

        self.editarea.fileNameChanged.connect(self.updateFileName)

        # ------------------------------------------------
        self.spritebar = SpriteBar(self)
        self.editarea.setEditSprite(self.spritebar.getCurSrpite())

        self.spritebar.spriteChanged.connect(self.spriteChanged)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.editarea)
        self.hbox.addWidget(self.spritebar)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(self.hbox)
        vbox.addWidget(self.colorbar)
        vbox.setStretch(0, h)
        vbox.setStretch(1, self.colorbar.cellSize*2+2)

        centralWidget = QtWidgets.QWidget(self)
        centralWidget.setLayout(vbox)

        self.setCentralWidget(centralWidget)

        self.setPencilEditMode()

        self.setGeometry(300, 300, 500, 550)
        self.setMinimumSize(500, 550)

        self.setWindowTitle('SpriteEditor')

        self.editarea.setFocus()


def main():
    
    app = QtWidgets.QApplication(sys.argv)
    # Afficher les icons dans les menus
    app.setAttribute(QtCore.Qt.AA_DontShowIconsInMenus, False)
    myMain = MyWindow()
    myMain.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
