__author__ = 'are'

import pyst
import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

pstfile = None
senfile = None

def onRefresh():
    updateData()

def onSelectFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])

def onSelectFile_2():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath_2.setText(path[0])

def updateData():

    # POPULATE PREFERRED VALUES TREE

    view = Dialog.treeWidgetSlaves
    view.clear()

    # Load the SEN file
    path = Dialog.lineEditInputFilePath.text()
    senfile = pyst.SenFile(path)

    pstpath = Dialog.lineEditInputFilePath_2.text()
    pstfile = pyst.PestCtrlFile(pstpath)

    iterations = senfile.getnumberofiterations()
    Dialog.lcdNumberTotalRuns.display(iterations)

    treeElements = {}

    for group in senfile.groups:
        newGroup= QTreeWidgetItem(0)
        newGroup.setText(0, group)
        treeElements[group] = newGroup
        view.addTopLevelItem(newGroup)
        newGroup.setExpanded(True)

    h = {
        'name':     0,
        'val':      1,
        'sens':     2,
        'lower':    3,
        'pref':     4,
        'upper':    5,
        }



    for p in senfile.getparamaternames():
        newPar = QTreeWidgetItem(0)
        newPar.setText(h['name'], p)
        newPar.setText(h['val'], str(senfile.parhistory[iterations][p]))
        newPar.setText(h['sens'], str(senfile.senhistory[iterations][p]))
        newPar.setText(h['lower'], str(pstfile.params[p].PARLBND))
        newPar.setText(h['pref'], str(pstfile.params[p].PARVAL1))
        newPar.setText(h['upper'], str(pstfile.params[p].PARUBND))

        treeElements[senfile.membership[p]].addChild(newPar)


    # POPULATE SEN FILE WINDOW

    Dialog.plainTextEdit.clear()

    senfileraw = open(path)
    lines = senfileraw.readlines()
    for l in lines:
        Dialog.plainTextEdit.appendPlainText(l.replace("\n",""))
    senfileraw.close()


# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('PIDashboard.ui')

Dialog.toolButtonSelectInputFile.clicked.connect(onSelectFile)
Dialog.toolButtonSelectInputFile_2.clicked.connect(onSelectFile_2)
Dialog.pushButtonRefresh.clicked.connect(onRefresh)

"""

# On startup, look for an RMR in calling directory:
currentDir = os.getcwd()
rmrfiles = []
for file in os.listdir(currentDir):
    if file.endswith(".rmr"):
        rmrfiles.append(file)
if len(rmrfiles) < 1:
    print("No RMR found")
else:
    if len(rmrfiles) > 1:
        print("More than one one RMR found, using " + rmrfiles[-1])

    Dialog.lineEditInputFilePath.setText(rmrfiles[-1])

"""

# Activate the user interface:
Dialog.show()
sys.exit(app.exec_())







