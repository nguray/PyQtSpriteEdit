#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMenu
from collections import namedtuple


class _Rect:
    def __init__(self, l, t, r, b):
        self.left = l
        self.top = t
        self.right = r
        self.bottom = b

    def normalize(self):
        if (self.left > self.right):
            d = self.left
            self.left = self.right
            self.right = d

        if (self.top > self.bottom):
            d = self.top
            self.top = self.bottom
            self.bottom = d

    def empty(self):
        self.left = -1
        self.top = -1
        self.right = -1
        self.bottom = -1

    def isEmpty(self):
        return ((self.left == self.right) and (self.top == self.bottom))

    def isValid(self):
        return (self.left < self.right) and (self.top < self.bottom)

    def width(self):
        if (self.right > self.left):
            return self.right - self.left
        else:
            return self.left - self.right

    def height(self):
        if (self.bottom > self.top):
            return self.bottom - self.top
        else:
            return self.top - self.bottom

    def contains(self, x, y):
        if (x >= self.left) and (x <= self.right) and (y >= self.top) and (
                y <= self.bottom):
            return True
        return False

    def translate(self, dx, dy):
        self.left += dx
        self.right += dx
        self.top += dy
        self.bottom += dy


class _Point:
    def __init__(self, cx, cy):
        self.x = cx
        self.y = cy


class DrawPolyLineMode:

    nb_points = 0
    list_points = []
    selected_point = None

    def __init__(self, outer):
        self.outer = outer

    def initDrawLine(self):
        self.list_points = []
        self.nb_points = 0

    def drawPolylineOnSprite(self):
        if (self.nb_points == 1):
            self.outer.sprite.setPixel(self.x, self.y,
                                       self.outer.foregroundColor.rgba())
        elif (self.nb_points > 1):
            qp = QtGui.QPainter(self.outer.sprite)
            qp.setPen(self.outer.foregroundColor)
            fFirst = True
            for pt in self.list_points:
                if fFirst:
                    fFirst = False
                    pt2 = pt
                else:
                    pt1 = pt2
                    pt2 = pt
                    qp.drawLine(pt1.x, pt1.y, pt2.x, pt2.y)

    def hitPolylinePoints(self, x, y):
        for pt in self.list_points:
            if ((pt.x == x) and (pt.y == y)):
                return pt
        return None

    def translatePolyline(self, dx, dy):
        for pt in self.list_points:
            pt.x += dx
            pt.y += dy

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.nb_points == 0:
                    # Pour le 1er point
                    self.outer.backupSprite()
                    pt = _Point(self.x, self.y)
                    self.list_points.append(pt)
                    self.nb_points += 1
                    self.outer.sprite.setPixel(
                        self.x, self.y, self.outer.foregroundColor.rgba())
                    self.selected_point = pt
                else:
                    # Pour les points suivants
                    self.selected_point = self.hitPolylinePoints(
                        self.x, self.y)
                    if (self.selected_point is None):
                        pt = self.list_points[self.nb_points - 1]
                        if (pt.x != self.x) or (pt.y != self.y):
                            pt = _Point(self.x, self.y)
                            self.list_points.append(pt)
                            self.nb_points += 1
                            # ReDraw Polyline
                            self.outer.restoreSprite()
                            self.drawPolylineOnSprite()
                            self.outer.repaint()
                            self.selected_point = pt
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.selected_point is not None:
                    if (self.selected_point.x !=
                            self.x) or (self.selected_point.y != self.y):
                        if modifiers == QtCore.Qt.ControlModifier:
                            dx = self.x - self.selected_point.x
                            dy = self.y - self.selected_point.y
                            self.translatePolyline(dx, dy)
                        else:
                            self.selected_point.x = self.x
                            self.selected_point.y = self.y
                        # ReDraw Polyline
                        self.outer.restoreSprite()
                        self.drawPolylineOnSprite()
                        self.outer.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            #
            self.initDrawLine()
            self.outer.repaint()

    def drawLivePolyLine(self, qp):
        for pt in self.list_points:
            if self.outer.InSprite(pt.x, pt.y):
                x1, y1 = self.outer.pixToMouseCoord(pt.x, pt.y)
                p1 = QtGui.QPen(QtGui.QColor(0, 0, 255, 255), 2)
                qp.setPen(p1)
                qp.setBrush(QtGui.QBrush(QtGui.QColor(128, 128, 255, 255)))
                qp.drawRect(x1, y1, self.outer.pixSize, self.outer.pixSize)


class PencilMode:
    def __init__(self, outer):
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.foregroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()


    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QtGui.QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.foregroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()

    def keyPressEvent(self, e):
        pass


