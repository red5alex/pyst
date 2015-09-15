__author__ = 'are'

import os
import sys
import pyst
import datetime
import math

from PyQt5.QtWidgets import QApplication, QFileDialog, QProgressBar
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.uic import loadUi

# Script Implementation:

def onrmrpathchange():
    path = Dialog.lineEditInputFilePath.text()
    if os.path.isfile(path):
        loadRMR()
        Dialog.pushButtonRefresh.setEnabled(True)
        Dialog.label_fileNotFound.setVisible(False)
    else:
        Dialog.pushButtonRefresh.setEnabled(False)
        if path.strip() != "":
            Dialog.label_fileNotFound.setVisible(True)
        else:
            Dialog.label_fileNotFound.setVisible(False)


def onRefresh():
    loadRMR()


def onSelectFile():
    path = QFileDialog.getOpenFileName()[0]
    Dialog.lineEditInputFilePath.setText(path)
    # if os.path.isfile(path):
    #    loadRMR()
    #    Dialog.pushButtonRefresh.setEnabled(True)
    # else:
    #   Dialog.pushButtonRefresh.setEnabled(False)


def loadRMR():
    Dialog.plainTextEdit.clear()

    nodeView = Dialog.treeWidgetSlaves
    nodeView.clear()

    runView = Dialog.treeWidgetRuns
    runView.clear()

    # Load the RMR file
    path = Dialog.lineEditInputFilePath.text()
    testrmr = pyst.RunManagementRecord(path)


# POPULATE SERVER STATUS TAB

    nruns = 0
    serverElements = {}

    for server in testrmr.servers:
        newServer = QTreeWidgetItem(0)
        newServer.setText(0, server)
        serverElements[server] = newServer
        nodeView.addTopLevelItem(newServer)
        newServer.setExpanded(True)

    h = {
        'name': 0,
        'slaveId': 101,
        'OK': 3,
        'late': 4,
        'failed': 5,
        'jobId': 100,
        'lastrun': 6,
        'currentrun': 7,
        'status': 1,
        'completion': 2
    }

    for n in testrmr.nodes:
        node = testrmr.nodes[n]

        newSlave = QTreeWidgetItem(0)
        serverElements[node.hostname].addChild(newSlave)

        newSlave.setText(h['name'], str(node.localindex) + ': Slave ' + str(node.index))
        newSlave.setText(h['slaveId'], str(node.index))
        newSlave.setText(h['OK'], str(node.getnumberofruns("RunCompletion")))
        newSlave.setText(h['late'], str(node.getnumberofruns("Late")))
        newSlave.setText(h['failed'], str(node.getnumberofruns("CommunicationFailure")))
        newSlave.setText(h['currentrun'], str(node.getcurrentrun()))

        # get the status:
        status = node.getstatus()
        if status == 'Running model':
            status += " " + str(node.getcurrentrun())
        newSlave.setText(h['status'], status)

        # get the duration of the last successful run
        daverage = -1.
        avduration = None
        if len(node.getsuccesfulruns()) > 0 and not status == "Communication Failure":
            #TODO: ..and not "run failure" or whatever the keyword is
            avduration = node.getaverageruntime()  # might return None
        if avduration is not None:
            timestr = "[" + str(avduration).split(".")[0] + "]"
            daverage = avduration.total_seconds()
        else:
            timestr = "[--:--:--]"

        newSlave.setText(h['lastrun'], timestr)

        # get the duration of the current run and write to file
        dcurrent = -1.
        if status == "Model run complete" or \
                        status == "Communication Failure":
            timestr = "[--:--:--]"
        else:
            # TODO fix this, Exception is thrown if a a slave has never been assigned a job yet
            duration = str(datetime.datetime.now() - node.getcurrentruntime()).split(".")[0]
            timestr = "[" + duration + "]"
            dcurrent = (datetime.datetime.now() - node.getcurrentruntime()).total_seconds()
        newSlave.setText(h['currentrun'], timestr)

        # if a model is running, and the duration of the average run is know, estimate the progress
        pb = QProgressBar()
        pb.setTextVisible(True)
        pb.setVisible(False)
        if status in ["Running model", "OverdueRun"]:
            if len(node.getsuccesfulruns()) == 0:  # first run
                pb.setMaximum(0)  # busy indicator

        if len(node.getsuccesfulruns()) > 0 and \
                not status == "Model run complete" and \
                not status == "Communication Failure":
            percentage = (dcurrent / daverage) * 100
            progtext = u" ({0}%)".format(str(int((dcurrent / daverage) * 100)))
            if percentage <= 100:
                pb.setMaximum(100)
            else:
                pb.setMaximum(0)  # busy indicator
            pb.setValue(percentage)
            pb.text = progtext
            pb.setVisible(True)
        else:
            pb.setVisible(False)

        Dialog.treeWidgetSlaves.setItemWidget(newSlave, h['completion'], pb)
        pb.setMaximumHeight(14)

