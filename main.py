#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from editarea import MyEditArea
from colorbar import MyColorBar
from spritebar import SpriteBar

# MSYS2 Shell : pyrcc5 -o resources.py qtspriteedit.qrc
import  resources

class myAbout(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(myAbout, self).__init__(parent)
        # Create widgets
        self.l1 = QtWidgets.QLabel("PyQtSpriteEdit version 0.1")
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


class MyWindow(QtWidgets.QMainWindow):

    filename = ""
    spriteBarX = 16

    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def newFile(self):
        """
        """
        self.filename = ""
        self.editarea.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        self.repaint()

    def newFile16(self):
        """
        """
        self.filename = ""
        self.editarea.init16Sprite()
        w, _ = self.editarea.computeSize()
        self.spriteBarX = w + 16
        self.hbox.setStretch(1, 20)
        self.repaint()

    def newFile32(self):
        """
        """
        self.filename = ""
        self.editarea.init32Sprite()
        w, _ = self.editarea.computeSize()
        self.spriteBarX = w + 16
        self.hbox.setStretch(1, 36)
        self.repaint()

    def newFile64(self):
        self.filename = ""
        self.editarea.init64Sprite()
        w, _ = self.editarea.computeSize()
        self.spriteBarX = w + 16
        self.hbox.setStretch(1, 68)
        self.repaint()

    def openFile(self):
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
        self.editarea.setEditMode(self.editarea.EDIT.Select)

    def setPencilEditMode(self):
        self.unCheckAllToolBarBtns()
        self.pencilModeAction.setChecked(True)
        self.editarea.setEditMode(self.editarea.EDIT.Pencil)

    def setLineEditMode(self):
        self.unCheckAllToolBarBtns()
        self.lineModeAction.setChecked(True)
        self.editarea.setEditMode(self.editarea.EDIT.DrawLine)

    def setRectangleEditMode(self):
        self.unCheckAllToolBarBtns()
        self.rectangleModeAction.setChecked(True)
        self.editarea.setEditMode(self.editarea.EDIT.DrawRectangle)

    def setEllipseEditMode(self):
        self.unCheckAllToolBarBtns()
        self.ellipseModeAction.setChecked(True)
        self.editarea.setEditMode(self.editarea.EDIT.DrawEllipse)

    def setFillEditMode(self):
        self.unCheckAllToolBarBtns()
        self.fillerModeAction.setChecked(True)
        self.editarea.setEditMode(self.editarea.EDIT.Fill)

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
        d = myAbout(self)
        d.show()

    def updateCursorPosDisplay(self, x, y):
        self.statusBar().showMessage("cursor : ({0},{1})".format(x, y))
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
        #newAction = QAction(QtGui.QIcon('icons/document-open.png'), 'New', self)
        newAction = QtWidgets.QAction('New', self)
        #newAction.setIcon(QtGui.QIcon('application-exit-symbolic.svg'))
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        # newAction.triggered.connect(self.newFile)

        newAction16 = QtWidgets.QAction('16 x 16', self)
        newAction16.triggered.connect(self.newFile16)
        newAction32 = QtWidgets.QAction('32 x 32', self)
        newAction32.triggered.connect(self.newFile32)
        newAction64 = QtWidgets.QAction('64 x 64', self)
        newAction64.triggered.connect(self.newFile64)

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
            u'Rotate 90° clockwise', self)
        rotate90ClockAction.triggered.connect(self.rotate90ClockImage)

        rotate90AntiClockAction = QtWidgets.QAction(
            QtGui.QIcon(':res/rotate_90_anticlockwise.png'),
            u'Rotate 90° counter-clockwise', self)
        rotate90AntiClockAction.triggered.connect(self.rotate90AntiClockImage)

        aboutAction = QtWidgets.QAction(QtGui.QIcon(':res/help-browser.png'), 'About',
                              self)
        aboutAction.triggered.connect(self.aboutMe)

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.subNewMenu = QtWidgets.QMenu('New')
        self.subNewMenu.setIcon(QtGui.QIcon(':res/document-new.png'))
        self.subNewMenu.addAction(newAction16)
        self.subNewMenu.addAction(newAction32)
        self.subNewMenu.addAction(newAction64)
        self.fileMenu.addMenu(self.subNewMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(openAction)
        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(exitAction)
        self.EditMenu = menubar.addMenu('&Edit')
        self.EditMenu.addAction(undoAction)
        self.EditMenu.addSeparator()
        self.EditMenu.addAction(cutAction)
        self.EditMenu.addAction(copyAction)
        self.EditMenu.addAction(pasteAction)

        self.ImageMenu = menubar.addMenu('Image')
        self.ImageMenu.addAction(mirrorHorizontalAction)
        self.ImageMenu.addAction(mirrorVerticalAction)
        self.ImageMenu.addAction(rotate90ClockAction)
        self.ImageMenu.addAction(rotate90AntiClockAction)

        self.AboutMenu = menubar.addMenu('?')
        self.AboutMenu.addAction(aboutAction)

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

        # -- Zone edition
        self.hbox.setStretch(0, w)
        # -- Sprite barre
        self.hbox.setStretch(1, 40)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(self.hbox)
        vbox.addWidget(self.colorbar)
        vbox.setStretch(0, h)
        vbox.setStretch(1, self.colorbar.cellsize*2+2)

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
