__author__ = 'are'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint, QPointF, QLine
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon, QLinearGradient
from math import log10, floor

class QParameterValueView(QWidget):
    def __init__(self,
                 axismin=1.,
                 axismax=99.,
                 logTransform=False,
                 parval=50.,
                 prefval=50.,
                 parlbnd=25.,
                 parubnd=75.,
                 priorstdev=None,
                 posteriorstdev=None,
                 scaleBase=0,
                 scaleInterval=1,
                 showBoundBracket=True,
                 showDevBar=True,
                 showPreCalRange=False,
                 showPostCalRange=False):

        self.BoundBracketVisible=showBoundBracket
        self.DevBarVisible=showDevBar
        self.PreCalRangeVisible=showPreCalRange
        self.PostCalRangeVisible=showPostCalRange

        self.logTransform = logTransform
        self.scaleBase = scaleBase
        self.scaleInterval = scaleInterval
        if logTransform:
            self.minAxis = log10(axismin)
            self.maxAxis = log10(axismax)
            self.parval = log10(parval)
            self.prefval = log10(prefval)
            self.parlbnd = log10(parlbnd)
            self.parubnd = log10(parubnd)
        else:
            self.minAxis = axismin
            self.maxAxis = axismax
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

    def initUI(self, ):
        self.setMinimumSize(1, 19)  # 1 = height, 19 = 19 px

    def setAxisMin(self, value):
        if self.logTransform:
            value = log10(value)
        self.minAxis = value

    def setAxisMax(self, value):
        if self.logTransform:
            value = log10(value)
        self.maxAxis = value

    def setParlbnd(self, value):
        if self.logTransform:
            value = log10(value)
        self.parlbnd = value

    def setParubnd(self, value):
        if self.logTransform:
            value = log10(value)
        self.parubnd = value

    def setParval(self, value):
        if self.logTransform:
            value = log10(value)
        self.parval = value

    def setPrefval(self, value):
        if self.logTransform:
            value = log10(value)
        self.prefval = value

    def setPriorstdev(self, value):
        if value == "from_bounds":
            value = self.parubnd - self.parlbnd
        if self.logTransform:
            value = log10(value)
        self.priorStdev = value

    def setPosteriorstdev(self, value):
        if value == "from_bounds":
            value = self.parubnd - self.parlbnd
        if self.logTransform:
            value = log10(value)
        self.posteriorStdev = value

    def setAxisbase(self, value):
        self.scaleBase = value

    def setAxisinterval(self, value):
        self.scaleInterval

    def showBoundBracket(self, show = True):
        self.BoundBracketVisible = show

    def showDevBar(self, show = True):
        self.DevBarVisible = show

    def showPreCalRange(self, show = True):
        self.PreCalRangeVisible = show

    def showPostCalRange(self, show = True):
        self.PostCalRangeVisible = show


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        # color settings:
        cWhite = QColor(255, 255, 255)
        cBlack = QColor(0, 0, 0)
        cDarkGreen = QColor(119, 177, 80)
        cOrangeYellow = QColor(255, 208, 98)
        cLightGrey = QColor(155, 155, 155)

        cBackGroundNorm = cWhite  # Normal Widget Background
        cBackGroundOutOfRange = QColor(255, 230, 230)  # Widget Background if parameter is at bound
        cAxis = QColor(215, 215, 215)  # Axis and Scale bars
        cBoundInterval = cBlack  # axis interval bewtween bounds
        cPrefValueMarker = QColor(31, 78, 121)  # preferred Value Marker
        cPrefValueRange = QColor(95, 157, 214)  # prior information range
        cCurrentValueMarker = QColor(56, 87, 35)
        cPosteriorValueRange = cOrangeYellow
        cValueMarkerOutOfRange = QColor(255, 38, 0)
        cDevInterval = QColor(255, 50, 50)

        # shape settings
        axisWidth = 1
        yDrawAreaHeight = 15
        xHorizontalMargin = 10
        yMarkerCurrentHeight = 7
        xMarkerCurrentWidth = 3
        yMarkerPrefHeight = 3
        xMarkerPrefWidth = 1
        yPriorHeight = 2
        yPosteriorHeight = 4
        yBracketHeight = 2
        yDevBarHeight = 5

        # important locations:
        actualWidgetSize = self.size()
        w = actualWidgetSize.width()
        h = actualWidgetSize.height()
        xDrawAreaWidth = w - 2 * xHorizontalMargin

        xLeft = xHorizontalMargin
        xRight = actualWidgetSize.width() - xHorizontalMargin
        xCenter = int((xLeft + xRight) / 2)
        yCenter = int(h / 2)
        yHigh = yCenter - (yDrawAreaHeight - 1) / 2
        yLow = yCenter + (yDrawAreaHeight - 1) / 2

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
        rectBackground = QRect(0, 0, w - 1, h - 1)  # left, top, height, width
        qp.setPen(cWhite)
        qp.setBrush(cBackground)
        qp.drawRect(rectBackground)

        # paint posterior parameter range
        center = xHorizontalMargin + xDrawAreaWidth * (parval - axmin) / (axmax - axmin)
        width = int(posterior * xDrawAreaWidth / (axmax - axmin) * 6)
        left = int(center - width / 2)
        top = yPosteriorHeight + 1
        height = yPosteriorHeight
        rectPosteriorRange = QRect(left, top, width, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width / 2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0, cBackground),
                           (0.66, cPosteriorValueRange),
                           (1, cPosteriorValueRange)])
        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        if self.PostCalRangeVisible:
            qp.drawRect(rectPosteriorRange)

        # draw scale
        scalebars = [self.scaleBase]
        while scalebars[0] > axmin:
            scalebars.insert(0, scalebars[0] - self.scaleInterval)
        while scalebars[-1] < axmax:
            scalebars.append(scalebars[-1] + self.scaleInterval)

        for sb in scalebars:
            sbx = xHorizontalMargin + (xDrawAreaWidth * (sb - axmin) / (axmax - axmin))
            LineSb = QLine(sbx, yCenter - 1, sbx, yCenter + 2)
            qp.setPen(cAxis)
            qp.drawLine(LineSb)

        # paint current parameter marker
        xCurrentMCenter = xHorizontalMargin + xDrawAreaWidth * (parval - axmin) / (axmax - axmin)
        left = xCurrentMCenter - (xMarkerCurrentWidth - 1) / 2
        rectCurrentParvalue = QRect(left,
                                    yCenter - yMarkerCurrentHeight,
                                    xMarkerCurrentWidth,
                                    yMarkerCurrentHeight)
        if self.parval <= self.parlbnd or self.parval >= self.parubnd:
            qp.setBrush(cValueMarkerOutOfRange)
            qp.setPen(cValueMarkerOutOfRange)
        else:
            qp.setBrush(cCurrentValueMarker)
            qp.setPen(cCurrentValueMarker)
        qp.drawRect(rectCurrentParvalue)

        # paint prior parameter range
        center = xHorizontalMargin + xDrawAreaWidth * (prefval - axmin) / (axmax - axmin)
        width = int(prior * xDrawAreaWidth / (axmax - axmin) * 6)
        left = int(center - width / 2)
        top = int(h / 2) + 1
        height = yPriorHeight

        rectPriorRange = QRect(left, yCenter + 1, width, yPriorHeight)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width / 2, top + height))
        gradient.setSpread(1)
        gradient.setStops([(0, cBackground),
                           (0.66, cPrefValueRange),
                           (1, cPrefValueRange)])
        qp.setBrush(gradient)
        qp.setPen(Qt.NoPen)
        if self.PreCalRangeVisible:
            qp.drawRect(rectPriorRange)

        # paint preferred parameter marker
        xPrefMCenter = xHorizontalMargin + xDrawAreaWidth * (prefval - axmin) / (axmax - axmin)
        left = xPrefMCenter - (xMarkerPrefWidth - 1) / 2
        rectPrefParvalue = QRect(left,
                                 yCenter + 1,
                                 xMarkerPrefWidth,
                                 yMarkerPrefHeight)
        qp.setBrush(cPrefValueMarker)
        qp.setPen(cPrefValueMarker)
        qp.drawRect(rectPrefParvalue)

        # draw parameter axis
        lineAxis = QLine(xLeft, yCenter, xRight, yCenter)
        # qp.setPen(Qt.DotLine)
        qp.setPen(cAxis)
        qp.drawLine(lineAxis)

        # draw bound bracket
        xUbound = xHorizontalMargin + (xDrawAreaWidth * (parubnd - axmin) / (axmax - axmin))
        xLbound = xHorizontalMargin + (xDrawAreaWidth * (parlbnd - axmin) / (axmax - axmin))
        LineUbound = QLine(xUbound, yCenter - yBracketHeight, xUbound, yCenter)
        LineLbound = QLine(xLbound, yCenter, xLbound, yCenter - yBracketHeight)
        LineBoundInterval = QLine(xLbound, yCenter, xUbound, yCenter)
        qp.setPen(cBoundInterval)
        if self.BoundBracketVisible:
            qp.drawLine(LineUbound)
            qp.drawLine(LineBoundInterval)
            qp.drawLine(LineLbound)

        # draw deviation bracket
        """
        LineCbound = QLine(xCurrentMCenter, yCenter - yBracketHeight, xCurrentMCenter, yCenter)
        LinePbound = QLine(xPrefMCenter, yCenter, xPrefMCenter, yCenter + yBracketHeight)
        LineDevInterval = QLine(xCurrentMCenter, yCenter, xPrefMCenter, yCenter)
        qp.setPen(cDevInterval)
        qp.drawLine(LineCbound)
        qp.drawLine(LinePbound)
        qp.drawLine(LineDevInterval)
        """

        # draw deviation bar
        center = xHorizontalMargin + xDrawAreaWidth * (prefval - axmin) / (axmax - axmin)
        width = xUbound - xLbound
        left = xLbound
        top = yCenter - yDevBarHeight / 2
        height = yDevBarHeight

        rect1stdev = QRect(center, top, xCurrentMCenter - xPrefMCenter, height)
        gradient = QLinearGradient(QPointF(left, top), QPointF(left + width / 2, top + height))

        gradient.setSpread(1)
        gradient.setStops([(1.00, cDarkGreen),
                           (0.67, cDarkGreen),
                           (0.65, cOrangeYellow),
                           (0.34, cOrangeYellow),
                           (0.32, cValueMarkerOutOfRange),
                           (0.00, cValueMarkerOutOfRange)])
        qp.setPen(Qt.NoPen)
        qp.setBrush(gradient)
        if self.DevBarVisible:
            qp.drawRect(rect1stdev)


