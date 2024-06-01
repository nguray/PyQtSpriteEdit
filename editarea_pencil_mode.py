
from PyQt5 import QtGui, QtCore, QtWidgets


class PencilMode:
    def __init__(self, outer):
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.foregroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()


    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QtGui.QApplication.keyboardModifiers()
        if self.outer.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.foregroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(self.x, self.y,
                                           self.outer.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()

    def keyPressEvent(self, keyEvent):
        pass

