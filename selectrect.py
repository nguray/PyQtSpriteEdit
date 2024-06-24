
from selectcorner import SelectCorner,RInt

class SelectRect:

    mode = 0
    _left = RInt(0)
    _top = RInt(0)
    _right = RInt(0)
    _bottom = RInt(0)
    TopLeft = SelectCorner()
    TopRight = SelectCorner()
    BottomLeft = SelectCorner()
    BottomRight = SelectCorner()
    _left_bak = 0
    _top_bak = 0
    _right_bak = 0
    _bottom_bak = 0

    def __init__(self) -> None:
        self.TopLeft._x = self._left
        self.TopLeft._y = self._top
        self.TopRight._x = self._right
        self.TopRight._y = self._top
        self.BottomLeft._x = self._left
        self.BottomLeft._y = self._bottom
        self.BottomRight._x = self._right
        self.BottomRight._y = self._bottom

    def setTopLeft(self,x: int,y: int):
        self.TopLeft.x = x
        self.TopLeft.y = y
    
    def getTopLeft(self) -> tuple[int, int]:
        return self.TopLeft.x,self.TopLeft.y

    def setTopRight(self,x: int,y: int):
        self.TopRight.x = x
        self.TopRight.y = y

    def getTopRight(self) -> tuple[int, int]:
        return self.TopRight.x,self.TopRight.y

    def setBottomRight(self,x: int,y: int):
        self.BottomRight.x = x
        self.BottomRight.y = y

    def getBottomRight(self) -> tuple[int, int]:
        return self.BottomRight.x,self.BottomRight.y

    def setBottomLeft(self,x: int,y: int):
        self.BottomLeft.x = x
        self.BottomLeft.y = y

    def getBottomLeft(self) -> tuple[int, int]:
        return self.BottomLeft.x,self.BottomLeft.y

    def isEmpty(self):
        return ((self._left.val == self._right.val) and (self._top.val == self._bottom.val))
    
    def empty(self):
        self._left.val = 0
        self._right.val = 0
        self._top.val = 0
        self._bottom.val = 0

    def getNormalize(self)-> tuple[int,int,int,int]:
        l = self._left.val
        t = self._top.val
        r = self._right.val
        b = self._bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        return l,t,r,b
    
    def normalize(self):
        l = self._left.val
        t = self._top.val
        r = self._right.val
        b = self._bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        self._left.val = l
        self._top.val = t
        self._right.val = r
        self._bottom.val = b

    def contains(self, x, y) -> bool:
        if (x >= self._left.val) and (x <= self._right.val) and \
            (y >= self._top.val) and (y <= self._bottom.val):
            return True
        return False
    
    def backup(self):
        self._left_bak   = self._left.val
        self._top_bak    = self._top.val
        self._right_bak  = self._right.val
        self._bottom_bak = self._bottom.val

    def restore(self):
        self._left.val   = self._left_bak
        self._top.val    = self._top_bak
        self._right.val  = self._right_bak
        self._bottom.val = self._bottom_bak

    def offset(self,dx: int,dy: int):
        self._left.val += dx
        self._right.val += dx
        self._top.val += dy
        self._bottom.val += dy

    def width(self) -> int:
        return self._right.val - self._left.val + 1
    
    def height(self) -> int:
        return self._bottom.val - self._top.val + 1

    @property
    def left(self):
        return self._left.val
    
    @left.setter
    def left(self,value):
        self._left.val = value

    @property
    def top(self):
        return self._top.val
    
    @top.setter
    def top(self,value):
        self._top.val = value

    @property
    def right(self):
        return self._right.val
    
    @right.setter
    def right(self,value):
        self._right.val = value

    @property
    def bottom(self):
        return self._bottom.val
    
    @bottom.setter
    def bottom(self,value):
        self._bottom.val = value

