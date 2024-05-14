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

from editarea_pencil_mode import PencilMode
from editarea_select_mode import SelectMode
from editarea_ellipse_mode import EllipseMode
from editarea_rectangle_mode import RectangleMode
from editarea_fill_mode import FillMode
from editarea_polyline_mode import PolyLineMode

from rect import Rect

class MyEditArea(QWidget):
    '''
    classdocs
    '''

    cursorPosChanged = QtCore.pyqtSignal(int, int)
    pipetForeColor = QtCore.pyqtSignal(QtGui.QColor)
    pipetBackColor = QtCore.pyqtSignal(QtGui.QColor)
    fileNameChanged = QtCore.pyqtSignal(str)

    EditeModes = namedtuple('EditModes', [
        'Select', 'Pencil', 'Rubber', 'DrawLine', 'DrawRectangle',
        'DrawEllipse', 'Fill'
    ])
    EDIT = EditeModes(0, 1, 2, 3, 4, 5, 6)

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

        self.myPickColorCursor = QtGui.QCursor(QtGui.QPixmap(":res/PickColor.png"),6,23)
        # ----------------------------------------------------------------------
        myCursorSelect = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorSelect.png", "PNG"), 0, 0)
        myCursorPencil = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorPencil.png", "PNG"), 12, 19)
        myCursorRubber = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRubber1.png", "PNG"), 12, 19)
        myCursorLine = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorLine.png", "PNG"), 12, 19)
        myCursorRectangle = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRectangle.png", "PNG"), 12, 19)
        myCursorEllipse = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorEllipse.png", "PNG"), 12, 19)
        myCursorFill = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorFill.png", "PNG"), 7, 21)
        self.editCursors = [
            myCursorSelect, myCursorPencil, myCursorRubber,
            myCursorLine, myCursorRectangle, myCursorEllipse, myCursorFill
        ]

        self.init32Sprite()

        selectRectModeAction = QAction(QtGui.QIcon('SelectRect.png'), 'Select',
                                       self)
        selectRectModeAction.setStatusTip('Select Tool')
        pencilModeAction = QAction(QtGui.QIcon('Pencil.png'), 'Pencil', self)
        pencilModeAction.setStatusTip('Pencil Tool')

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
            lineModeAction, rectangleModeAction,
            ellipseModeAction, fillerModeAction
        ]

        # -- Instancier les objects des classes
        self.DrawPolyLineModeObj = PolyLineMode(self)
        self.PencilModeObj = PencilMode(self)
        self.SelectModeObj = SelectMode(self)
        self.DrawRectangleModeObj = RectangleMode(self)
        self.DrawEllipseModeObj = EllipseMode(self)
        self.FillModeObj = FillMode(self)
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
        modifiers = QApplication.keyboardModifiers()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and modifiers & QtCore.Qt.ShiftModifier:
            if self.InSprite(self.x, self.y):
                c = self.sprite.pixel(self.x, self.y)
                self.foregroundColor.setRgba(c)
                self.pipetForeColor.emit(self.foregroundColor)
        else:
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
        if e.key() == QtCore.Qt.Key_Space:
            self.setEditMode(self.prev_edit_mode)
        elif e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(self.myPickColorCursor)
        else:
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

    def keyReleaseEvent(self,e):
        if e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(QtCore.Qt.ArrowCursor)


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
