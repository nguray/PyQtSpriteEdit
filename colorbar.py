#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QColorDialog


class ColorRect(QtCore.QRect):

    color = QtGui.QColor(0, 0, 0, 0)

    def __init__(self, c):
        QtCore.QRect.__init__(self)
        self.color = c

    def draw(self, qp):
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


class MyColorBar(QWidget):
    '''
    classdocs
    '''

    foreColorChanged = QtCore.pyqtSignal(QtGui.QColor)
    backColorChanged = QtCore.pyqtSignal(QtGui.QColor)

    cellsize = 18
    selectedForeColor = ColorRect(QtGui.QColor(0, 0, 0, 255))
    selectedBackColor = ColorRect(QtGui.QColor(0, 0, 0, 0))

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QWidget.__init__(self, parent)

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
        for lin in self.palette:
            linPalette = self.palette[lin]
            y = self.cellsize * lin
            c = 0
            for colorRect in linPalette:
                x = self.cellsize * c + 2 * self.cellsize
                c += 1
                colorRect.setRect(x + 1, y + 1, self.cellsize - 2,
                                  self.cellsize - 2)
                colorRect.draw(qp)

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x = mousePos.x()
        y = mousePos.y()
        for lin in self.palette:
            linPalette = self.palette[lin]
            for colorRect in linPalette:
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

    def savePalette(self):
        with open("palette.cfg", 'w') as outF:
            c = self.selectedForeColor.color.rgba()
            outF.write(str(c))
            outF.write("\n")
            c = self.selectedBackColor.color.rgba()
            outF.write(str(c))
            outF.write("\n")
            for lin in self.palette:
                linPalette = self.palette[lin]
                for colorRect in linPalette:
                    c = colorRect.color.rgba()
                    outF.write(str(c))
                    outF.write("\n")

    def loadPalette(self):
        with open("palette.cfg", 'r') as inF:
            strlin = inF.readline()
            self.selectedForeColor.color.setRgba(int(strlin))
            strlin = inF.readline()
            self.selectedBackColor.color.setRgba(int(strlin))
            for lin in self.palette:
                linPalette = self.palette[lin]
                for colorRect in linPalette:
                    strlin = inF.readline()
                    if strlin != "":
                        colorRect.color.setRgba(int(strlin))

    def mouseDoubleClickEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x = mousePos.x()
        y = mousePos.y()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            for lin in self.palette:
                linPalette = self.palette[lin]
                for colorRect in linPalette:
                    if colorRect.contains(x, y):
                        col = QColorDialog.getColor()
                        if col.isValid():
                            colorRect.color = col
                            self.repaint()
                            self.savePalette()

    def paintEvent(self, e):

        qp = QtGui.QPainter()

        qp.begin(self)

        self.drawPalette(qp)

        s = 2 * self.cellsize - 2
        self.selectedBackColor.setRect(1, 1, s, s)
        self.selectedBackColor.draw(qp)

        s = int(1.5 * self.cellsize - 2)
        self.selectedForeColor.setRect(1, 1, s, s)
        self.selectedForeColor.draw(qp)

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
        