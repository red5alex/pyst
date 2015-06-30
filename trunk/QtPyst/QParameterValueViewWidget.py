__author__ = 'are'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QRect, QPoint, QPointF
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon, QLinearGradient

class QParameterValueView(QWidget):

    def __init__(self,
                 axismin=0.,
                 axismax=100.,
                 log=False,
                 parval=50.,
                 prefval=50.,
                 parlbnd=25.,
                 parubnd=75.,
                 priorstdev=None,
                 posteriorstdev=None):


        self.minAxis = axismin
        self.maxAxis = axismax
        self.log = log
        self.parval = parval
        self.prefval = prefval
        self.parlbnd = parlbnd
        self.parubnd = parubnd

        if priorstdev is None:
            self.priorStdev = (parubnd - parlbnd) / 6
        else:
            self.priorStdev = priorstdev

        if posteriorstdev is None:
            self.posteriorStdev = (parubnd - parlbnd) / 6
        else:
            self.posteriorStdev = posteriorstdev

        super().__init__()
        self.initUI()


    def initUI(self,):
        self.setMinimumSize(1, 20)  # 1 = height, 20 = 20 px

    def setAxisMin(self, value):
        self.minAxis = value

    def setAxisMax(self, value):
        self.maxAxis = value

    def setParlbnd(self, value):
        self.parlbnd = value

    def setParubnd(self, value):
        self.parubnd = value

    def setParval(self, value):
        self.parval = value

    def setPrefval(self, value):
        self.prefval = value

    def setPriorstdev(self, value):
        self.priorStdev = value

    def setPosteriorstdev(self, value):
        self.posteriorStdev = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        # color settings:
        white = QColor(255, 255, 255)

        cBackGroundNorm = white
        cBackGroundOutOfRange = QColor(255,230,230)
        cAxis = QColor(128, 128, 128)
        cPrefValueMarker = QColor(31, 78, 121)
        cPrefValueRange = QColor(95, 157, 214)
        cCurrentValueMarker = QColor(56, 87, 35)
        cPosteriorValueRange = QColor(119, 177, 80)
        cValueMarkerOutOfRange = QColor(255, 38, 0)

        # shape settings:
        size = self.size()
        w = size.width()
        h = size.height()
        pxAxis = 1
        markerHeight = 10
        markerWidth = 3
        boundfactor = 1.3

        # some pointers for better readability:
        parval = self.parval
        prefval = self.prefval
        axmin = self.minAxis
        axmax = self.maxAxis
        parlbnd = self.parlbnd
        parubnd = self.parubnd
        prior = self.priorStdev
        posterior = self.posteriorStdev

        # check if value is out of range
        if self.parval <= self.parlbnd or self.parval >= self.parubnd:
            cBackground = cBackGroundOutOfRange
        else:
            cBackground = cBackGroundNorm

        # paint background:
        rectBackground = QRect(0, 0, w-1, h-1)  # left, top, height, width
        qp.setPen(Qt.NoPen)
        qp.setBrush(cBackground)
        qp.drawRect(rectBackground)

        # paint posterior parameter range
        center = w*(parval-axmin)/(axmax-axmin)
        width = int(posterior*w/(axmax-axmin)*6)
        left = int(center - width/ 2)
        top = int(markerHeight * 0.333)+1
        height = int(markerHeight * 0.666)
        rectPosteriorRange = QRect(left, top, width, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width/2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0, cBackground),
                           (0.66, cPosteriorValueRange),
                           (1, cPosteriorValueRange)])
        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        qp.drawRect(rectPosteriorRange)

        # paint upper bound
        left = (w*(parubnd-axmin)/(axmax-axmin))
        right = (w*(parubnd-axmin)/(axmax-axmin)) + markerWidth*boundfactor
        top = h/2 - markerWidth*boundfactor - pxAxis/2
        down = h/2 - pxAxis / 2
        polyLbound = QPolygon([QPoint(left, down), QPoint(right, down), QPoint(left, top)])
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawConvexPolygon(polyLbound)

        # paint lower bound
        left = (w*(parlbnd-axmin)/(axmax-axmin))
        right = (w*(parlbnd-axmin)/(axmax-axmin))- markerWidth*boundfactor
        top = h/2 - markerWidth*boundfactor - pxAxis/2
        down = h/2 - pxAxis / 2
        polyLbound = QPolygon([QPoint(left, down), QPoint(right, down), QPoint(left, top)])
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawConvexPolygon(polyLbound)

        # paint current parameter marker
        rectCurrentParvalue = QRect(w*(parval-axmin)/(axmax-axmin)-markerWidth/2, 0, markerWidth, markerHeight)
        if self.parval <= self.parlbnd or self.parval >= self.parubnd:
            qp.setBrush(cValueMarkerOutOfRange)
            qp.setPen(cValueMarkerOutOfRange)
        else:
            qp.setBrush(cCurrentValueMarker)
            qp.setPen(cCurrentValueMarker)
        qp.drawRect(rectCurrentParvalue)

        # paint prior parameter range
        center = w*(prefval-axmin)/(axmax-axmin)
        width = int(prior*w/(axmax-axmin)*6)
        left = int(center - width/2)
        top = int(h/2)+1
        height = int(markerHeight * 0.66)
        rectPriorRange = QRect(left, top, width, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width/2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0, cBackground),
                           (0.66, cPrefValueRange),
                           (1, cPrefValueRange)])
        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        qp.drawRect(rectPriorRange)

        # paint preferred parameter marker
        rectPrefParvalue = QRect(w*(prefval-axmin)/(axmax-axmin)-markerWidth/2, h/2, markerWidth, h)
        qp.setBrush(cPrefValueMarker)
        qp.setPen(cPrefValueMarker)
        qp.drawRect(rectPrefParvalue)

        # paint parameter axis
        rectAxis = QRect(0, h/2, w-1, pxAxis)  # left, top, height, width
        qp.setBrush(cAxis)
        qp.setPen(cAxis)
        qp.drawRect(rectAxis)

        # example for fonts (used later for axis)
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

