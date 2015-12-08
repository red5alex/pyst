__author__ = 'are'

import sys
import os
from subprocess import check_output, CalledProcessError, STDOUT

import pyst
from pyst.utils.linearUncertainty import genlinpred
from QtPyst.QParameterValueViewWidget import *

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QApplication, QSizePolicy, QTreeWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi

import matplotlib
matplotlib.use("Qt5Agg")
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import math

import time

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class SpeedUpPlotCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 8.0, 1.0)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)



pstfile = None
senfile = None


def onrefresh():
    updatedata()

    path_sen = Dialog.lineEditInputFilePath.text()
    file_sen = pyst.SenFile(path_sen)
    iterations = file_sen.getnumberofiterations()
    Dialog.spinBox_IterationNumber.setValue(iterations)


def onselectsenfile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])


class RunTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setrundata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setrundata(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


def onrunsingleinstancetest():
    sequence = Dialog.lineEdit_sequenceSingleTest.text().split(",")
    modelpath = Dialog.lineEditInputFilePath.text()

    logfile = open(modelpath+".log","w")

    table = Dialog.tableWidget_singleTestResult
    rowpositions = {}

    outwindow = Dialog.plainTextEdit_SingleTestOut
    outwindow.clear()

    for r in sequence:
        rowposition = table.rowCount()
        table.insertRow(rowposition)
        table.setItem(rowposition, 0, QTableWidgetItem(r))
        table.setItem(rowposition, 1, QTableWidgetItem("queued"))
        rowpositions[r] = rowposition

    speeduptable = {}
    for r in sequence:
        rowposition = rowpositions[r]
        table.setItem(rowposition, 1, QTableWidgetItem("running"))
        t0 = time.time()
        call_to(["feflow62c.exe", modelpath, "threads "+r], outwindow)
        dt = time.time() - t0
        table.setItem(rowposition, 1, QTableWidgetItem("complete"))
        timeItem = QTableWidgetItem(str(dt))
        table.setItem(rowposition, 2, timeItem)
        speeduptable[int(r)] = dt

        logfile.write("threads="+r+"\t"+str(dt))

    logfile.close()



def call_to(args, target):
    try:
        prompt = check_output(args, stderr=STDOUT)
        target.appendPlainText(str(prompt.decode('UTF-8')))
    except CalledProcessError:
        target.appendPlainText("Error Running Model!")


def calculatelinearuncertainty():
    path_pst = Dialog.lineEditInputFilePath_2.text()

    filename = path_pst.split("/")[-1]
    workpath = path_pst.replace(filename, "")
    case = filename.replace(".pst", "")

    os.chdir(workpath)

    # create PEST control file and JCO file without regularization
    window = Dialog.plainTextEdit_Genlinpredprompt
    call_to(["subreg1.exe", filename, "noreg.pst"], window)
    call_to(["jco2jco.exe", case, "noreg"], window )

    senfilepath = Dialog.lineEditInputFilePath.text()
    senfile = pyst.SenFile(senfilepath)

    fileList = {}

    for p in senfile.getparamaternames():
        outpath = workpath + p + ".genlinpred.out"
        genlinpred("noreg.pst", workpath, prediction_par=p, outfilename=outpath, writeoutputto=window)
        fileList[p] = outpath

    Dialog.plainTextEdit_Genlinpredout.clear()
    for f in fileList:
        outpath = fileList[f]
        Dialog.plainTextEdit_Genlinpredout.appendPlainText(outpath)

    Dialog.checkBox_PostCalParamUncert.setEnabled(True)


def updatedata():
    # Load the SEN file
    path_sen = Dialog.lineEditInputFilePath.text()
    file_sen = pyst.SenFile(path_sen)

    # abort if file is empty
    Dialog.label_senFileNotReadable.setVisible(False)
    if len(file_sen.groups) == 0:
        Dialog.label_senFileNotReadable.setVisible(True)
        return

    path_pst = Dialog.lineEditInputFilePath_2.text()
    file_pst = pyst.PestCtrlFile(path_pst)

    # change working directory
    filename = path_pst.split("/")[-1]
    workpath = path_pst.replace(filename, "")
    os.chdir(workpath)

    # set spinbox and LCD to last iteration
    iterations = file_sen.getnumberofiterations()
    Dialog.spinBox_IterationNumber.setMaximum(iterations)
    CurrentIteration = Dialog.spinBox_IterationNumber.value()
    Dialog.lcdNumberTotalRuns.display(iterations)

    # POPULATE PREFERRED VALUES TREE
    view = Dialog.treeWidgetSlaves
    view.clear()
    treeelements = {}
    for group in file_sen.groups:
        newgroup = QTreeWidgetItem(0)
        newgroup.setText(0, group)
        treeelements[group] = newgroup
        view.addTopLevelItem(newgroup)
        newgroup.setExpanded(True)

    h = {
        'name': 0,
        'val': 1,
        'sens': 2,
        'lower': 3,
        'pref': 4,
        'upper': 5}  # column numbers

    for p in file_sen.getparamaternames():
        newpar = QTreeWidgetItem(0)
        newpar.setText(h['name'], p)
        newpar.setText(h['val'], str(file_sen.parhistory[CurrentIteration][p]))
        newpar.setText(h['sens'], str(file_sen.senhistory[CurrentIteration][p]))
        newpar.setText(h['lower'], str(file_pst.params[p].PARLBND))
        newpar.setText(h['pref'], str(file_pst.params[p].PARVAL1))
        newpar.setText(h['upper'], str(file_pst.params[p].PARUBND))

        treeelements[file_sen.membership[p]].addChild(newpar)

    # POPULATE PARAMETER STATE VIEW
    view = Dialog.treeWidgetParameterState
    view.clear()
    # get Parametergroups as top level items:
    viewTopLevelItems = {}
    viewTreeItems = {}
    for gname in file_sen.groups:
        newGroupItem = QTreeWidgetItem(0)
        newGroupItem.setText(0, gname)
        newScaleView = QParameterValueViewScale(logTransform=True)
        viewTreeItems[gname.lower()] = newScaleView
        viewTopLevelItems[gname] = newGroupItem
        view.addTopLevelItem(newGroupItem)
        Dialog.treeWidgetParameterState.setItemWidget(newGroupItem, 4, newScaleView)
        newGroupItem.setExpanded(True)

    AxisMinGlobal = None
    AxisMaxGlobal = None
    AxisBaseGlobal = 0
    AxisIntervalGlobal = 0

    parvals = file_sen.parhistory[CurrentIteration]
    for pname in file_sen.getparamaternames():
        parameter = file_pst.params[pname]

        newPar = QTreeWidgetItem(0)
        viewTopLevelItems[parameter.PARGP].addChild(newPar)
        newPar.setText(0, pname)

        # set Sensitivity
        sh = file_sen.senhistory
        newPar.setText(1, str(sh[CurrentIteration][pname]))

        # set Phi contrib
        ph = file_sen.parhistory
        parval = ph[CurrentIteration][pname]
        prefval = parameter.PARVAL1
        phi = abs(log10(parval) - log10(prefval)) ** 2
        newPar.setText(2, "{:.7f}".format(phi))

        # set Identifiability index
        expectedFilePath = pname + ".genlinpred.out"
        if os.path.isfile(expectedFilePath):
            genlinpredresult = pyst.GenlinpredOutFile(expectedFilePath)
            identifiabilityIndex = genlinpredresult.parameterUncertainty.identifiability[pname]
            newPar.setText(3, "{:.7f}".format(identifiabilityIndex))

        # set parameterview
        parvalView = QParameterValueView(logTransform=True)
        parvalView.setParlbnd(parameter.PARLBND)
        parvalView.setParubnd(parameter.PARUBND)
        parvalView.setParval(parvals[pname.lower()])
        parvalView.setPrefval(parameter.PARVAL1)

        if os.path.isfile(expectedFilePath):
            genlinpredresult = pyst.GenlinpredOutFile(expectedFilePath)
            priorvariance = genlinpredresult.predunc1.preCalTotalUncertaintyVariance
            priorstddev = priorvariance ** 0.5
            posteriorvar = genlinpredresult.predunc1.postCalTotalUncertaintyVariance
            posteriorstddev = posteriorvar ** 0.5
        else:
            priorstddev = 1
            posteriorstddev = 1

        parvalView.setPriorstdev(priorstddev)
        parvalView.setPosteriorstdev(posteriorstddev)
        parvalView.setAxisMin(parameter.PARLBND)
        parvalView.setAxisMax(parameter.PARUBND)

        parvalView.showBoundBracket(Dialog.checkBox_BoundBrackets.isChecked())
        parvalView.showDevBar(Dialog.checkBox_Deviation.isChecked())
        parvalView.showPreCalRange(Dialog.checkBox_PreCalParamUncert.isChecked())
        parvalView.showPostCalRange(Dialog.checkBox_PostCalParamUncert.isChecked())

        if AxisMinGlobal is None or parameter.PARLBND < AxisMinGlobal:
            AxisMinGlobal = parameter.PARLBND
        if AxisMaxGlobal is None or parameter.PARUBND > AxisMaxGlobal:
            AxisMaxGlobal = parameter.PARUBND
        Dialog.treeWidgetParameterState.setItemWidget(newPar, 4, parvalView)
        viewTreeItems[pname.lower()] = parvalView

    # set consistent axis scale amongst all widgets
    # TODO: consistency to be implemented per group
    for item in viewTreeItems.keys():
        viewTreeItems[item].setAxisMin(AxisMinGlobal)
        viewTreeItems[item].setAxisMax(AxisMaxGlobal)
        viewTreeItems[item].setAxisbase(AxisBaseGlobal)
        viewTreeItems[item].setAxisinterval(AxisIntervalGlobal)

    # POPULATE FILE WINDOWS
    Dialog.plainTextEdit.clear()  # SEN File Window
    senfileraw = open(path_sen)
    lines = senfileraw.readlines()
    for l in lines:
        Dialog.plainTextEdit.appendPlainText(l.replace("\n", ""))
    senfileraw.close()

    Dialog.plainTextEdit_PstFile.clear()  # PST File Window
    pstfileraw = open(path_pst)
    lines = pstfileraw.readlines()
    for l in lines:
        Dialog.plainTextEdit_PstFile.appendPlainText(l.replace("\n", ""))
    pstfileraw.close()

# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('ParallelPerformanceTest.ui')

figure = Figure()
canvas = FigureCanvas(figure)

l = Dialog.gridLayout_PREDVAR
sc = SpeedUpPlotCanvas(Dialog, width=5, height=4, dpi=100)
l.addWidget(sc)

figure.add_subplot(111)
canvas.draw()

Dialog.toolButtonSelectInputFile.clicked.connect(onselectsenfile)
Dialog.pushButtonRunSingleInstanceTest.clicked.connect(onrunsingleinstancetest)

# Activate user interface:
Dialog.show()
sys.exit(app.exec_())
