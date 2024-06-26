
from PyQt5 import QtGui, QtCore, QtWidgets


class PencilMode:

    select_rect = None

    def __init__(self, outer):
        self.outer = outer
        self.prev_x = 0
        self.prev_y = 0

    def resetMode(self):
        pass

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.outer.inSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(x, y, self.outer.foregroundColor.rgba())
                self.prev_x = x
                self.prev_y = y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(x, y, self.outer.backgroundColor.rgba())
                self.prev_x = x
                self.prev_y = y
                self.outer.repaint()


    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.outer.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QtGui.QApplication.keyboardModifiers()
        if self.outer.inSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.outer.sprite.setPixel(x, y,
                                           self.outer.foregroundColor.rgba())
                self.prev_x = x
                self.prev_y = y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.outer.backupSprite()
                self.outer.sprite.setPixel(x, y,
                                           self.outer.backgroundColor.rgba())
                self.prev_x = x
                self.prev_y = y
                self.outer.repaint()

    def keyPressEvent(self, keyEvent):
        pass

