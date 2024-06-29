

from PyQt5 import QtGui, QtCore, QtWidgets


class FillMode:

    select_rect = None

    def __init__(self, outer):
        self.outer = outer

    def resetMode(self):
        pass

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                # Get Target Color
                iTargetColor = self.outer.sprite.pixel(x, y)
                iNewColor = self.outer.foregroundColor.rgba()
                self.outer.floodFill(x, y, iTargetColor, iNewColor)
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        pass

    def keyPressEvent(self, e):
        pass