# POPULATE RUN WINDOW
    iterationTreeWidgets = {}
    phaseTreeWidgets = {}

    for iteration in testrmr.iterations:
        newiteration = QTreeWidgetItem(0)
        newiteration.setText(0, "Iteration " + str(iteration.index))
        iterationTreeWidgets[iteration] = newiteration
        runView.addTopLevelItem(newiteration)
        newiteration.setExpanded(True)

        for phase in iteration.phases:
            newphase = QTreeWidgetItem(0)
            newphase.setText(0, phase.type)
            phaseTreeWidgets[phase] = newphase
            iterationTreeWidgets[iteration].addChild(newphase)
            newphase.setExpanded(False)

            for runkey in phase.runs:
                run = testrmr.runs[runkey]
                newrun = QTreeWidgetItem(0)

                newrun.setText(0, "model " + str(run.index))

                status = run.getstatus()
                if status == "Model run complete":
                    newrun.setText(1, "complete")
                elif status == "Running model":
                    newrun.setText(1, "in prgress")
                else:
                    newrun.setText(1, status)

                nodeid = run.getlastnode()
                if nodeid is not None:
                    node = testrmr.nodes[nodeid]
                    newrun.setText(2, node.hostname)
                    newrun.setText(3, str(node.localindex))

                duration = run.getduration()
                newrun.setText(4, "[" + str(duration).split(".")[0] + "]")

                newphase.addChild(newrun)

    ni = len(testrmr.iterations)
    if ni > 0:
        lastIteration = testrmr.iterations[-1]
        iterationTreeWidgets[lastIteration].setExpanded(True)
        np = len(lastIteration.phases)
        if np > 0:
            lastPhase = lastIteration.phases[-1]
            phaseTreeWidgets[lastPhase].setExpanded(True)

# SET LCD DISPLAYS
    ncompleted = testrmr.getnumberofcompletedruns()
    Dialog.lcdNumberTotalRuns.display(ncompleted)
    Dialog.lcdNumberTotalServers.display(len(testrmr.servers))
    Dialog.lcdNumberTotalSlaves.display(len(testrmr.nodes))

    rph = testrmr.getrunsperhour()
    rph = round(rph,4)
    if rph >= 0.1:
        rph = round(rph,3)
    if rph >= 1.:
        rph = round(rph,2)
    if rph >= 10.:
        rph = round(rph,1)
    if rph >= 100.:
        rph = round(rph,0)
    Dialog.lcdNumberRunsPerHour.display(rph)