class SelectMode:

    pasteRect = _Rect(0, 0, 0, 0)
    hit_paste = False
    hit_paste_x = -1
    hit_paste_y = -1

    hit_handle = -1
    hit_pix_x = -1
    hit_pix_y = -1

    hit_pt = -1

    selectRect = _Rect(0, 0, 0, 0)

    cpy_width = 0
    cpy_height = 0

    def __init__(self, outer):
        self.outer = outer

    def initSelectRect(self):
        self.selectRect.left = -1
        self.selectRect.right = -1
        self.selectRect.top = -1
        self.selectRect.bottom = -1
        self.hit_handle = -1
        self.hit_pix_x = -1
        self.hit_pix_y = -1

    def initPasteRect(self):
        self.pasteRect.left = -1
        self.pasteRect.right = -1
        self.pasteRect.top = -1
        self.pasteRect.bottom = -1

    def drawPasteRect(self, qp):
        pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        x1, y1 = self.outer.pixToMouseCoord(self.pasteRect.left,
                                            self.pasteRect.top)
        x2, y2 = self.outer.pixToMouseCoord(self.pasteRect.right + 1,
                                            self.pasteRect.bottom + 1)
        qp.drawLine(x1, y1, x2, y1)
        qp.drawLine(x2, y1, x2, y2)
        qp.drawLine(x2, y2, x1, y2)
        qp.drawLine(x1, y2, x1, y1)

    def drawSelectRect(self, qp):
        normRect = _Rect(self.selectRect.left, self.selectRect.top,
                         self.selectRect.right, self.selectRect.bottom)
        normRect.normalize()
        pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_Xor)
        x1, y1 = self.outer.pixToMouseCoord(normRect.left, normRect.top)
        x2, y2 = self.outer.pixToMouseCoord(normRect.right + 1,
                                            normRect.bottom + 1)
        qp.drawLine(x1, y1, x2, y1)
        qp.drawLine(x2, y1, x2, y2)
        qp.drawLine(x2, y2, x1, y2)
        qp.drawLine(x1, y2, x1, y1)
        # Draw Select Handles
        pixSize = self.outer.pixSize
        x2, y2 = self.outer.pixToMouseCoord(normRect.right, normRect.bottom)
        qp.drawLine(x1 + pixSize, y1, x1 + pixSize, y1 + pixSize)
        qp.drawLine(x1 + pixSize, y1 + pixSize, x1, y1 + pixSize)
        qp.drawLine(x2, y1, x2, y1 + pixSize)
        qp.drawLine(x2, y1 + pixSize, x2 + pixSize, y1 + pixSize)
        qp.drawLine(x2, y2, x2 + pixSize, y2)
        qp.drawLine(x2, y2, x2, y2 + pixSize)
        qp.drawLine(x1, y2, x1 + pixSize, y2)
        qp.drawLine(x1 + pixSize, y2, x1 + pixSize, y2 + pixSize)

    def hitSelectRect(self, x, y):
        if not self.selectRect.isEmpty():
            myRect = _Rect(self.selectRect.left, self.selectRect.top,
                           self.selectRect.right, self.selectRect.bottom)
            myRect.normalize()
            if (x == myRect.left) and (y == myRect.top):
                return 0
            elif (x == myRect.right) and (y == myRect.top):
                return 1
            elif (x == myRect.right) and (y == myRect.bottom):
                return 2
            elif (x == myRect.left) and (y == myRect.bottom):
                return 3
        return -1

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if (self.pasteRect.contains(self.x, self.y)):
                    self.hit_paste = True
                    self.hit_paste_x = self.x
                    self.hit_paste_y = self.y
                else:
                    self.hit_paste = False
                    self.initPasteRect()
                    self.hit_handle = self.hitSelectRect(self.x, self.y)
                    if self.hit_handle != -1:
                        self.hit_pix_x = self.x
                        self.hit_pix_y = self.y
                    else:
                        self.hit_pt = -1
                        self.selectRect.left = self.x
                        self.selectRect.top = self.y
                        self.selectRect.right = self.x
                        self.selectRect.bottom = self.y
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        self.hit_handle = -1

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if self.hit_paste:
                if (self.x != self.hit_paste_x) or (self.y !=
                                                    self.hit_paste_y):
                    dx = self.x - self.hit_paste_x
                    dy = self.y - self.hit_paste_y
                    self.outer.restoreSprite()
                    self.pasteRect.left += dx
                    self.pasteRect.top += dy
                    self.pasteRect.right += dx
                    self.pasteRect.bottom += dy
                    qp = QtGui.QPainter()
                    qp.begin(self.outer.sprite)
                    w = self.cpy_width + 1
                    h = self.cpy_height + 1
                    qp.drawImage(
                        QtCore.QRect(self.pasteRect.left, self.pasteRect.top,
                                     w, h), self.outer.sprite_cpy,
                        QtCore.QRect(0, 0, w, h))
                    qp.end()
                    self.hit_paste_x = self.x
                    self.hit_paste_y = self.y
                    self.outer.repaint()
            elif self.hit_handle != -1:
                dx = self.x - self.hit_pix_x
                dy = self.y - self.hit_pix_y
                if (dx != 0) or (dy != 0):
                    self.hit_pix_x = self.x
                    self.hit_pix_y = self.y
                    if modifiers == QtCore.Qt.ControlModifier:
                        self.selectRect.translate(dx, dy)
                    else:
                        if (self.hit_handle == 0):  # Pt Haut Gauche
                            if (self.x < self.selectRect.right):
                                self.selectRect.left = self.x
                            if (self.y < self.selectRect.bottom):
                                self.selectRect.top = self.y
                        elif (self.hit_handle == 1):  # Pt Haut Droite
                            if (self.x > self.selectRect.left):
                                self.selectRect.right = self.x
                            if (self.y < self.selectRect.bottom):
                                self.selectRect.top = self.y
                        elif (self.hit_handle == 2):  # Pt Bas Droite
                            if (self.x > self.selectRect.left):
                                self.selectRect.right = self.x
                            if (self.y > self.selectRect.top):
                                self.selectRect.bottom = self.y
                        elif (self.hit_handle == 3):  # Pt Bas Gauche
                            if (self.x < self.selectRect.right):
                                self.selectRect.left = self.x
                            if (self.y > self.selectRect.top):
                                self.selectRect.bottom = self.y
                    self.outer.repaint()
            elif (self.selectRect.right != self.x) or (self.selectRect.bottom
                                                       != self.y):
                self.selectRect.right = self.x
                self.selectRect.bottom = self.y
                self.outer.repaint()

    def keyPressEvent(self, e):
        pass


