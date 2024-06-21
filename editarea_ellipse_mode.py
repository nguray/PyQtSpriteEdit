
from PyQt5 import QtGui, QtCore, QtWidgets

from rect import Rect


class EllipseMode:

    live_rect = Rect(-1, -1, -1, -1)
    hit_handle = -1
    hit_pix_x = -1
    hit_pix_y = -1

    select_rect = None

    def __init__(self, outer):
        self.outer = outer

    def resetMode(self):
        self.initDrawEllipse()

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
            myRect = Rect(self.live_rect.left, self.live_rect.top,
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
        myRect = Rect(self.live_rect.left, self.live_rect.top,
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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
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
                    myRect = Rect(self.live_rect.left, self.live_rect.top,
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

