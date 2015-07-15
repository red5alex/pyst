__author__ = 'are'

import sys
import os
from subprocess import call

import pyst
from pyst.utils.linearUncertainty import genlinpred
from QtPyst.QParameterValueViewWidget import *

from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.uic import loadUi

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
    calculatelinearuncertainty()


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
    #TODO: consistency to be implemented per group
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

# Activate user interface:
Dialog.show()
sys.exit(app.exec_())
