
from dataclasses import dataclass

@dataclass
class Rect:

    left : int
    top : int
    right : int
    bottom : int

    def normalize(self):
        if (self.left > self.right):
            d = self.left
            self.left = self.right
            self.right = d

        if (self.top > self.bottom):
            d = self.top
            self.top = self.bottom
            self.bottom = d

    def empty(self):
        self.left = -1
        self.top = -1
        self.right = -1
        self.bottom = -1

    def isEmpty(self):
        return ((self.left == self.right) and (self.top == self.bottom))

    def isValid(self):
        return (self.left < self.right) and (self.top < self.bottom)

    def width(self):
        if (self.right > self.left):
            return self.right - self.left
        else:
            return self.left - self.right

    def height(self):
        if (self.bottom > self.top):
            return self.bottom - self.top
        else:
            return self.top - self.bottom

    def contains(self, x, y):
        if (x >= self.left) and (x <= self.right) and (y >= self.top) and (
                y <= self.bottom):
            return True
        return False

    def translate(self, dx, dy):
        self.left += dx
        self.right += dx
        self.top += dy
        self.bottom += dy

