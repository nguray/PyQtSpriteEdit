
from typing import Any
from PyQt5 import QtGui, QtCore, QtWidgets

from rect import Rect

class RInt:
    val=0
    def __init__(self, nv: int) -> None:
        self.val = nv

class SelectHandle:
    x = RInt(0)
    y = RInt(0)
    def __init__(self) -> None:
        pass

class SelectRect:

    left = RInt(0)
    top = RInt(0)
    right = RInt(0)
    bottom = RInt(0)
    TopLeft = SelectHandle()
    TopRight = SelectHandle()
    BottomLeft = SelectHandle()
    BottomRight = SelectHandle()

    def __init__(self) -> None:
        self.TopLeft.x = self.left
        self.TopLeft.y = self.top
        self.TopRight.x = self.right
        self.TopRight.y = self.top
        self.BottomLeft.x = self.left
        self.BottomLeft.y = self.bottom
        self.BottomRight.x = self.right
        self.BottomRight.y = self.bottom

    def setTopLeft(self,x: int,y: int):
        self.TopLeft.x.val = x
        self.TopLeft.y.val = y
    
    def getTopLeft(self):
        return self.TopLeft.x.val,self.TopLeft.y.val

    def setTopRight(self,x: int,y: int):
        self.TopRight.x.val = x
        self.TopRight.y.val = y

    def getTopRight(self):
        return self.TopRight.x.val,self.TopRight.y.val

    def setBottomRight(self,x: int,y: int):
        self.BottomRight.x.val = x
        self.BottomRight.y.val = y

    def getBottomRight(self):
        return self.BottomRight.x.val,self.BottomRight.y.val

    def setBottomLeft(self,x: int,y: int):
        self.BottomLeft.x.val = x
        self.BottomLeft.y.val = y

    def getBottomLeft(self):
        return self.BottomLeft.x.val,self.BottomLeft.y.val

    def isEmpty(self):
        return ((self.left.val == self.right.val) and (self.top.val == self.bottom.val))
    
    def getNormalize(self):
        l = self.left.val
        t = self.top.val
        r = self.right.val
        b = self.bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        return l,t,r,b


