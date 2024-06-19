
from rint import RInt
from selectcorner import SelectCorner

class SelectRect:

    mode = 0
    left = RInt(0)
    top = RInt(0)
    right = RInt(0)
    bottom = RInt(0)
    TopLeft = SelectCorner()
    TopRight = SelectCorner()
    BottomLeft = SelectCorner()
    BottomRight = SelectCorner()
    left_bak = RInt(0)
    top_bak = RInt(0)
    right_bak = RInt(0)
    bottom_bak = RInt(0)

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
    
    def empty(self):
        self.left.val = 0
        self.right.val = 0
        self.top.val = 0
        self.bottom.val = 0

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
    
    def normalize(self):
        l = self.left.val
        t = self.top.val
        r = self.right.val
        b = self.bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        self.left.val = l
        self.top.val = t
        self.right.val = r
        self.bottom.val = b

    def contains(self, x, y):
        if (x >= self.left.val) and (x <= self.right.val) and \
            (y >= self.top.val) and (y <= self.bottom.val):
            return True
        return False
    
    def backup(self):
        self.left_bak.val   = self.left.val
        self.top_bak.val    = self.top.val
        self.right_bak.val  = self.right.val
        self.bottom_bak.val = self.bottom.val

    def restore(self):
        self.left.val   = self.left_bak.val
        self.top.val    = self.top_bak.val
        self.right.val  = self.right_bak.val
        self.bottom.val = self.bottom_bak.val

    def offset(self,dx: int,dy: int):
        self.left.val += dx
        self.right.val += dx
        self.top.val += dy
        self.bottom.val += dy

    def width(self) -> int:
        return self.right.val - self.left.val + 1
    
    def height(self) -> int:
        return self.bottom.val - self.top.val + 1
    
    

