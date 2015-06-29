__author__ = 'are'

import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication,
    QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QRect, QPoint, QPointF
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon, QLinearGradient


class Communicate(QObject):

    updateBW = pyqtSignal(int)


class PriorInfoView(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self, axismin=0, axismax=100, current=50, preferred=50, lbound=25, hbound=75, log=False):

        self.setMinimumSize(1, 20)  # 1 = height, 20 = 20 px

        self.minAxis = axismin
        self.maxAxis = axismax

        self.log = log

        self.valueCurrent = current
        self.valuePreferred = preferred
        self.valueLbound = lbound
        self.valueUbound = hbound

        self.priorStdev = (hbound - lbound) / 6
        self.posteriorStdev = (hbound - lbound) / 6

        # self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setMinAxis(self, value):
        self.minAxis = value

    def setMaxAxis(self, value):
        self.maxAxis = value

    def setValueLbound(self, value):
        self.valueLbound = value

    def setValueUbound(self, value):
        self.valueUbound = value

    def setValueCurrent(self, value):
        self.valueCurrent = value

    def setValuePreferred(self, value):
        self.valuePreferred = value

    def setValuePriorStdev(self, value):
        self.priorStdev = value

    def setValuePosteriorStdev(self, value):
        self.posteriorStdev = value

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()


    def drawWidget(self, qp):

        # position of current parameter value
        posc = self.valueCurrent
        posp = self.valuePreferred
        posmin = self.minAxis
        posmax = self.maxAxis
        poslb = self.valueLbound
        posub = self.valueUbound

        prior = self.priorStdev
        posterior = self.posteriorStdev

        size = self.size()
        w = size.width()
        h = size.height()

        # color settings:
        white = QColor(255, 255, 255)

        cBackGround = white
        cAxis = QColor(128, 128, 128)
        cPrefValueMarker = QColor(31, 78, 121)
        cPrefValueRange = QColor(95, 157, 214)
        cCurrentValueMarker = QColor(56, 87, 35)
        cPosteriorValueRange = QColor(119, 177, 80)
        cValueMarkerOutOfRange = QColor(255, 38, 0)

        # shape settings:
        pxAxis = 1
        markerHeight = 10
        markerWidth = 3
        boundfactor = 1.3

        # paint background:
        rBackground = QRect(0, 0, w-1, h-1)
        qp.setBrush(cBackGround)
        qp.setPen(cBackGround)
        qp.drawRect(rBackground)

        # paint posterior parameter range
        center = w*(posc-posmin)/(posmax-posmin)
        width = int(posterior*w/(posmax-posmin)*6)
        left = int(center - width/ 2)
        top = int(markerHeight * 0.333)
        height = int(markerHeight * 0.666)
        rPosteriorRange = QRect(left, top, width, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width/2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0, cBackGround),
                           (0.66, cPosteriorValueRange),
                           (1, cPosteriorValueRange)])

        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        qp.drawRect(rPosteriorRange)

        # paint upper bound
        left = (w*(posub-posmin)/(posmax-posmin))
        right = (w*(posub-posmin)/(posmax-posmin)) + markerWidth*boundfactor
        top = h/2 - markerWidth*boundfactor - pxAxis/2
        down = h/2 - pxAxis / 2
        pLbound = QPolygon([QPoint(left, down), QPoint(right, down), QPoint(left, top)])
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawConvexPolygon(pLbound)

        # paint lower bound
        left = (w*(poslb-posmin)/(posmax-posmin))
        right = (w*(poslb-posmin)/(posmax-posmin))- markerWidth*boundfactor
        top = h/2 - markerWidth*boundfactor - pxAxis/2
        down = h/2 - pxAxis / 2
        pLbound = QPolygon([QPoint(left, down), QPoint(right, down), QPoint(left, top)])
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawConvexPolygon(pLbound)

        # paint current parameter marker
        rCurrentParvalue = QRect(w*(posc-posmin)/(posmax-posmin)-markerWidth/2, 0, markerWidth, markerHeight)  # left, top, height, width
        if self.valueCurrent <= self.valueLbound or self.valueCurrent >= self.valueUbound:
            qp.setBrush(cValueMarkerOutOfRange)
            qp.setPen(cValueMarkerOutOfRange)
        else:
            qp.setBrush(cCurrentValueMarker)
            qp.setPen(cCurrentValueMarker)
        qp.drawRect(rCurrentParvalue)

        # paint prior parameter range
        center = w*(posp-posmin)/(posmax-posmin)
        width = int(prior*w/(posmax-posmin)*6)
        left = int(center - width/ 2)
        top = int(h/2)
        height = int(markerHeight * 0.66)
        rPriorRange = QRect(left, top, width, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width/2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0,cBackGround),
                           (0.66, cPrefValueRange),
                           (1,cPrefValueRange)])

        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        qp.drawRect(rPriorRange)

        # paint preferred parameter marker
        rPrefParvalue = QRect(w*(posp-posmin)/(posmax-posmin)-markerWidth/2, h/2, markerWidth, h)
        qp.setBrush(cPrefValueMarker)
        qp.setPen(cPrefValueMarker)
        qp.drawRect(rPrefParvalue)

        # paint parameter axis
        rAxis = QRect(0, h/2, w-1, pxAxis) # left, top, height, width
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawRect(rAxis)

        """

        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)




        step = int(round(w / 10.0))


        till = int(((w / 750.0) * self.value))
        full = int(((w / 750.0) * 700))

        if self.value >= 700:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)

        else:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)


        pen = QPen(QColor(20, 20, 20), 1,
            Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        j = 0

        for i in range(step, 10*step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j]))
            j = j + 1

        """


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        testmin = 20
        testmax = 120

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(testmin, testmax)
        sld.setValue((testmax+testmin)/2)
        sld.setGeometry(30, 40, 300, 30)

        self.c = Communicate()
        self.wid = PriorInfoView()
        self.wid.setMinAxis(testmin)
        self.wid.setMaxAxis(testmax)
        self.c.updateBW[int].connect(self.wid.setValueCurrent)

        sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('Parameter value widget')
        self.show()


    def changeValue(self, value):

        self.c.updateBW.emit(value)
        self.wid.repaint()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())