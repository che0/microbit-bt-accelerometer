from PyQt5 import QtCore, QtWidgets, QtGui


class Canvas(QtWidgets.QGraphicsScene):
    def paint(self):
        rect = QtCore.QRectF(0, 0, 100, 100)
        color = QtGui.QColor(255, 0, 0)
        self.addRect(rect, brush=QtGui.QBrush(color))


def main():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()

    canvas = Canvas()
    view = QtWidgets.QGraphicsView(canvas)
    window.setCentralWidget(view)
    window.showFullScreen()

    canvas.paint()

    return app.exec()

if __name__ == '__main__':
    main()
