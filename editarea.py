#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

@author: nguray
'''
import os
from PyQt5 import QtGui, QtCore, QtWidgets

from editarea_pencil_mode import PencilMode
from editarea_select_mode import SelectMode
from editarea_ellipse_mode import EllipseMode
from editarea_rectangle_mode import RectangleMode
from editarea_fill_mode import FillMode
from editarea_polyline_mode import PolyLineMode


from editmode import EditMode

class MyEditArea(QtWidgets.QWidget):
    '''
    classdocs
    '''

    cursorPosChanged = QtCore.pyqtSignal(int, int)
    pipetForeColor = QtCore.pyqtSignal(QtGui.QColor)
    pipetBackColor = QtCore.pyqtSignal(QtGui.QColor)
    fileNameChanged = QtCore.pyqtSignal(str)


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QWidget.__init__(self, parent)

        self.x = -1
        self.y = -1

        self.editMode = 0
        self.prevEditMode = 0

        self.foregroundColor = QtGui.QColor(0, 0, 255, 255)
        self.backgroundColor = QtGui.QColor(0, 0, 0, 0)

        self.pixSize = 12
        self.nbRowPix = 32
        self.nbColumnPix = 32
        self.sprite = None
        self.spriteCopy = None
        self.initSprite(32,32)

        self.curEditModeObj = None

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

        selectRectModeAction = QtWidgets.QAction(QtGui.QIcon('SelectRect.png'), 'Select',
                                       self)
        selectRectModeAction.setStatusTip('Select Tool')
        pencilModeAction = QtWidgets.QAction(QtGui.QIcon('Pencil.png'), 'Pencil', self)
        pencilModeAction.setStatusTip('Pencil Tool')

        lineModeAction = QtWidgets.QAction(QtGui.QIcon('DrawLine.png'), 'Draw Line',
                                 self)
        lineModeAction.setStatusTip('Draw Line Tool')
        rectangleModeAction = QtWidgets.QAction(QtGui.QIcon('DrawRectangle.png'),
                                      'Draw Rectangle', self)
        rectangleModeAction.setStatusTip('Draw Rectangle Tool')
        ellipseModeAction = QtWidgets.QAction(QtGui.QIcon('DrawEllipse.png'),
                                    'Draw Ellipse', self)
        ellipseModeAction.setStatusTip('Draw Ellipse Tool')
        fillerModeAction = QtWidgets.QAction(QtGui.QIcon('Filler.png'), 'Fill', self)
        fillerModeAction.setStatusTip('Fill Tool')

        self.editActions = [
            selectRectModeAction, pencilModeAction,
            lineModeAction, rectangleModeAction,
            ellipseModeAction, fillerModeAction
        ]

        # -- Instancier les objects des classes

        self.DictModes = {
            EditMode.SELECT : SelectMode(self),
            EditMode.PENCIL : PencilMode(self),
            EditMode.POLYLINE : PolyLineMode(self),
            EditMode.RECTANGLE : RectangleMode(self),
            EditMode.ELLIPSE : EllipseMode(self),
            EditMode.FILL : FillMode(self)
        }

        self.curEditModeObj = self.DictModes[EditMode.SELECT]

        self.show()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAcceptDrops(True)

    def initSprite(self,w,h):
        self.pixSize = 12
        self.nbRowPix = h
        self.nbColumnPix = w
        self.sprite = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        self.sprite_bak = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)

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
        """ -- """
        self.curEditModeObj.resetMode()
        # --
        self.repaint()

    def setEditMode(self, m):
        """ -- """
        if self.editMode != m:
            self.prevEditMode = self.editMode
            self.editMode = m

            # Changer la forme du curseur de la souris
            #self.setCursor(self.editCursors[self.editMode])

            self.curEditModeObj = self.DictModes[m]
            self.curEditModeObj.resetMode()

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
        """
        """
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

    def inSprite(self, x, y):
        if ((x >= 0) and (x < self.nbColumnPix) and (y >= 0)
                and (y < self.nbRowPix)):
            return True
        else:
            return False

    def backupSprite(self):
        """ Make a backup of the sprite """
        self.sprite_bak.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite_bak)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()

    def restoreSprite(self):
        """ Restore backup sprite """
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite_bak,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()
        self.repaint()

    def doUndo(self):
        """ -- """ 
        self.restoreSprite()
        self.curEditModeObj.resetMode()

    def doCutRect(self):
        """ Manage cut select """
        if self.curEditModeObj is not self.DictModes[EditMode.SELECT]:
            return
        if not self.curEditModeObj.select_rect.isEmpty():
            w = self.curEditModeObj.select_rect.width()
            h = self.curEditModeObj.select_rect.height()
            self.spriteCopy = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)    
            self.spriteCopy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            # Faire une copie de zone
            qp.begin(self.sprite_cpy)
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), self.sprite,
                QtCore.QRect(self.curEditModeObj.select_rect.left,
                             self.curEditModeObj.select_rect.top, w, h))
            qp.end()
            # Effacer la zone
            qp1 = QtGui.QPainter()
            qp1.begin(self.sprite)
            r, g, b, a = self.backgroundColor.getRgb()
            qp1.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
            qp1.fillRect(
                QtCore.QRect(self.curEditModeObj.select_rect.left,
                             self.curEditModeObj.select_rect.top, w, h),
                QtGui.QColor(r, g, b, a))
            qp1.end()
            self.curEditModeObj.resetMode()

    def doCopyRect(self):
        """ Manage copy selected """
        if self.curEditModeObj is not self.DictModes[EditMode.SELECT]:
            return
        if not self.curEditModeObj.select_rect.isEmpty():
            w = self.curEditModeObj.select_rect.width()
            h = self.curEditModeObj.select_rect.height()
            self.spriteCopy = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
            self.spriteCopy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            qp.begin(self.spriteCopy)
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), self.sprite,
                QtCore.QRect(self.curEditModeObj.select_rect.left,
                             self.curEditModeObj.select_rect.top, w, h))
            qp.end()
            self.curEditModeObj.initSelectRect()
            self.repaint()

    def doPasteRect(self):
        """ Manage paste copy """
        if self.curEditModeObj is not self.DictModes[EditMode.SELECT]:
            return
        w = self.spriteCopy.width()
        h = self.spriteCopy.height()
        if w and h:
            self.backupSprite()
            self.curEditModeObj.select_rect.setTopLeft(0,0)
            self.curEditModeObj.select_rect.setBottomRight(w-1,h-1)
            self.curEditModeObj.select_rect.mode = 2
            qp = QtGui.QPainter()
            qp.begin(self.sprite)
            qp.drawImage(QtCore.QRect(0, 0, w, h), self.spriteCopy,
                         QtCore.QRect(0, 0, w, h))
            qp.end()
        

    def floodFill(self, x0, y0, iTargetColor, iNewColor):
        """ Do flood fill """
        c = self.sprite.pixel(x0, y0)
        if c == iNewColor or c != iTargetColor:
            return
        self.sprite.setPixel(x0, y0, iNewColor)
        if y0 > 0:
            self.floodFill(x0, y0 - 1, iTargetColor, iNewColor)
        if y0 < self.nbColumnPix - 1:
            self.floodFill(x0, y0 + 1, iTargetColor, iNewColor)
        if x0 < self.nbColumnPix - 1:
            self.floodFill(x0 + 1, y0, iTargetColor, iNewColor)
        if x0 > 0:
            self.floodFill(x0 - 1, y0, iTargetColor, iNewColor)

    def mousePressEvent(self, mouseEvent):
        """ Manage mouse button press """
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and modifiers & QtCore.Qt.ShiftModifier:
            if self.inSprite(self.x, self.y):
                c = self.sprite.pixel(self.x, self.y)
                self.foregroundColor.setRgba(c)
                self.pipetForeColor.emit(self.foregroundColor)
        else:
            # --
            self.curEditModeObj.mousePressEvent(mouseEvent)
            self.cursorPosChanged.emit(self.x, self.y)

    def mouseReleaseEvent(self, mouseEvent):
        """ Manage  mouse button release """
        self.curEditModeObj.mouseReleaseEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """ Manage mouse move """
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        self.curEditModeObj.mouseMoveEvent(mouseEvent)
        self.cursorPosChanged.emit(self.x, self.y)

    def doMirrorHorizontal(self):
        """ Do sprite horizontal mirror """
        #
        self.curEditModeObj.resetMode()
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
        """  Do sprite vertical mirror """
        #
        self.curEditModeObj.resetMode()
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
        """ Clockwise rotation """
        #
        self.curEditModeObj.resetMode()
        self.backupSprite()
        #
        for y in range(0, self.nbColumnPix):
            for x in range(0, self.nbRowPix):
                c = self.sprite_bak.pixel(x, y)
                self.sprite.setPixel(self.nbColumnPix - y - 1, x, c)

        #
        self.repaint()

    def doRotate90AntiClock(self):
        """ Anticlockwise rotation """
        #
        self.curEditModeObj.resetMode()
        self.backupSprite()
        #
        for y in range(0, self.nbColumnPix):
            for x in range(0, self.nbRowPix):
                c = self.sprite_bak.pixel(x, y)
                self.sprite.setPixel(y, self.nbRowPix - x - 1, c)

        #
        self.repaint()

    def setEditSprite(self, sprite):
        """ Define edit sprite """
        self.sprite = sprite
        self.repaint()

    def keyPressEvent(self, e):
        """ Process KeyPress """
        if e.key() == QtCore.Qt.Key_Space:
            self.setEditMode(self.prevEditMode)
        elif e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(self.myPickColorCursor)
        else:
            self.curEditModeObj.keyPressEvent(e)

    def keyReleaseEvent(self,e):
        """  Process KeyRelease"""
        if e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(QtCore.Qt.ArrowCursor)


    def paintEvent(self, e):
        """ Do paint job """

        qp = QtGui.QPainter()

        qp.begin(self)

        size = self.size()
        w = size.width()
        h = size.height()

        if w>h:
            if self.nbRowPix>self.nbColumnPix:
                self.pixSize = int(h/self.nbRowPix)
            else:
                self.pixSize = int(h/self.nbColumnPix)
        else:
            if self.nbRowPix>self.nbColumnPix:
                self.pixSize = int(w/self.nbRowPix)
            else:
                self.pixSize = int(w/self.nbColumnPix)

        self.drawGrid(qp)


        # Draw Select rectangle
        if self.curEditModeObj.select_rect is not None:
            self.curEditModeObj.drawSelectBackground(qp)

        #
        self.drawSpritePixels(qp)

        if self.curEditModeObj.select_rect is not None:
            if self.curEditModeObj.select_rect.mode==1:
                self.curEditModeObj.drawSelectHandles(qp)

        qp.end()


    def dragEnterEvent(self, e):
        """ Manage drag """
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):
        """ Manage Drop """
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = url.path()
                if path[0] == '/':
                    path = path[1:]
                if os.path.isfile(path):
                    print(path)
                    if path.upper().endswith(".PNG"):
                        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
                        img = QtGui.QImage()
                        img.load(path, "PNG")
                        qp = QtGui.QPainter()
                        qp.begin(self.sprite)
                        wSrc = img.width()
                        hSrc = img.height()
                        wDes = wSrc if wSrc < 32 else 32
                        hDes = hSrc if hSrc < 32 else 32
                        qp.drawImage(QtCore.QRect(0, 0, wDes, hDes), img,
                                     QtCore.QRect(0, 0, wSrc, hSrc))
                        qp.end()
                        self.repaint()
                        self.fileNameChanged.emit(path)
