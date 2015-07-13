__author__ = 'are'

import pyst
from pyst.utils.linearUncertainty import genlinpred

import sys
import os
import shutil
from subprocess import call

from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsScene
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.uic import loadUi

import matplotlib

matplotlib.use("Qt5Agg")

from QtPyst.QParameterValueViewWidget import *

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


def onselectpstfile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath_2.setText(path[0])


def onselectjcofile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath_3.setText(path[0])


def onIterationChanged():
    updatedata()


def onStateChangedDevBar():
    updatedata()


def onStateChangedBoundBracket():
    updatedata()


def onStateChangedPriorUncert():
    updatedata()


def onStateChangedPosteriorUncert():
    updatedata()


def onPushButtonRunGenlinpredPressed():
    listOfUncertaintyResults = calculatelinearuncertainty()
    pass


def calculatelinearuncertainty():
    path_pst = Dialog.lineEditInputFilePath_2.text()

    filename = path_pst.split("/")[-1]
    workpath = path_pst.replace(filename, "")
    case = filename.replace(".pst", "")

    os.chdir(workpath)

    # create PEST control file and JCO file without regularization
    call(["subreg1.exe", filename, "noreg.pst"])
    call(["jco2jco.exe", case, "noreg"])

    senfilepath = Dialog.lineEditInputFilePath.text()
    senfile = pyst.SenFile(senfilepath)

    fileList = {}

    for p in senfile.getparamaternames():
        outpath = workpath + p + ".genlinpred.out"
        genlinpred("noreg.pst", workpath, prediction_par=p, outfilename=outpath)
        fileList[p] = outpath


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
        'upper': 5,
    }

    for p in file_sen.getparamaternames():
        newpar = QTreeWidgetItem(0)
        newpar.setText(h['name'], p)
        newpar.setText(h['val'], str(file_sen.parhistory[CurrentIteration][p]))
        newpar.setText(h['sens'], str(file_sen.senhistory[CurrentIteration][p]))
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
        Phi = abs(log10(parval) - log10(prefval)) ** 2
        newPar.setText(2, "{:.7f}".format(Phi))

        # set Identifiability index
        expectedFilePath = pname+".genlinpred.out"
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
            preVar = genlinpredresult.predunc1.preCalTotalUncertaintyVariance
            preDev = preVar**0.5
            postVar = genlinpredresult.predunc1.postCalTotalUncertaintyVariance
            postDev = postVar**0.5
        else:
            postDev = 1


        parvalView.setPriorstdev(preDev)
        parvalView.setPosteriorstdev(postDev)
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

    for i in viewTreeItems.keys():
        viewTreeItems[i].setAxisMin(AxisMinGlobal)
        viewTreeItems[i].setAxisMax(AxisMaxGlobal)
        viewTreeItems[i].setAxisbase(AxisBaseGlobal)
        viewTreeItems[i].setAxisinterval(AxisIntervalGlobal)


# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('PIDashboard.ui')

Dialog.toolButtonSelectInputFile.clicked.connect(onselectsenfile)
Dialog.toolButtonSelectInputFile_2.clicked.connect(onselectpstfile)

Dialog.pushButtonRefresh.clicked.connect(onrefresh)
Dialog.pushButtonRunGenlinpred.clicked.connect(onPushButtonRunGenlinpredPressed)

Dialog.spinBox_IterationNumber.valueChanged.connect(onIterationChanged)

Dialog.checkBox_BoundBrackets.stateChanged.connect(onStateChangedBoundBracket)
Dialog.checkBox_Deviation.stateChanged.connect(onStateChangedDevBar)
Dialog.checkBox_PreCalParamUncert.stateChanged.connect(onStateChangedPriorUncert)
Dialog.checkBox_PostCalParamUncert.stateChanged.connect(onStateChangedPosteriorUncert)

Dialog.treeWidgetParameterState.setColumnWidth(0, 100)
Dialog.treeWidgetParameterState.setColumnWidth(1, 70)
Dialog.treeWidgetParameterState.setColumnWidth(2, 70)
Dialog.treeWidgetParameterState.setColumnWidth(3, 70)

Dialog.label_senFileNotReadable.setVisible(False)

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