class DrawRectangleMode:

    live_rect = _Rect(-1, -1, -1, -1)
    hit_handle = -1
    hit_pix_x = -1
    hit_pix_y = -1

    def __init__(self, outer):
        self.outer = outer

    def initDrawRect(self):
        self.live_rect.left = -1
        self.live_rect.right = -1
        self.live_rect.top = -1
        self.live_rect.bottom = -1
        self.hit_handle = -1
        self.hit_pix_x = -1
        self.hit_pix_y = -1

    def hitLiveRect(self, x, y):
        if not self.live_rect.isEmpty():
            myRect = _Rect(self.live_rect.left, self.live_rect.top,
                           self.live_rect.right, self.live_rect.bottom)
            myRect.normalize()
            if (x == myRect.left) and (y == myRect.top):
                return 0
            elif (x == myRect.right) and (y == myRect.top):
                return 1
            elif (x == myRect.right) and (y == myRect.bottom):
                return 2
            elif (x == myRect.left) and (y == myRect.bottom):
                return 3
        return -1

    def drawLiveRect(self, qp):
        myRect = _Rect(self.live_rect.left, self.live_rect.top,
                       self.live_rect.right, self.live_rect.bottom)
        myRect.normalize()
        x1, y1 = self.outer.pixToMouseCoord(myRect.left, myRect.top)
        x2, y2 = self.outer.pixToMouseCoord(myRect.right, myRect.bottom)
        p1 = QtGui.QPen(QtGui.QColor(0, 0, 255, 255), 2)
        qp.setPen(p1)
        qp.setBrush(QtGui.QBrush(QtGui.QColor(128, 128, 255, 255)))
        pixSize = self.outer.pixSize
        if self.outer.InSprite(myRect.left, myRect.top):
            qp.drawRect(x1, y1, pixSize, pixSize)
        if self.outer.InSprite(myRect.right, myRect.top):
            qp.drawRect(x2, y1, pixSize, pixSize)
        if self.outer.InSprite(myRect.right, myRect.bottom):
            qp.drawRect(x2, y2, pixSize, pixSize)
        if self.outer.InSprite(myRect.left, myRect.bottom):
            qp.drawRect(x1, y2, pixSize, pixSize)

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.hit_handle = self.hitLiveRect(self.x, self.y)
                if self.hit_handle != -1:
                    self.hit_pix_x = self.x
                    self.hit_pix_y = self.y
                else:
                    self.outer.backupSprite()
                    self.live_rect.left = self.x
                    self.live_rect.top = self.y
                    self.live_rect.right = self.x
                    self.live_rect.bottom = self.y
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        if not self.live_rect.isEmpty():
            self.live_rect.normalize()
        self.hit_handle = -1

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.hit_handle != -1:
                    dx = self.x - self.hit_pix_x
                    dy = self.y - self.hit_pix_y
                    if (dx != 0) or (dy != 0):
                        self.hit_pix_x = self.x
                        self.hit_pix_y = self.y
                        if modifiers == QtCore.Qt.ControlModifier:
                            self.live_rect.translate(dx, dy)
                        else:
                            if (self.hit_handle == 0):  # Pt Haut Gauche
                                if (self.x < self.live_rect.right):
                                    self.live_rect.left = self.x
                                if (self.y < self.live_rect.bottom):
                                    self.live_rect.top = self.y
                            elif (self.hit_handle == 1):  # Pt Haut Droite
                                if (self.x > self.live_rect.left):
                                    self.live_rect.right = self.x
                                if (self.y < self.live_rect.bottom):
                                    self.live_rect.top = self.y
                            elif (self.hit_handle == 2):  # Pt Bas Droite
                                if (self.x > self.live_rect.left):
                                    self.live_rect.right = self.x
                                if (self.y > self.live_rect.top):
                                    self.live_rect.bottom = self.y
                            elif (self.hit_handle == 3):  # Pt Bas Gauche
                                if (self.x < self.live_rect.right):
                                    self.live_rect.left = self.x
                                if (self.y > self.live_rect.top):
                                    self.live_rect.bottom = self.y
                        self.outer.restoreSprite()
                        qp = QtGui.QPainter(self.outer.sprite)
                        qp.setPen(self.outer.foregroundColor)
                        qp.drawRect(self.live_rect.left, self.live_rect.top,
                                    self.live_rect.width(),
                                    self.live_rect.height())
                        self.outer.repaint()
                elif (self.live_rect.right != self.x) or (self.live_rect.bottom
                                                          != self.y):
                    self.outer.restoreSprite()
                    qp = QtGui.QPainter(self.outer.sprite)
                    qp.setPen(self.outer.foregroundColor)
                    self.live_rect.right = self.x
                    self.live_rect.bottom = self.y
                    myRect = _Rect(self.live_rect.left, self.live_rect.top,
                                   self.live_rect.right, self.live_rect.bottom)
                    myRect.normalize()
                    qp.drawRect(myRect.left, myRect.top, myRect.width(),
                                myRect.height())
                    self.outer.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            #
            self.initDrawRect()
            self.outer.repaint()


