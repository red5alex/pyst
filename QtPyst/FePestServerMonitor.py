__author__ = 'are'

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.uic import loadUi

# Script Implementation


def onSelectFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])

    Dialog.plainTextEdit.clear()
    Dialog.plainTextEdit.appendPlainText("test")



# User Interface
app = QApplication(sys.argv)
Dialog = loadUi('FePestServerMonitor.ui')

Dialog.toolButtonSelectInputFile.clicked.connect(onSelectFile)

Dialog.show()
sys.exit(app.exec_())


