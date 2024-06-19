
from typing import Any
from PyQt5 import QtGui, QtCore, QtWidgets

from rect import Rect
from selectcorner import SelectCorner
from selectrect import SelectRect



class SelectMode:

    hit_corner = None
    cpy_width = 0
    cpy_height = 0

    select_rect = SelectRect()
    start_x = 0
    start_y = 0
    f_move = False

    def __init__(self, outer):
        self.outer = outer
        # self.select_rect.setTopLeft(10,20)
        # x, y = self.select_rect.getBottomLeft()
        # pass

    def initSelectRect(self):
        self.hit_corner = None
        self.start_x = 0
        self.start_y = 0
        self.select_rect.empty()
        self.select_rect.mode = 0
        self.f_move = False
        self.hit_pix_x = -1
        self.hit_pix_y = -1

    def drawSelectRect(self, qp):
        """
        """
        x1,y1,x2,y2 = self.select_rect.getNormalize()
        #print("x1 : %2d, x2 : %2d" % (x1, x2))
        if x1!=x2 and y1!=y2:
            wx1, wy1 = self.outer.pixToMouseCoord(x1, y1)
            wx2, wy2 = self.outer.pixToMouseCoord(x2 + 1,y2 + 1)
            qp.fillRect(wx1,wy1,wx2-wx1,wy2-wy1,QtGui.QBrush(QtGui.QColor(0,0,255,25)))

            # qp.setCompositionMode(QtGui.QPainter.CompositionMode_Xor)
            # Draw Frame
            # pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 1, QtCore.Qt.SolidLine)
            # qp.setPen(pen)
            # qp.drawLine(wx1, wy1, wx2, wy1)
            # qp.drawLine(wx2, wy1, wx2, wy2)
            # qp.drawLine(wx2, wy2, wx1, wy2)
            # qp.drawLine(wx1, wy2, wx1, wy1)

            # Draw corners handle
            s = int(self.outer.pixSize*0.7)
            qp.fillRect(wx1,wy1,s,s,QtGui.QBrush(QtGui.QColor(0,0,200,128)))            
            qp.fillRect(wx2-s,wy1,s,s,QtGui.QBrush(QtGui.QColor(0,0,200,128)))            
            qp.fillRect(wx2-s,wy2-s,s,s,QtGui.QBrush(QtGui.QColor(0,0,200,128)))    
            qp.fillRect(wx1,wy2-s,s,s,QtGui.QBrush(QtGui.QColor(0,0,200,128)))    

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

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()

        if self.outer.InSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                match self.select_rect.mode:
                    case 0:
                        self.select_rect.setTopLeft(x,y)
                        self.select_rect.setBottomRight(x,y)
                    case 1:
                        self.hit_corner = self.hitCorner(x,y)
                        if self.hit_corner is None:
                            if self.select_rect.contains(x,y):
                                self.select_rect.backup()
                                self.start_x = x
                                self.start_y = y
                                self.f_move = True
                            else:
                                self.select_rect.setTopLeft(x,y)
                                self.select_rect.setBottomRight(x,y)
                                self.select_rect.mode = 0
                        self.outer.repaint()
                    case _:
                        if self.select_rect.contains(x,y):
                            self.select_rect.backup()
                            self.start_x = x
                            self.start_y = y
                            self.f_move = True
                        else:
                            self.initSelectRect()
                            self.select_rect.setTopLeft(x,y)
                            self.select_rect.setBottomRight(x,y)
                            self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        match self.select_rect.mode:
            case 0:
                if not self.select_rect.isEmpty():
                    self.select_rect.normalize()
                    self.select_rect.mode = 1
            case 1:
                self.hit_corner = None
                self.f_move = False
            case _:
                self.hit_corner = None
                self.f_move = False

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        #modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.outer.InSprite(x, y):

            match self.select_rect.mode:
                case 0:
                    self.select_rect.setBottomRight(x,y)
                    self.outer.repaint()
                case 1:
                    if self.f_move:
                        dx = x - self.start_x
                        dy = y - self.start_y
                        if dx!=0 or dy!=0:
                            self.select_rect.restore()
                            self.select_rect.offset(dx,dy)
                    elif self.hit_corner is not None:
                        sav_x = self.hit_corner.x.val
                        sav_y = self.hit_corner.y.val 
                        self.hit_corner.x.val = x
                        self.hit_corner.y.val = y
                        if self.select_rect.width() < 2 :
                            self.hit_corner.x.val = sav_x
                        if self.select_rect.height() < 2 :
                            self.hit_corner.y.val = sav_y
                    self.outer.repaint()
                case _:
                    if self.f_move:
                        dx = x - self.start_x
                        dy = y - self.start_y
                        if dx!=0 or dy!=0:
                            self.select_rect.restore()
                            self.select_rect.offset(dx,dy)
                            self.outer.restoreSprite()
                            qp = QtGui.QPainter()
                            qp.begin(self.outer.sprite)
                            w = self.cpy_width
                            h = self.cpy_height
                            qp.drawImage(
                                QtCore.QRect(self.select_rect.left.val, 
                                             self.select_rect.top.val,
                                            w, h), self.outer.sprite_cpy,
                                QtCore.QRect(0, 0, w, h))
                            qp.end()
                            self.outer.repaint()

    def keyPressEvent(self, e):
        pass

