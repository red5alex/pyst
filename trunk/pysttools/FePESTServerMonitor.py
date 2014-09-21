__author__ = 'are'

import os
import sys
import pyst
import datetime

# find the RMR - file in calling directory
currentDir = os.getcwd()
rmrfiles = []

for file in os.listdir(currentDir):
    if file.endswith(".rmr"):
        rmrfiles.append(file)

if len(rmrfiles) > 1:
    print("Warning: More than one one RMR found, using " + rmrfiles[-1])

if len(rmrfiles) < 1:
    print("Error: No RMR found! Aborting...")
    sys.exit(1)

# Load the RMR file
testrmr = pyst.RunManagementRecord(currentDir+"\\"+rmrfiles[-1])

# Write statistics to nodes - output file
outfile = open(currentDir+"\\"+rmrfiles[-1]+".nodes", "w")
outfile.write("STR = # of started model runs\n")
outfile.write("OK  = # of successfully finished model runs\n")
outfile.write("DUE = # of overdue model runs\n")
outfile.write("LAT = # of model runs finished too late\n")
outfile.write("STR = # of communication failures\n\n")
outfile.write("ID\tserver\tslave\tSTR\tOK\tDUE\tLAT\tCOM\trun\tlast run\tthis run\tstatus\n")

nruns = 0

for node in testrmr.nodes:
    n = testrmr.nodes[node]
    outfile.write(str(n.index) + "\t")
    outfile.write(n.hostname + "\t")
    outfile.write(str(n.localindex) + "\t\t")
    outfile.write(str(n.getnumberofruns("RunCommencement")) + "\t")
    outfile.write(str(n.getnumberofruns("RunCompletion")) + "\t")
    nruns += n.getnumberofruns("RunCompletion")

    outfile.write(str(n.getnumberofruns("OverdueRun")) + "\t")
    outfile.write(str(n.getnumberofruns("Late")) + "\t")
    outfile.write(str(n.getnumberofruns("CommunicationFailure")) + "\t")

    outfile.write(str(n.getcurrentrun()) + "\t")

    # get the duration of the last successful run
    dlast = -1.
    if len(n.getsuccesfulruns()) > 0:
        lastduration = n.getsuccesfulruns()[-1].getduration()
        outfile.write("["+str(lastduration).split(".")[0] + "]\t")
        dlast = lastduration.total_seconds()
    else:
        outfile.write("[-:--:--]\t")

    # get the duration of the current run and write to file
    dcurrent = -1.
    if n.getstatus() == "Model run complete":
        outfile.write("[-:--:--]\t")
    else:
        duration = str(datetime.datetime.now() - n.getcurrentruntime()).split(".")[0]
        outfile.write("["+duration + "]\t")
        dcurrent = (datetime.datetime.now() - n.getcurrentruntime()).total_seconds()

    # if a model is running, and the duration of the previous run is know, estimate the progress
    if len(n.getsuccesfulruns()) > 0 and n.getstatus() != "Model run complete":
        progress = " (" +str(int((dcurrent / dlast)*100))+"%)"
    else:
        progress = ""


    outfile.write(str(n.getstatus()) + progress + "\t")

    outfile.write("\n")

outfile.write("\n"+str(nruns) + " runs completed\n")
outfile.close()

print("\n\n")
outfile = open(currentDir+"\\"+rmrfiles[-1]+".nodes")
for l in outfile.readlines():
    print(l.strip())
outfile.close()



pass