class SelectMode:

    pasteRect = Rect(0, 0, 0, 0)
    hit_paste = False
    hit_paste_x = -1
    hit_paste_y = -1

    hit_corner = None
    hit_pix_x = -1
    hit_pix_y = -1

    hit_pt = -1

    selectRect = Rect(0, 0, 0, 0)

    cpy_width = 0
    cpy_height = 0

    select_rect = SelectRect()

    def __init__(self, outer):
        self.outer = outer
        # self.select_rect.setTopLeft(10,20)
        # x, y = self.select_rect.getBottomLeft()
        # pass


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
        """
        """
        x1,y1,x2,y2 = self.select_rect.getNormalize()
        #print("x1 : %2d, x2 : %2d" % (x1, x2))
        if x1!=x2 and y1!=y2:
            wx1, wy1 = self.outer.pixToMouseCoord(x1, y1)
            wx2, wy2 = self.outer.pixToMouseCoord(x2 + 1,y2 + 1)
            qp.fillRect(wx1,wy1,wx2-wx1,wy2-wy1,QtGui.QBrush(QtGui.QColor(0,0,255,25)))

            qp.setCompositionMode(QtGui.QPainter.CompositionMode_Xor)

            # Draw Frame
            pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(wx1, wy1, wx2, wy1)
            qp.drawLine(wx2, wy1, wx2, wy2)
            qp.drawLine(wx2, wy2, wx1, wy2)
            qp.drawLine(wx1, wy2, wx1, wy1)

            # Draw corners handle
            s = int(self.outer.pixSize / 2)
            qp.fillRect(wx1,wy1,s,s,QtGui.QBrush(QtGui.QColor(50,50,200)))            
            qp.fillRect(wx2-s,wy1,s,s,QtGui.QBrush(QtGui.QColor(50,50,200)))            
            qp.fillRect(wx2-s,wy2-s,s,s,QtGui.QBrush(QtGui.QColor(50,50,200)))    
            qp.fillRect(wx1,wy2-s,s,s,QtGui.QBrush(QtGui.QColor(50,50,200)))    

    def hitCorner(self,x,y):
        l,t,r,b = self.select_rect.getNormalize()
        if (x==l) and (y==t):
            return self.select_rect.TopLeft
        elif (x==r) and (y==t):
            return self.select_rect.TopRight
        elif (x==r) and (y==b):
            return self.select_rect.BottomRight
        elif (x==l) and (y==b):
            return self.select_rect.BottomLeft
        else:
            return None


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
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.select_rect.isEmpty():
                    self.select_rect.setTopLeft(x,y)
                    self.select_rect.setBottomRight(x,y)
                else:
                    self.hit_corner = self.hitCorner(x,y)


                # if (self.pasteRect.contains(self.x, self.y)):
                #     self.hit_paste = True
                #     self.hit_paste_x = self.x
                #     self.hit_paste_y = self.y
                # else:
                #     self.hit_paste = False
                #     self.initPasteRect()
                #     self.hit_handle = self.hitSelectRect(self.x, self.y)
                #     if self.hit_handle != -1:
                #         self.hit_pix_x = self.x
                #         self.hit_pix_y = self.y
                #     else:
                #         self.hit_pt = -1
                #         self.selectRect.left = self.x
                #         self.selectRect.top = self.y
                #         self.selectRect.right = self.x
                #         self.selectRect.bottom = self.y
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        self.hit_corner = None

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        #modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.outer.InSprite(x, y):
            if self.hit_corner is not None:
                self.hit_corner.x.val = x
                self.hit_corner.y.val = y
            else:
                self.select_rect.setBottomRight(x,y)
            self.outer.repaint()

            # if self.hit_paste:
            #     if (self.x != self.hit_paste_x) or (self.y !=
            #                                         self.hit_paste_y):
            #         dx = self.x - self.hit_paste_x
            #         dy = self.y - self.hit_paste_y
            #         self.outer.restoreSprite()
            #         self.pasteRect.left += dx
            #         self.pasteRect.top += dy
            #         self.pasteRect.right += dx
            #         self.pasteRect.bottom += dy
            #         qp = QtGui.QPainter()
            #         qp.begin(self.outer.sprite)
            #         w = self.cpy_width + 1
            #         h = self.cpy_height + 1
            #         qp.drawImage(
            #             QtCore.QRect(self.pasteRect.left, self.pasteRect.top,
            #                          w, h), self.outer.sprite_cpy,
            #             QtCore.QRect(0, 0, w, h))
            #         qp.end()
            #         self.hit_paste_x = self.x
            #         self.hit_paste_y = self.y
            #         self.outer.repaint()
            # elif self.hit_handle != -1:
            #     dx = self.x - self.hit_pix_x
            #     dy = self.y - self.hit_pix_y
            #     if (dx != 0) or (dy != 0):
            #         self.hit_pix_x = self.x
            #         self.hit_pix_y = self.y
            #         if modifiers == QtCore.Qt.ControlModifier:
            #             self.selectRect.translate(dx, dy)
            #         else:
            #             if (self.hit_handle == 0):  # Pt Haut Gauche
            #                 if (self.x < self.selectRect.right):
            #                     self.selectRect.left = self.x
            #                 if (self.y < self.selectRect.bottom):
            #                     self.selectRect.top = self.y
            #             elif (self.hit_handle == 1):  # Pt Haut Droite
            #                 if (self.x > self.selectRect.left):
            #                     self.selectRect.right = self.x
            #                 if (self.y < self.selectRect.bottom):
            #                     self.selectRect.top = self.y
            #             elif (self.hit_handle == 2):  # Pt Bas Droite
            #                 if (self.x > self.selectRect.left):
            #                     self.selectRect.right = self.x
            #                 if (self.y > self.selectRect.top):
            #                     self.selectRect.bottom = self.y
            #             elif (self.hit_handle == 3):  # Pt Bas Gauche
            #                 if (self.x < self.selectRect.right):
            #                     self.selectRect.left = self.x
            #                 if (self.y > self.selectRect.top):
            #                     self.selectRect.bottom = self.y
            #         self.outer.repaint()
            # elif (self.selectRect.right != self.x) or (self.selectRect.bottom
            #                                            != self.y):
            #     self.selectRect.right = self.x
            #     self.selectRect.bottom = self.y
            #     self.outer.repaint()

    def keyPressEvent(self, e):
        pass

