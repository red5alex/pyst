__author__ = 'are'

import sys

import os
import sys
import pyst
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.uic import loadUi

# Script Implementation:

def onRefresh():
    loadRMR()

def onSelectFile():
    path = QFileDialog.getOpenFileName()
    Dialog.lineEditInputFilePath.setText(path[0])
    loadRMR()

def loadRMR():
    Dialog.plainTextEdit.clear()

    view = Dialog.treeWidgetSlaves
    view.clear()

    # Load the RMR file
    path = Dialog.lineEditInputFilePath.text()
    testrmr = pyst.RunManagementRecord(path)

    # Write statistics to nodes - output file
    Dialog.plainTextEdit.appendPlainText("OK  = # of successfully finished model runs")
    Dialog.plainTextEdit.appendPlainText("LAT = # of model runs finished too late")
    Dialog.plainTextEdit.appendPlainText("STR = # of communication failures\n")
    Dialog.plainTextEdit.appendPlainText("ID\tserver\tslave\tOK\tLAT\tCOM\tjob\tlast run\tthis run\tstatus")

    nruns = 0
    serverElements = {}

    for server in testrmr.servers:
        newServer = QTreeWidgetItem(0)
        newServer.setText(0, server)
        serverElements[server] = newServer
        view.addTopLevelItem(newServer)
        newServer.setExpanded(True)

    h = {
        'name':     0,
        'slaveId':  101,
        'OK':       3,
        'late':     4,
        'failed':   5,
        'jobId':    100,
        'lastrun':  6,
        'currentrun':   7,
        'status':       1,
        'completion':   2
    }

    for n in testrmr.nodes:
        node = testrmr.nodes[n]
        newSlave = QTreeWidgetItem(0)
        newSlave.setText(h['name'], str(node.localindex)+': Slave '+str(node.index))
        newSlave.setText(h['slaveId'], str(node.index))
        newSlave.setText(h['OK'], str(node.getnumberofruns("RunCompletion")))
        newSlave.setText(h['late'], str(node.getnumberofruns("Late")))
        newSlave.setText(h['failed'], str(node.getnumberofruns("CommunicationFailure")))
        newSlave.setText(h['currentrun'], str(node.getcurrentrun()))

        serverElements[node.hostname].addChild(newSlave)

        # get the status:
        status = node.getstatus()
        if status == 'Running model':
            status += " " +str(node.getcurrentrun())
        newSlave.setText(h['status'], status)

        # get the duration of the last successful run
        dlast = -1.
        if len(node.getsuccesfulruns()) > 0 and not status == "Communication Failure":
            lastduration = node.getsuccesfulruns()[-1].getduration()
            timestr = "["+str(lastduration).split(".")[0] + "]"
            dlast = lastduration.total_seconds()
        else:
            timestr = "[--:--:--]"

        newSlave.setText(h['lastrun'], timestr)

        # get the duration of the current run and write to file
        dcurrent = -1.
        if status == "Model run complete" or \
                status == "Communication Failure":
            timestr = "[--:--:--]"
        else:
            duration = str(datetime.datetime.now() - node.getcurrentruntime()).split(".")[0]
            timestr = "["+duration + "]"
            dcurrent = (datetime.datetime.now() - node.getcurrentruntime()).total_seconds()
        newSlave.setText(h['currentrun'], timestr)

        # if a model is running, and the duration of the previous run is know, estimate the progress
        if len(node.getsuccesfulruns()) > 0 and \
                not status == "Model run complete" and\
                not status == "Communication Failure":
            progress = u" ({0}%)".format(str(int((dcurrent / dlast) * 100)))
        else:
            progress = ""
        newSlave.setText(h['completion'], progress)

        ncompleted = testrmr.getnumberofcompletedruns()
        Dialog.lcdNumberTotalRuns.display(ncompleted)



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
        dlast = -1.
        if len(n.getsuccesfulruns()) > 0 and not status == "Communication Failure":
            lastduration = n.getsuccesfulruns()[-1].getduration()
            newline += "["+str(lastduration).split(".")[0] + "]\t"
            dlast = lastduration.total_seconds()
        else:
            newline += "[-:--:--]\t"

        # get the duration of the current run and write to file
        dcurrent = -1.
        if status == "Model run complete" or \
                status == "Communication Failure":
            newline += "[-:--:--]\t"
        else:
            duration = str(datetime.datetime.now() - n.getcurrentruntime()).split(".")[0]
            newline += "["+duration + "]\t"
            dcurrent = (datetime.datetime.now() - n.getcurrentruntime()).total_seconds()

        # if a model is running, and the duration of the previous run is know, estimate the progress
        if len(n.getsuccesfulruns()) > 0 and \
                not status == "Model run complete" and\
                not status == "Communication Failure":
            progress = u" ({0}%)".format(str(int((dcurrent / dlast) * 100)))
        else:
            progress = ""

        newline += str(n.getstatus()) + progress + "\t"

        Dialog.plainTextEdit.appendPlainText(newline)

    Dialog.plainTextEdit.appendPlainText("\n"+str(nruns) + " runs completed\n")

# Initialize User Interface:
app = QApplication(sys.argv)
Dialog = loadUi('FePestServerMonitor.ui')

Dialog.toolButtonSelectInputFile.clicked.connect(onSelectFile)
Dialog.pushButtonRefresh.clicked.connect(onRefresh)

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

# Activate the user interface:
Dialog.show()
sys.exit(app.exec_())





