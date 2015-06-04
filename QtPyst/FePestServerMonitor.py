__author__ = 'are'

import sys

import os
import sys
import pyst
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
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

    # Load the RMR file
    path = Dialog.lineEditInputFilePath.text()
    testrmr = pyst.RunManagementRecord(path)


    "D:/Repositories/red5alex.cloudforge/pyst/trunk/example_files/runManagementRecord.rmr"

    # Write statistics to nodes - output file
    #outfile = open(currentDir+"\\"+rmrfiles[-1]+".nodes", "w")
    #outfile.write("STR = # of started model runs\n")
    Dialog.plainTextEdit.appendPlainText("OK  = # of successfully finished model runs")
    #outfile.write("DUE = # of overdue model runs\n")
    Dialog.plainTextEdit.appendPlainText("LAT = # of model runs finished too late")
    Dialog.plainTextEdit.appendPlainText("STR = # of communication failures\n")
    Dialog.plainTextEdit.appendPlainText("ID\tserver\tslave\tOK\tLAT\tCOM\tjob\tlast run\tthis run\tstatus")

    nruns = 0


    for node in testrmr.nodes:

        newline = ""

        n = testrmr.nodes[node]
        status = n.getstatus()

        newline += str(n.index) + "\t"
        """
        outfile.write(n.hostname + "\t")
        outfile.write(str(n.localindex) + "\t\t")
        #outfile.write(str(n.getnumberofruns("RunCommencement")) + "\t")
        outfile.write(str(n.getnumberofruns("RunCompletion")) + "\t")
        nruns += n.getnumberofruns("RunCompletion")

        #outfile.write(str(n.getnumberofruns("OverdueRun")) + "\t")
        outfile.write(str(n.getnumberofruns("Late")) + "\t")
        outfile.write(str(n.getnumberofruns("CommunicationFailure")) + "\t")

        outfile.write(str(n.getcurrentrun()) + "\t")

        # get the duration of the last successful run
        dlast = -1.
        if len(n.getsuccesfulruns()) > 0 and not status == "Communication Failure":
            lastduration = n.getsuccesfulruns()[-1].getduration()
            outfile.write("["+str(lastduration).split(".")[0] + "]\t")
            dlast = lastduration.total_seconds()
        else:
            outfile.write("[-:--:--]\t")

        # get the duration of the current run and write to file
        dcurrent = -1.
        if status == "Model run complete" or \
                status == "Communication Failure":
            outfile.write("[-:--:--]\t")
        else:
            duration = str(datetime.datetime.now() - n.getcurrentruntime()).split(".")[0]
            outfile.write("["+duration + "]\t")
            dcurrent = (datetime.datetime.now() - n.getcurrentruntime()).total_seconds()

        # if a model is running, and the duration of the previous run is know, estimate the progress
        if len(n.getsuccesfulruns()) > 0 and \
                not status == "Model run complete" and\
                not status == "Communication Failure":
            progress = u" ({0}%)".format(str(int((dcurrent / dlast) * 100)))
        else:
            progress = ""

        outfile.write(str(n.getstatus()) + progress + "\t")
        """

        Dialog.plainTextEdit.appendPlainText(newline)


    """
    outfile.write("\n"+str(nruns) + " runs completed\n")


    print("\n\n")
    outfile = open(currentDir+"\\"+rmrfiles[-1]+".nodes")
    for l in outfile.readlines():
        print(l.strip())
    outfile.close()

    """




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





