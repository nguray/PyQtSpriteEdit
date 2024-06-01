
from PyQt5 import QtGui, QtCore, QtWidgets

from rect import Rect

class SelectMode:

    pasteRect = Rect(0, 0, 0, 0)
    hit_paste = False
    hit_paste_x = -1
    hit_paste_y = -1

    hit_handle = -1
    hit_pix_x = -1
    hit_pix_y = -1

    hit_pt = -1

    selectRect = Rect(0, 0, 0, 0)

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
        normRect = Rect(self.selectRect.left, self.selectRect.top,
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
            myRect = Rect(self.selectRect.left, self.selectRect.top,
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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
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

