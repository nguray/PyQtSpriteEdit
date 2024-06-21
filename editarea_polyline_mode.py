

from PyQt5 import QtGui, QtCore, QtWidgets

from dataclasses import dataclass

@dataclass
class _Point:
    x : int
    y : int

class PolyLineMode:

    nb_points = 0
    list_points = []
    selected_point = None
    select_rect = None


    def __init__(self, outer):
        self.outer = outer

    def resetMode(self):
        self.initDrawLine()

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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if modifiers & QtCore.Qt.ShiftModifier:
                    pass
                else:
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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
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

