
from rint import RInt
from selectcorner import SelectCorner

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
    left_bak = RInt(0)
    top_bak = RInt(0)
    right_bak = RInt(0)
    bottom_bak = RInt(0)

    def __init__(self) -> None:
        self.TopLeft.x = self._left
        self.TopLeft.y = self._top
        self.TopRight.x = self._right
        self.TopRight.y = self._top
        self.BottomLeft.x = self._left
        self.BottomLeft.y = self._bottom
        self.BottomRight.x = self._right
        self.BottomRight.y = self._bottom

    def setTopLeft(self,x: int,y: int):
        self.TopLeft.x.val = x
        self.TopLeft.y.val = y
    
    def getTopLeft(self) -> tuple[int, int]:
        return self.TopLeft.x.val,self.TopLeft.y.val

    def setTopRight(self,x: int,y: int):
        self.TopRight.x.val = x
        self.TopRight.y.val = y

    def getTopRight(self) -> tuple[int, int]:
        return self.TopRight.x.val,self.TopRight.y.val

    def setBottomRight(self,x: int,y: int):
        self.BottomRight.x.val = x
        self.BottomRight.y.val = y

    def getBottomRight(self) -> tuple[int, int]:
        return self.BottomRight.x.val,self.BottomRight.y.val

    def setBottomLeft(self,x: int,y: int):
        self.BottomLeft.x.val = x
        self.BottomLeft.y.val = y

    def getBottomLeft(self) -> tuple[int, int]:
        return self.BottomLeft.x.val,self.BottomLeft.y.val

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
        self.left_bak.val   = self._left.val
        self.top_bak.val    = self._top.val
        self.right_bak.val  = self._right.val
        self.bottom_bak.val = self._bottom.val

    def restore(self):
        self._left.val   = self.left_bak.val
        self._top.val    = self.top_bak.val
        self._right.val  = self.right_bak.val
        self._bottom.val = self.bottom_bak.val

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

