__author__ = 'are'

import os
import sys
import pyst
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QProgressBar
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.uic import loadUi

from pyst.utils import pest as pu
from pysttools.MAT2DAT.mat2dat import mat2dat


# user interface calls

jcofilepath = ""
matfilepath = ""
datfilepath = ""

def onSelectJCOFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditJCOFilePath.setText(path[0])


def JCOpathChanged():
    exist = os.path.isfile(Dialog.lineEditJCOFilePath.text())
    Dialog.pushButtonRunJCO2MAT.setEnabled(exist)


def onSelectMATFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditMATFilePath.setText(path[0])


def MATpathChanged():
    exist = os.path.isfile(Dialog.lineEditMATFilePath.text())
    Dialog.pushButtonRunMAT2JCO.setEnabled(exist)
    Dialog.pushButtonRunMAT2DAT.setEnabled(exist)


def onSelectDATFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditDATFilePath.setText(path[0])


def DATpathChanged():
    exist = os.path.isfile(Dialog.lineEditDATFilePath.text())
    Dialog.pushButtonRunDAT2MAT.setEnabled(exist)


def onRunJCO2MAT():
    jcofilepath= Dialog.lineEditJCOFilePath.text()
    matfilepath = jcofilepath.replace(".jco", ".mat")
    targetExist = os.path.isfile(matfilepath)
    pu.jco2mat(jcofilepath, matfilepath)
    Dialog.lineEditMATFilePath.setText(matfilepath)


def onRunMAT2JCO():
    matfilepath = Dialog.lineEditMATFilePath.text()
    jcofilepath= matfilepath.replace(".mat", ".jco")
    pu.mat2jco(matfilepath, jcofilepath)
    Dialog.lineEditJCOFilePath.setText(jcofilepath)


def onRunMAT2DAT():
    matfilepath = Dialog.lineEditMATFilePath.text()
    datfilepath = matfilepath.replace(".mat", ".dat")
    mat2dat(matfilepath, datfilepath, verbose=True)
    Dialog.lineEditDATFilePath.setText(datfilepath)

def onRunDAT2MAT():
    matfilepath = Dialog.lineEditJCOFilePath.text()
    datfilepath = Dialog.lineEditJCOFilePath.text()
    print("Dat2Mat not implemented")


# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('MatrixManipulation.ui')

Dialog.toolButtonSelectJCOFile.clicked.connect(onSelectJCOFile)
Dialog.toolButtonSelectMATFile.clicked.connect(onSelectMATFile)
Dialog.toolButtonSelectDATFile.clicked.connect(onSelectDATFile)

Dialog.pushButtonRunJCO2MAT.clicked.connect(onRunJCO2MAT)
Dialog.pushButtonRunMAT2JCO.clicked.connect(onRunMAT2JCO)
Dialog.pushButtonRunMAT2DAT.clicked.connect(onRunMAT2DAT)
Dialog.pushButtonRunDAT2MAT.clicked.connect(onRunDAT2MAT)

Dialog.lineEditJCOFilePath.textChanged.connect(JCOpathChanged)
Dialog.lineEditMATFilePath.textChanged.connect(MATpathChanged)
Dialog.lineEditDATFilePath.textChanged.connect(DATpathChanged)

# Activate the user interface:
Dialog.show()
sys.exit(app.exec_())