class DrawEllipseMode:

    live_rect = _Rect(-1, -1, -1, -1)
    hit_handle = -1
    hit_pix_x = -1
    hit_pix_y = -1

    def __init__(self, outer):
        self.outer = outer

    def initDrawEllipse(self):
        self.live_rect.left = -1
        self.live_rect.right = -1
        self.live_rect.top = -1
        self.live_rect.bottom = -1
        self.hit_handle = -1
        self.hit_pix_x = -1
        self.hit_pix_y = -1

    def hitLiveEllipse(self, x, y):
        if not self.live_rect.isEmpty():
            myRect = _Rect(self.live_rect.left, self.live_rect.top,
                           self.live_rect.right, self.live_rect.bottom)
            myRect.normalize()
            if (x == myRect.left) and (y == myRect.top):
                return 0
            elif (x == myRect.right) and (y == myRect.top):
                return 1
            elif (x == myRect.right) and (y == myRect.bottom):
                return 2
            elif (x == myRect.left) and (y == myRect.bottom):
                return 3
        return -1

    def drawLiveEllipse(self, qp):
        myRect = _Rect(self.live_rect.left, self.live_rect.top,
                       self.live_rect.right, self.live_rect.bottom)
        myRect.normalize()
        x1, y1 = self.outer.pixToMouseCoord(myRect.left, myRect.top)
        x2, y2 = self.outer.pixToMouseCoord(myRect.right, myRect.bottom)
        p1 = QtGui.QPen(QtGui.QColor(0, 0, 255, 255), 2)
        qp.setPen(p1)
        qp.setBrush(QtGui.QBrush(QtGui.QColor(128, 128, 255, 255)))
        pixSize = self.outer.pixSize
        if self.outer.InSprite(myRect.left, myRect.top):
            qp.drawRect(x1, y1, pixSize, pixSize)
        if self.outer.InSprite(myRect.right, myRect.top):
            qp.drawRect(x2, y1, pixSize, pixSize)
        if self.outer.InSprite(myRect.right, myRect.bottom):
            qp.drawRect(x2, y2, pixSize, pixSize)
        if self.outer.InSprite(myRect.left, myRect.bottom):
            qp.drawRect(x1, y2, pixSize, pixSize)

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.hit_handle = self.hitLiveEllipse(self.x, self.y)
                if self.hit_handle != -1:
                    self.hit_pix_x = self.x
                    self.hit_pix_y = self.y
                else:
                    self.outer.backupSprite()
                    self.live_rect.left = self.x
                    self.live_rect.top = self.y
                    self.live_rect.right = self.x
                    self.live_rect.bottom = self.y
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        if not self.live_rect.isEmpty():
            self.live_rect.normalize()
        self.hit_handle = -1

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.hit_handle != -1:
                    dx = self.x - self.hit_pix_x
                    dy = self.y - self.hit_pix_y
                    if (dx != 0) or (dy != 0):
                        self.hit_pix_x = self.x
                        self.hit_pix_y = self.y
                        if modifiers == QtCore.Qt.ControlModifier:
                            self.live_rect.translate(dx, dy)
                        else:
                            if (self.hit_handle == 0):  # Pt Haut Gauche
                                if (self.x < self.live_rect.right):
                                    self.live_rect.left = self.x
                                if (self.y < self.live_rect.bottom):
                                    self.live_rect.top = self.y
                            elif (self.hit_handle == 1):  # Pt Haut Droite
                                if (self.x > self.live_rect.left):
                                    self.live_rect.right = self.x
                                if (self.y < self.live_rect.bottom):
                                    self.live_rect.top = self.y
                            elif (self.hit_handle == 2):  # Pt Bas Droite
                                if (self.x > self.live_rect.left):
                                    self.live_rect.right = self.x
                                if (self.y > self.live_rect.top):
                                    self.live_rect.bottom = self.y
                            elif (self.hit_handle == 3):  # Pt Bas Gauche
                                if (self.x < self.live_rect.right):
                                    self.live_rect.left = self.x
                                if (self.y > self.live_rect.top):
                                    self.live_rect.bottom = self.y
                        self.outer.restoreSprite()
                        qp = QtGui.QPainter(self.outer.sprite)
                        qp.setPen(self.outer.foregroundColor)
                        qp.drawEllipse(self.live_rect.left, self.live_rect.top,
                                       self.live_rect.width(),
                                       self.live_rect.height())
                        self.outer.repaint()
                elif (self.live_rect.right != self.x) or (self.live_rect.bottom
                                                          != self.y):
                    self.outer.restoreSprite()
                    qp = QtGui.QPainter(self.outer.sprite)
                    qp.setPen(self.outer.foregroundColor)
                    self.live_rect.right = self.x
                    self.live_rect.bottom = self.y
                    myRect = _Rect(self.live_rect.left, self.live_rect.top,
                                   self.live_rect.right, self.live_rect.bottom)
                    myRect.normalize()
                    qp.drawEllipse(myRect.left, myRect.top, myRect.width(),
                                   myRect.height())
                    self.outer.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            #
            self.initDrawEllipse()
            self.outer.repaint()


