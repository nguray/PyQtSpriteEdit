#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''

from PyQt5 import QtGui, QtCore, QtWidgets


class SpriteBar(QtWidgets.QWidget):
    '''
    Sprites palette
    '''

    spriteChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QWidget.__init__(self, parent)

        self.setMinimumWidth(48)
        self.setMaximumWidth(48)

        self.list_sprites = []
        self.list_sprites_names = []
        self.nb_cells = 8
        self.current_sprite = 0
        self.cell_size = 48

        for i in range(0, self.nb_cells):
            if (i == 0):
                s = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
                s.fill(QtGui.qRgba(0, 0, 0, 0))
                self.list_sprites.append(s)
            else:
                self.list_sprites.append(None)
            self.list_sprites_names.append("")

    def mouse2Index(self, mx, my):
        '''
        '''
        size = self.size()
        w = size.width()
        # h = size.height()
        centerX = w / 2
        xLeft = centerX - self.cell_size / 2
        xRight = xLeft + self.cell_size
        if ((mx > xLeft) and (mx < xRight)):
            id = int((my - 4) / self.cell_size)
            if (id < self.nb_cells):
                return id
        return -1

    def getCurSrpite(self):
        '''
        '''
        return self.list_sprites[self.current_sprite]

    def mousePressEvent(self, mouseEvent):
        '''
        '''
        mousePos = mouseEvent.pos()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            id = self.mouse2Index(mousePos.x(), mousePos.y())
            if id >= 0:
                if self.list_sprites[id] is None:
                    s = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
                    self.list_sprites[id] = s
                    s.fill(QtGui.qRgba(0, 0, 0, 0))
                self.current_sprite = id
                self.spriteChanged.emit()
                self.repaint()

    def drawSprites(self, qp):
        '''
        '''
        size = self.size()
        w = size.width()
        centerX = w / 2
        for i,s in enumerate(self.list_sprites):
            if s!=None:
                x = centerX - s.width() / 2
                y = i * self.cell_size + self.cell_size/2 - s.height()/2 + 4
                qp.drawImage(QtCore.QPoint(int(x), int(y)), s)

    def loadSprite(self, fileName):
        '''
        '''
        s = self.list_sprites[self.current_sprite]
        self.list_sprites_names[self.current_sprite] = fileName
        s.load(fileName, "PNG")

    def saveAsSprite(self, fileName):
        '''
        '''
        s = self.list_sprites[self.current_sprite]
        self.list_sprites_names[self.current_sprite] = fileName
        s.save(fileName, "PNG")


    def saveSprite(self):
        '''
        '''
        s = self.list_sprites[self.current_sprite]
        fileName = self.list_sprites_names[self.current_sprite]
        s.save(fileName, "PNG")


    def drawSelectMark(self, qp):
        '''
        '''
        size = self.size()
        w = size.width() - 1
        xLeft = 0
        xRight = xLeft + w
        pen = QtGui.QPen(QtGui.QColor(20, 20, 255), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        yTop = self.current_sprite * self.cell_size
        yBottom = yTop + self.cell_size
        # -- Top Left
        qp.drawLine(xLeft, yTop, xLeft, yTop+4)
        qp.drawLine(xLeft, yTop, xLeft+4, yTop)
        # -- Bottom Right
        qp.drawLine(xRight, yBottom, xRight, yBottom-4)
        qp.drawLine(xRight, yBottom, xRight-4, yBottom)
        # -- Top Right
        qp.drawLine(xRight, yTop, xRight-4, yTop)
        qp.drawLine(xRight, yTop, xRight, yTop+4)
        # -- Bottom Left
        qp.drawLine(xLeft, yBottom, xLeft, yBottom-4)
        qp.drawLine(xLeft, yBottom, xLeft+4, yBottom)


    def paintEvent(self, e):
        '''
        '''
        qp = QtGui.QPainter()

        qp.begin(self)

        size = self.size()
        w = size.width()
        # h = size.height()
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        #qp.drawRect(0, 0, w - 1, (8 * self.cell_size + 4) - 1)

        xLeft  = 0
        xRight = w - 1
        yTop   = 0
        for i in range(0,len(self.list_sprites)):
            qp.drawLine(xLeft, yTop, xRight, yTop)
            yTop += self.cell_size
        qp.drawLine(xLeft, yTop, xRight, yTop)
        qp.drawLine(xLeft, 0, xLeft, yTop)
        qp.drawLine(xRight, 0, xRight, yTop)


        self.drawSprites(qp)
        self.drawSelectMark(qp)

        qp.end()
