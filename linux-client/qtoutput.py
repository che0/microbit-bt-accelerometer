#!/usr/bin/env python3
from PyQt5 import QtCore, QtWidgets, QtGui
import btsensor
import os


class Canvas(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.text = None

    def paint(self):
        rect = QtCore.QRectF(0, 0, 100, 100)
        color = QtGui.QColor(255, 0, 0)
        self.addRect(rect, brush=QtGui.QBrush(color))

    def write(self, text):
        if self.text is None:
            self.text = self.addText(text)
        else:
            self.text.setPlainText(text)


class ForwardingAccelerometer(btsensor.MicrobitAccelerometer):
    def setCanvas(self, canvas):
        self.__canvas = canvas

    def processData(self, x, y, z):
        self.__canvas.write(f'{x}, {y}, {z}')

    def checkNotifications(self):
        self.waitForNotifications(10)


def main():
    mac = os.getenv('MICROBIT_MAC')
    if not mac:
        raise RuntimeError('need MICROBIT_MAC')

    accelerometer = ForwardingAccelerometer(mac)

    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()

    canvas = Canvas()
    accelerometer.setCanvas(canvas)
    accelerometer.setNotifications()

    timer = QtCore.QTimer()
    timer.timeout.connect(accelerometer.checkNotifications)

    view = QtWidgets.QGraphicsView(canvas)
    window.setCentralWidget(view)
    window.showFullScreen()

    canvas.paint()
    timer.start(100)

    return app.exec()

if __name__ == '__main__':
    main()