class FillMode:
    def __init__(self, outer):
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                # Get Target Color
                iTargetColor = self.outer.sprite.pixel(self.x, self.y)
                iNewColor = self.outer.foregroundColor.rgba()
                self.outer.floodFill(self.x, self.y, iTargetColor, iNewColor)
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        pass

    def keyPressEvent(self, e):
        pass


class PipetMode:
    def __init__(self, outer):
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            c = self.outer.sprite.pixel(self.x, self.y)
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.foregroundColor.setRgba(c)
                self.outer.pipetForeColor.emit(self.outer.foregroundColor)
            else:
                self.outer.backgroundColor.setRgba(c)
                self.outer.pipetBackColor.emit(self.outer.backgroundColor)
            self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        pass

    def keyPressEvent(self, e):
        pass


class MyEditArea(QWidget):
    '''
    classdocs
    '''

    cursorPosChanged = QtCore.pyqtSignal(int, int)
    pipetForeColor = QtCore.pyqtSignal(QtGui.QColor)
    pipetBackColor = QtCore.pyqtSignal(QtGui.QColor)
    fileNameChanged = QtCore.pyqtSignal(str)

    EditeModes = namedtuple('EditModes', [
        'Select', 'Pencil', 'Rubber', 'Pipet', 'DrawLine', 'DrawRectangle',
        'DrawEllipse', 'Fill'
    ])
    EDIT = EditeModes(0, 1, 2, 3, 4, 5, 6, 7)

    x = -1
    y = -1

    edit_mode = 0
    prev_edit_mode = 0

    foregroundColor = QtGui.QColor(0, 0, 255, 255)
    backgroundColor = QtGui.QColor(0, 0, 0, 0)

    pixSize = 12
    nbRowPix = 32
    nbColumnPix = 32

    sprite = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
    sprite_bak = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
    sprite_cpy = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)

    CurEditModeObj = None

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QWidget.__init__(self, parent)

        # ----------------------------------------------------------------------
        myCursorSelect = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorSelect.png", "PNG"), 0, 0)
        myCursorPencil = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorPencil.png", "PNG"), 12, 19)
        myCursorRubber = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRubber1.png", "PNG"), 12, 19)
        myCursorPipet = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorPipet.png", "PNG"), 12, 19)
        myCursorLine = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorLine.png", "PNG"), 12, 19)
        myCursorRectangle = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRectangle.png", "PNG"), 12, 19)
        myCursorEllipse = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorEllipse.png", "PNG"), 12, 19)
        myCursorFill = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorFill.png", "PNG"), 7, 21)
        self.editCursors = [
            myCursorSelect, myCursorPencil, myCursorRubber, myCursorPipet,
            myCursorLine, myCursorRectangle, myCursorEllipse, myCursorFill
        ]

        self.init32Sprite()

        selectRectModeAction = QAction(QtGui.QIcon('SelectRect.png'), 'Select',
                                       self)
        selectRectModeAction.setStatusTip('Select Tool')
        pencilModeAction = QAction(QtGui.QIcon('Pencil.png'), 'Pencil', self)
        pencilModeAction.setStatusTip('Pencil Tool')
        pipetModeAction = QAction(QtGui.QIcon('Pipet.png'), 'Pipet', self)
        pipetModeAction.setStatusTip('Pipet Tool')
        lineModeAction = QAction(QtGui.QIcon('DrawLine.png'), 'Draw Line',
                                 self)
        lineModeAction.setStatusTip('Draw Line Tool')
        rectangleModeAction = QAction(QtGui.QIcon('DrawRectangle.png'),
                                      'Draw Rectangle', self)
        rectangleModeAction.setStatusTip('Draw Rectangle Tool')
        ellipseModeAction = QAction(QtGui.QIcon('DrawEllipse.png'),
                                    'Draw Ellipse', self)
        ellipseModeAction.setStatusTip('Draw Ellipse Tool')
        fillerModeAction = QAction(QtGui.QIcon('Filler.png'), 'Fill', self)
        fillerModeAction.setStatusTip('Fill Tool')

        self.editActions = [
            selectRectModeAction, pencilModeAction,
            pipetModeAction, lineModeAction, rectangleModeAction,
            ellipseModeAction, fillerModeAction
        ]

        # -- Instancier les objects des classes
        self.DrawPolyLineModeObj = DrawPolyLineMode(self)
        self.PencilModeObj = PencilMode(self)
        self.SelectModeObj = SelectMode(self)
        self.DrawRectangleModeObj = DrawRectangleMode(self)
        self.DrawEllipseModeObj = DrawEllipseMode(self)
        self.FillModeObj = FillMode(self)
        self.PipetModeObj = PipetMode(self)
        self.CurEditModeObj = self.SelectModeObj

        self.show()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAcceptDrops(True)

    def init32Sprite(self):
        self.pixSize = 12
        self.nbRowPix = 32
        self.nbColumnPix = 32
        self.sprite = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        self.sprite_bak = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
        self.sprite_cpy = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)

    def init16Sprite(self):
        self.pixSize = 24
        self.nbRowPix = 16
        self.nbColumnPix = 16
        self.sprite = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        self.sprite_bak = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        self.sprite_cpy = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)

    def init64Sprite(self):
        self.pixSize = 8
        self.nbRowPix = 64
        self.nbColumnPix = 64
        self.sprite = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        self.sprite_bak = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)
        self.sprite_cpy = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)

    def contextMenuEvent(self, event):
        """
        """
        pass
        # menu = QMenu(self)

        # for a in self.editActions:
        #     menu.addAction(a)

        # # Afficher le context menu
        # action = menu.exec_(self.mapToGlobal(event.pos()))

        # # Traiter le choix de l'utilisateur
        # for m, a in enumerate(self.editActions):
        #     if a == action:
        #         self.setEditMode(m)

    def resetSelect(self):
        """
            Réinitialser les sélections
        """
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.DrawPolyLineModeObj.initDrawLine()
        self.DrawRectangleModeObj.initDrawRect()
        self.DrawEllipseModeObj.initDrawEllipse()

    def setEditMode(self, m):
        """
        """
        if self.edit_mode != m:
            self.prev_edit_mode = self.edit_mode
            self.edit_mode = m
            self.resetSelect()
            # Changer la forme du curseur de la souris
            #self.setCursor(self.editCursors[self.edit_mode])

            if (self.edit_mode == self.EDIT.Select):  # Select Rectangle Mode
                self.CurEditModeObj = self.SelectModeObj

            elif (self.edit_mode == self.EDIT.Pencil):  # Pencil Mode
                self.CurEditModeObj = self.PencilModeObj

            elif (self.edit_mode == self.EDIT.Pipet):  # Pipet Mode
                self.CurEditModeObj = self.PipetModeObj

            elif (self.edit_mode == self.EDIT.DrawLine):  # Draw line Mode
                self.CurEditModeObj = self.DrawPolyLineModeObj

            elif (self.edit_mode == self.EDIT.DrawRectangle
                  ):  # Draw rectangle Mode
                self.CurEditModeObj = self.DrawRectangleModeObj

            elif (self.edit_mode == self.EDIT.DrawEllipse
                  ):  # Draw ellipse Mode
                self.CurEditModeObj = self.DrawEllipseModeObj

            elif (self.edit_mode == self.EDIT.Fill):  # Fill Mode
                self.CurEditModeObj = self.FillModeObj
            # --
            self.repaint()

    def changeForeColor(self, c):
        self.foregroundColor = c

    def changeBackColor(self, c):
        self.backgroundColor = c

    def computeSize(self):
        w = self.nbColumnPix * self.pixSize + 1
        h = self.nbRowPix * self.pixSize + 1
        return w, h

    def drawGrid(self, qp):
        '''
        '''
        col = QtGui.QColor(50, 50, 50)
        qp.setPen(col)
        for iy in range(0, self.nbRowPix + 1):
            y = iy * self.pixSize
            for ix in range(0, self.nbColumnPix + 1):
                x = ix * self.pixSize
                qp.drawPoint(x, y)

    def mouseToPixCoord(self, mx, my):
        x = int(mx / self.pixSize)
        y = int(my / self.pixSize)
        return x, y

    def pixToMouseCoord(self, px, py):
        mx = px * self.pixSize
        my = py * self.pixSize
        return mx, my

    def drawSpritePixels(self, qp):
        color = QtGui.QColor()
        for y in range(0, self.nbRowPix):
            py = y * self.pixSize + 1
            for x in range(0, self.nbColumnPix):
                px = x * self.pixSize + 1
                icol = self.sprite.pixel(x, y)
                color.setRgba(icol)
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(px, py, self.pixSize - 2, self.pixSize - 2)

    def InSprite(self, x, y):
        if ((x >= 0) and (x < self.nbColumnPix) and (y >= 0)
                and (y < self.nbRowPix)):
            return True
        else:
            return False

    def backupSprite(self):
        self.sprite_bak.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite_bak)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()

    def restoreSprite(self):
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite_bak,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()
        self.repaint()

    def doUndo(self):
        self.restoreSprite()
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.initDrawLine()
        self.initDrawRect()
        self.initDrawEllipse()

    def doCutRect(self):
        if not self.SelectModeObj.selectRect.isEmpty():
            self.sprite_cpy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            # Faire une copie de zone
            qp.begin(self.sprite_cpy)
            self.SelectModeObj.cpy_width = self.SelectModeObj.selectRect.width(
            )
            self.SelectModeObj.cpy_height = self.SelectModeObj.\
                selectRect.height()
            w = self.SelectModeObj.cpy_width + 1
            h = self.SelectModeObj.cpy_height + 1
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), self.sprite,
                QtCore.QRect(self.SelectModeObj.selectRect.left,
                             self.SelectModeObj.selectRect.top, w, h))
            qp.end()
            # Effacer la zone
            qp1 = QtGui.QPainter()
            qp1.begin(self.sprite)
            r, g, b, a = self.backgroundColor.getRgb()
            qp1.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
            qp1.fillRect(
                QtCore.QRect(self.SelectModeObj.selectRect.left,
                             self.SelectModeObj.selectRect.top, w, h),
                QtGui.QColor(r, g, b, a))
            qp1.end()
            self.SelectModeObj.initSelectRect()

    def doCopyRect(self):
        if not self.SelectModeObj.selectRect.isEmpty():
            self.sprite_cpy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            qp.begin(self.sprite_cpy)
            self.SelectModeObj.cpy_width = \
                     self.SelectModeObj.selectRect.width()
            self.SelectModeObj.cpy_height = \
                     self.SelectModeObj.selectRect.height()
            w = self.SelectModeObj.cpy_width + 1
            h = self.SelectModeObj.cpy_height + 1
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), self.sprite,
                QtCore.QRect(self.SelectModeObj.selectRect.left,
                             self.SelectModeObj.selectRect.top, w, h))
            qp.end()
            self.SelectModeObj.initSelectRect()

    def doPasteRect(self):
        if self.SelectModeObj.cpy_width and self.SelectModeObj.cpy_height:
            self.backupSprite()
            self.SelectModeObj.pasteRect.left = 0
            self.SelectModeObj.pasteRect.top = 0
            self.SelectModeObj.pasteRect.right = self.SelectModeObj.cpy_width
            self.SelectModeObj.pasteRect.bottom = self.SelectModeObj.cpy_height
            qp = QtGui.QPainter()
            qp.begin(self.sprite)
            w = self.SelectModeObj.cpy_width + 1
            h = self.SelectModeObj.cpy_height + 1
            qp.drawImage(QtCore.QRect(0, 0, w, h), self.sprite_cpy,
                         QtCore.QRect(0, 0, w, h))
            qp.end()

    def floodFill(self, x0, y0, iTargetColor, iNewColor):
        """
        """
        c = self.sprite.pixel(x0, y0)
        if c == iNewColor or c != iTargetColor:
            return
        self.sprite.setPixel(x0, y0, iNewColor)
        if (y0 > 0):
            self.floodFill(x0, y0 - 1, iTargetColor, iNewColor)
        if (y0 < self.nbColumnPix - 1):
            self.floodFill(x0, y0 + 1, iTargetColor, iNewColor)
        if x0 < self.nbColumnPix - 1:
            self.floodFill(x0 + 1, y0, iTargetColor, iNewColor)
        if x0 > 0:
            self.floodFill(x0 - 1, y0, iTargetColor, iNewColor)

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        # --
        self.CurEditModeObj.mousePressEvent(mouseEvent)
        self.cursorPosChanged.emit(self.x, self.y)

    def mouseReleaseEvent(self, mouseEvent):
        self.CurEditModeObj.mouseReleaseEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        self.CurEditModeObj.mouseMoveEvent(mouseEvent)
        self.cursorPosChanged.emit(self.x, self.y)

    def doMirrorHorizontal(self):
        #
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.DrawPolyLineModeObj.initDrawLine()
        self.DrawRectangleModeObj.initDrawRect()
        self.DrawEllipseModeObj.initDrawEllipse()
        self.backupSprite()
        #
        h = int(self.nbColumnPix / 2)
        w = self.nbColumnPix - 1
        for y in range(0, self.nbRowPix):
            for i in range(0, h):
                c0 = self.sprite.pixel(i, y)
                c1 = self.sprite.pixel(w - i, y)
                self.sprite.setPixel(i, y, c1)
                self.sprite.setPixel(w - i, y, c0)
        #
        self.repaint()

    def doMirrorVertical(self):
        #
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.DrawPolyLineModeObj.initDrawLine()
        self.DrawRectangleModeObj.initDrawRect()
        self.DrawEllipseModeObj.initDrawEllipse()
        self.backupSprite()
        #
        h = int(self.nbRowPix / 2)
        w = self.nbRowPix - 1
        for x in range(0, self.nbColumnPix):
            for i in range(0, h):
                c0 = self.sprite.pixel(x, i)
                c1 = self.sprite.pixel(x, w - i)
                self.sprite.setPixel(x, i, c1)
                self.sprite.setPixel(x, w - i, c0)
        #
        self.repaint()

    def doRotate90Clock(self):
        #
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.DrawPolyLineModeObj.initDrawLine()
        self.DrawRectangleModeObj.initDrawRect()
        self.DrawEllipseModeObj.initDrawEllipse()
        self.backupSprite()
        #
        for y in range(0, self.nbColumnPix):
            for x in range(0, self.nbRowPix):
                c = self.sprite_bak.pixel(x, y)
                self.sprite.setPixel(self.nbColumnPix - y - 1, x, c)

        #
        self.repaint()

    def doRotate90AntiClock(self):
        #
        self.SelectModeObj.initPasteRect()
        self.SelectModeObj.initSelectRect()
        self.DrawPolyLineModeObj.initDrawLine()
        self.DrawRectangleModeObj.initDrawRect()
        self.DrawEllipseModeObj.initDrawEllipse()
        self.backupSprite()
        #
        for y in range(0, self.nbColumnPix):
            for x in range(0, self.nbRowPix):
                c = self.sprite_bak.pixel(x, y)
                self.sprite.setPixel(y, self.nbRowPix - x - 1, c)

        #
        self.repaint()

    def setEditSprite(self, sprite):
        self.sprite = sprite
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.CurEditModeObj.keyPressEvent(e)
#             if (self.edit_mode==self.EDIT.DrawLine):
#                 #
#                 self.DrawPolyLineModeObj.keyPressEvent(e)
#                 #self.initDrawLine()
#                 #self.repaint()
#             elif (self.edit_mode==self.EDIT.DrawRectangle):
#                 #
#                 self.DrawRectangleModeObj.keyPressEvent(e)
#                 #self.initDrawRect()
#                 #self.repaint()
#             elif (self.edit_mode==self.EDIT.DrawEllipse):
#                 self.DrawEllipseModeObj.keyPressEvent(e)
#                 #self.initDrawRect()
#                 #self.repaint()
        elif e.key() == QtCore.Qt.Key_Space:
            self.setEditMode(self.prev_edit_mode)

    def paintEvent(self, e):

        qp = QtGui.QPainter()

        qp.begin(self)

        # size = self.size()
        # w = size.width()
        # h = size.height()

        self.drawGrid(qp)

        #
        self.drawSpritePixels(qp)

        # Draw Select rectangle
        if not self.SelectModeObj.selectRect.isEmpty():
            self.SelectModeObj.drawSelectRect(qp)

        if not self.SelectModeObj.pasteRect.isEmpty():
            self.SelectModeObj.drawPasteRect(qp)

        if not self.DrawRectangleModeObj.live_rect.isEmpty():
            self.DrawRectangleModeObj.drawLiveRect(qp)

        if not self.DrawEllipseModeObj.live_rect.isEmpty():
            self.DrawEllipseModeObj.drawLiveEllipse(qp)

        # if (self.nb_points>0):
        #    self.drawLivePolyLine(qp)
        self.DrawPolyLineModeObj.drawLivePolyLine(qp)

        # color = self.forewardColor
        # if (self.x>=0) and (self.y>=0):
        #    qp.setPen(color)
        #    qp.setBrush(color)
        #    mx,my = self.pixToMouseCoord(self.x,self.y)
        #    qp.drawRect(mx,my,self.pixSize,self.pixSize)

        qp.end()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = url.path()
                if path[0] == '/':
                    path = path[1:]
                if os.path.isfile(path):
                    print(path)
                    if (path.upper().endswith(".PNG")):
                        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
                        img = QtGui.QImage()
                        img.load(path, "PNG")
                        qp = QtGui.QPainter()
                        qp.begin(self.sprite)
                        wSrc = img.width()
                        hSrc = img.height()
                        if (wSrc <= 32):
                            wDes = wSrc
                        else:
                            wDes = 32
                        if (hSrc < 32):
                            hDes = hSrc
                        else:
                            hDes = 32
                        qp.drawImage(QtCore.QRect(0, 0, wDes, hDes), img,
                                     QtCore.QRect(0, 0, wSrc, hSrc))
                        qp.end()
                        self.repaint()
                        self.fileNameChanged.emit(path)
