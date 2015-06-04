__author__ = 'are'

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.uic import loadUi

# Script Implementation

def test():
    print("push Button")
    filePath = Dialog.lineEditInputFilePath.text()
    print(filePath)

def selectFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])

# User Interface
app = QApplication(sys.argv)
Dialog = loadUi('test.ui')

Dialog.pushButtonRun.clicked.connect(test)
Dialog.toolButtonSelectInputFile.clicked.connect(selectFile)

Dialog.show()
sys.exit(app.exec_())


