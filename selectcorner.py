

class RInt:
    def __init__(self, nv: int) -> None:
        self.val = nv

class SelectCorner:
    
    def __init__(self) -> None:
        self._x = RInt(0)
        self._y = RInt(0)
    
    @property
    def x(self):
        return self._x.val
    
    @x.setter
    def x(self,value):
        self._x.val = value

    @property
    def y(self):
        return self._y.val
    
    @y.setter
    def y(self,value):
        self._y.val = value

    