class QParameterValueViewScale(QParameterValueView):
    def drawWidget(self, qp):

        # color settings:
        cWhite = QColor(255, 255, 255)
        cBlack = QColor(0, 0, 0)

        cBackGroundNorm = cWhite
        cBackGroundOutOfRange = QColor(255, 230, 230)
        cAxis = QColor(155, 155, 155)
        cBoundInterval = cBlack
        cPrefValueMarker = QColor(31, 78, 121)
        cPrefValueRange = QColor(95, 157, 214)
        cCurrentValueMarker = QColor(56, 87, 35)
        cPosteriorValueRange = QColor(119, 177, 80)
        cValueMarkerOutOfRange = QColor(255, 38, 0)


        # shape settings
        axisWidth = 1
        yDrawAreaHeight = 15
        xHorizontalMargin = 10
        yMarkerCurrentHeight = 7
        xMarkerCurrentWidth = 3
        yMarkerPrefHeight = 4
        xMarkerPrefWidth = 3
        yPriorHeight = 3
        yPosteriorHeight = 4

        # important locations:
        actualWidgetSize = self.size()
        w = actualWidgetSize.width()
        h = actualWidgetSize.height()
        xDrawAreaWidth = w - 2 * xHorizontalMargin

        xLeft = xHorizontalMargin
        xRight = actualWidgetSize.width() - xHorizontalMargin
        xCenter = int((xLeft + xRight) / 2)
        yCenter = int(h / 2)
        yHigh = yCenter - (yDrawAreaHeight - 1) / 2
        yLow = yCenter + (yDrawAreaHeight - 1) / 2

        # some pointers for better readability:
        parval = self.parval
        prefval = self.prefval
        axmin = self.minAxis
        axmax = self.maxAxis
        parlbnd = self.parlbnd
        parubnd = self.parubnd
        prior = self.priorStdev
        posterior = self.posteriorStdev

        # paint background:
        rectBackground = QRect(0, 0, w - 1, h - 1)  # left, top, height, width
        qp.setPen(Qt.NoPen)
        qp.setBrush(cBackGroundNorm)
        qp.drawRect(rectBackground)

        # draw scale
        scalebars = [self.scaleBase]
        while scalebars[0] > axmin:
            scalebars.insert(0, scalebars[0] - self.scaleInterval)
        while scalebars[-1] < axmax:
            scalebars.append(scalebars[-1] + self.scaleInterval)

        for sb in scalebars:
            scaletext = str(sb) + " m/d"
            if self.logTransform:
                scaletext = "10^" + scaletext

            sbx = xHorizontalMargin + (xDrawAreaWidth * (sb - axmin) / (axmax - axmin))
            # LineSb = QLine(sbx, yCenter - 1, sbx, yCenter + 2)
            qp.setPen(cBlack)
            #            qp.drawLine(LineSb)
            font = QFont('Serif', 7, QFont.Light)
            qp.setFont(font)
            metrics = qp.fontMetrics()
            fw = metrics.width(scaletext)
            fh = metrics.height()
            qp.drawText(sbx - fw / 2, yCenter + fh / 2, scaletext)