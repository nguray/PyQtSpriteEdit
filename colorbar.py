#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''
import os.path
from PyQt5 import QtGui, QtCore, QtWidgets

class ColorRect(QtCore.QRect):
    """
    Color Cell Rectangle
    """
 
    def __init__(self, c):
        QtCore.QRect.__init__(self)
        self.color = c

    def draw(self, qp: QtGui.QPainter):
        if self.color.rgba() == QtGui.QColor(255, 255, 255, 255).rgba():
            qp.setPen(QtGui.QColor(0, 0, 0, 255))
            qp.setBrush(self.color)
            qp.drawRect(self)
        else:
            qp.setBrush(self.color)
            if self.color.alpha() == 0:
                qp.setPen(QtGui.QColor(100, 10, 10, 255))
                qp.drawRect(self)
                self.adjust(0, 0, 1, 1)
                qp.drawLine(self.topLeft(), self.bottomRight())
                qp.drawLine(self.topRight(), self.bottomLeft())
            else:
                qp.setPen(self.color)
                qp.drawRect(self)
    
    def drawFrame(self, qp):
        r = 255-self.color.red()
        g = 255-self.color.green()
        b = 255-self.color.blue()
        qp.setPen(QtGui.QColor(r, g, b, 255))
        qp.drawLine(self.topLeft(),self.topRight())
        qp.drawLine(self.topRight(),self.bottomRight())
        qp.drawLine(self.bottomRight(),self.bottomLeft())
        qp.drawLine(self.bottomLeft(),self.topLeft())

class MyColorBar(QtWidgets.QWidget):
    '''
    Colors palette
    '''

    foreColorChanged = QtCore.pyqtSignal(QtGui.QColor)
    backColorChanged = QtCore.pyqtSignal(QtGui.QColor)


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QWidget.__init__(self, parent)

        self.cellSize = 18
        self.selectedForeColor = ColorRect(QtGui.QColor(0, 0, 0, 255))
        self.selectedBackColor = ColorRect(QtGui.QColor(0, 0, 0, 0))

        self.fDragForegroundColor = False
        self.dragColorRect = ColorRect(QtGui.QColor(0, 0, 0, 0))

        self.palette = {
            0: [
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 255)),
                ColorRect(QtGui.QColor(127, 127, 127, 255)),
                ColorRect(QtGui.QColor(136, 0, 21, 255)),
                ColorRect(QtGui.QColor(237, 28, 36, 255)),
                ColorRect(QtGui.QColor(255, 127, 39, 255)),
                ColorRect(QtGui.QColor(255, 242, 0, 255)),
                ColorRect(QtGui.QColor(34, 177, 79, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255)),
                ColorRect(QtGui.QColor(0, 162, 232, 255))
            ],
            1: [
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0)),
                ColorRect(QtGui.QColor(0, 0, 0, 0))
            ]
        }

    def changeForeColor(self, c):
        self.selectedForeColor.color = c
        self.repaint()

    def changeBackColor(self, c):
        self.selectedBackColor.color = c
        self.repaint()

    def drawPalette(self, qp):
        for lin in self.palette.items():
            y = self.cellSize * lin[0]
            for c,colorRect in enumerate(lin[1]):
                x = self.cellSize * c + 2 * self.cellSize
                colorRect.setRect(x + 1, y + 1, self.cellSize - 2,
                                  self.cellSize - 2)
                colorRect.draw(qp)

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x = mousePos.x()
        y = mousePos.y()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            if self.selectedForeColor.contains(x,y):
                self.fDragForegroundColor = True
                self.dragColorRect.color = self.selectedForeColor.color
                offSet = self.cellSize // 2
                self.dragColorRect.setRect(x-offSet,y-offSet,self.cellSize,self.cellSize)
                self.repaint()
            else:
                for lin in self.palette.items():
                    for colorRect in lin[1]:
                        if colorRect.contains(x, y):
                            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                                self.selectedForeColor.color = colorRect.color
                                self.foreColorChanged.emit(self.selectedForeColor.color)
                                self.repaint()
                                return
                            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                                self.selectedBackColor.color = colorRect.color
                                self.backColorChanged.emit(self.selectedBackColor.color)
                                self.repaint()
                                return
                            
    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        if self.fDragForegroundColor:
            x = mousePos.x()
            y = mousePos.y()
            if self.fDragForegroundColor:
                offSet = self.cellSize // 2
                self.dragColorRect.setRect(x-offSet,y-offSet,self.cellSize,self.cellSize)
                self.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        if self.fDragForegroundColor:
            x = mousePos.x()
            y = mousePos.y()
            for lin in self.palette.items():
                for colorRect in lin[1]:
                    if colorRect.contains(x, y):
                        colorRect.color = self.dragColorRect.color
            self.fDragForegroundColor = False
            self.dragColorRect.setRect(0,0,0,0)
            self.repaint()            

    def savePalette(self):
        with open("palette.cfg", 'w') as outF:
            c = self.selectedForeColor.color.rgba()
            outF.write(str(c))
            outF.write("\n")
            c = self.selectedBackColor.color.rgba()
            outF.write(str(c))
            outF.write("\n")
            for lin in self.palette.items():
                for colorRect in lin[1]:
                    c = colorRect.color.rgba()
                    outF.write(str(c))
                    outF.write("\n")

    def loadPalette(self):
        if os.path.exists("palette.cfg"):
            with open("palette.cfg", 'r') as inF:
                strlin = inF.readline()
                self.selectedForeColor.color.setRgba(int(strlin))
                strlin = inF.readline()
                self.selectedBackColor.color.setRgba(int(strlin))
                for lin in self.palette.items():
                    for colorRect in lin[1]:
                        strlin = inF.readline()
                        if strlin != "":
                            colorRect.color.setRgba(int(strlin))

    def mouseDoubleClickEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x = mousePos.x()
        y = mousePos.y()
        for lin in self.palette.items():
            for colorRect in lin[1]:
                if colorRect.contains(x, y):
                    col = QtWidgets.QColorDialog.getColor()
                    if col.isValid():
                        colorRect.color = col
                        self.repaint()
                        self.savePalette()

    def paintEvent(self, e):

        qp = QtGui.QPainter()

        qp.begin(self)

        self.drawPalette(qp)

        s = 2 * self.cellSize - 2
        self.selectedBackColor.setRect(1, 1, s, s)
        self.selectedBackColor.draw(qp)

        s = int(1.5 * self.cellSize - 2)
        self.selectedForeColor.setRect(1, 1, s, s)
        self.selectedForeColor.draw(qp)

        if self.fDragForegroundColor:
            self.dragColorRect.draw(qp)
            self.dragColorRect.drawFrame(qp)

        # size = self.size()
        # w = size.width()
        # h = size.height()
        # pen = QtGui.QPen(QtGui.QColor(20,20,20),1,QtCore.Qt.SolidLine)
        # qp.setPen(pen)
        # qp.drawRect(0,0,w-1,h-1)

        qp.end()

    # Deleting (Calling destructor)
    def __del__(self):
        self.savePalette()
        