# POPULATE TEXT BASED SERVER STATUS (NOT SHOWN)
    """
    # Write statistics to nodes - output file
    Dialog.plainTextEdit.appendPlainText("OK  = # of successfully finished model runs")
    Dialog.plainTextEdit.appendPlainText("LAT = # of model runs finished too late")
    Dialog.plainTextEdit.appendPlainText("STR = # of communication failures\n")
    Dialog.plainTextEdit.appendPlainText("ID\tserver\tslave\tOK\tLAT\tCOM\tjob\tlast run\tthis run\tstatus")

    for node in testrmr.nodes:

        newline = ""
        n = testrmr.nodes[node]
        status = n.getstatus()
        newline += str(n.index) + "\t"  # ID
        newline += n.hostname + "\t"  # server
        newline += str(n.localindex) + "\t"  # slave
        # newline += str(n.getnumberofruns("RunCommencement")) + "\t")
        newline += str(n.getnumberofruns("RunCompletion")) + "\t"
        nruns += n.getnumberofruns("RunCompletion")

        # newline += str(n.getnumberofruns("OverdueRun")) + "\t")
        newline += str(n.getnumberofruns("Late")) + "\t"
        newline += str(n.getnumberofruns("CommunicationFailure")) + "\t"

        newline += str(n.getcurrentrun()) + "\t"

        # get the duration of the last successful run
        daverage = -1.
        if len(n.getsuccesfulruns()) > 0 and not status == "Communication Failure":
            avduration = n.getsuccesfulruns()[-1].getduration()
            newline += "[" + str(avduration).split(".")[0] + "]\t"
            daverage = avduration.total_seconds()
        else:
            newline += "[-:--:--]\t"

        # get the duration of the current run and write to file
        dcurrent = -1.
        if status == "Model run complete" or \
                        status == "Communication Failure":
            newline += "[-:--:--]\t"
        else:
            duration = str(datetime.datetime.now() - n.getcurrentruntime()).split(".")[0]
            newline += "[" + duration + "]\t"
            dcurrent = (datetime.datetime.now() - n.getcurrentruntime()).total_seconds()

        # if a model is running, and the duration of the previous run is know, estimate the progress
        if len(n.getsuccesfulruns()) > 0 and \
                not status == "Model run complete" and \
                not status == "Communication Failure":
            progtext = u" ({0}%)".format(str(int((dcurrent / daverage) * 100)))
        else:
            progtext = ""

        newline += str(n.getstatus()) + progtext + "\t"

        Dialog.plainTextEdit.appendPlainText(newline)

    Dialog.plainTextEdit.appendPlainText("\n" + str(nruns) + " runs completed\n")
    """

# LOAD RAW RUN MANAGEMENT RECORD FILE INTO RMR TAB
    Dialog.plainTextEdit_RMRFileContent.clear()
    rmrfile = open(path)
    for l in rmrfile.readlines():
        Dialog.plainTextEdit_RMRFileContent.appendPlainText(l.strip())
    rmrfile.close()

# INITIALIZE USER ITERFACE
app = QApplication(sys.argv)
Dialog = loadUi('FePestServerMonitor.ui')

Dialog.tabWidget.removeTab(1)

Dialog.lineEditInputFilePath.textChanged.connect(onrmrpathchange)
Dialog.toolButtonSelectInputFile.clicked.connect(onSelectFile)
Dialog.pushButtonRefresh.clicked.connect(onRefresh)

Dialog.label_fileNotFound.setVisible(False)

Dialog.treeWidgetSlaves.setColumnWidth(3, 25)
Dialog.treeWidgetSlaves.setColumnWidth(4, 25)
Dialog.treeWidgetSlaves.setColumnWidth(5, 25)
Dialog.treeWidgetSlaves.setColumnWidth(6, 100)
Dialog.treeWidgetSlaves.setColumnWidth(7, 100)

Dialog.treeWidgetRuns.setColumnWidth(0, 170)
Dialog.treeWidgetRuns.setColumnWidth(1, 80)
Dialog.treeWidgetRuns.setColumnWidth(2, 100)
Dialog.treeWidgetRuns.setColumnWidth(3, 40)
Dialog.treeWidgetRuns.setColumnWidth(4, 100)

# On startup, look for an RMR in calling directory:
currentDir = os.getcwd()
rmrfiles = []
for file in os.listdir(currentDir):
    if file.endswith(".rmr"):
        rmrfiles.append(file)
if len(rmrfiles) < 1:
    pass
    # print("No RMR found")
else:
    if len(rmrfiles) > 1:
        pass
    # print("More than one one RMR found, using " + rmrfiles[-1])

    Dialog.lineEditInputFilePath.setText(rmrfiles[-1])

# Activate the user interface:
Dialog.show()
sys.exit(app.exec_())
