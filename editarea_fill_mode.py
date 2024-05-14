

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication


class FillMode:
    def __init__(self, outer):
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                # Get Target Color
                iTargetColor = self.outer.sprite.pixel(self.x, self.y)
                iNewColor = self.outer.foregroundColor.rgba()
                self.outer.floodFill(self.x, self.y, iTargetColor, iNewColor)
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        pass

    def keyPressEvent(self, e):
        pass

