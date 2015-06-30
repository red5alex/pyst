__author__ = 'are'

import sys
from PyQt5.QtWidgets import QWidget, QSlider, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QObject, Qt, pyqtSignal

from QtPyst.QParameterValueViewWidget import QParameterValueView

class Communicate(QObject):
    updateBW = pyqtSignal(int)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        testmin = 0
        testmax = 120

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(testmin, testmax)
        sld.setValue((testmax+testmin)/2)
        sld.setGeometry(30, 40, 300, 30)

        self.c = Communicate()
        self.wid = QParameterValueView()
        self.wid.setAxisMin(testmin)
        self.wid.setAxisMax(testmax)
        self.c.updateBW[int].connect(self.wid.setParval)
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
