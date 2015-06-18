__author__ = 'are'

import pyst
import sys

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsScene
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.uic import loadUi

import matplotlib
matplotlib.use("Qt5Agg")
# from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure

pstfile = None
senfile = None


def onrefresh():
    updatedata()


def onselectfile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])


def onselectfile_2():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath_2.setText(path[0])


def updatedata():

    # POPULATE PREFERRED VALUES TREE

    view = Dialog.treeWidgetSlaves
    view.clear()

    # Load the SEN file
    path_sen = Dialog.lineEditInputFilePath.text()
    file_sen = pyst.SenFile(path_sen)

    path_pst = Dialog.lineEditInputFilePath_2.text()
    file_pst = pyst.PestCtrlFile(path_pst)

    iterations = file_sen.getnumberofiterations()
    Dialog.lcdNumberTotalRuns.display(iterations)

    treeelements = {}

    for group in file_sen.groups:
        newgroup = QTreeWidgetItem(0)
        newgroup.setText(0, group)
        treeelements[group] = newgroup
        view.addTopLevelItem(newgroup)
        newgroup.setExpanded(True)

    h = {
        'name':     0,
        'val':      1,
        'sens':     2,
        'lower':    3,
        'pref':     4,
        'upper':    5,
        }

    for p in file_sen.getparamaternames():
        newpar = QTreeWidgetItem(0)
        newpar.setText(h['name'], p)
        newpar.setText(h['val'], str(file_sen.parhistory[iterations][p]))
        newpar.setText(h['sens'], str(file_sen.senhistory[iterations][p]))
        newpar.setText(h['lower'], str(file_pst.params[p].PARLBND))
        newpar.setText(h['pref'], str(file_pst.params[p].PARVAL1))
        newpar.setText(h['upper'], str(file_pst.params[p].PARUBND))

        treeelements[file_sen.membership[p]].addChild(newpar)

    # POPULATE SEN FILE WINDOW

    Dialog.plainTextEdit.clear()

    senfileraw = open(path_sen)
    lines = senfileraw.readlines()
    for l in lines:
        Dialog.plainTextEdit.appendPlainText(l.replace("\n", ""))
    senfileraw.close()


# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('PIDashboard.ui')

gv = Dialog.graphicsView
gs = QGraphicsScene(gv)
gs.addLine(0., 0., 1., 1.)


Dialog.toolButtonSelectInputFile.clicked.connect(onselectfile)
Dialog.toolButtonSelectInputFile_2.clicked.connect(onselectfile_2)
Dialog.pushButtonRefresh.clicked.connect(onrefresh)

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