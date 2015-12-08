__author__ = 'are'

from subprocess import call
import os
import time

from openpyxl import Workbook
from openpyxl.charts import ScatterChart, Reference, Series

# user settings
# this script will execute a FEFLOW given by workfolder / femfilename and test the run time with different
# numbers of threads as provided by list sequence.
# results are written on screen, an ASCII logfile and an Exceltable

sequence = [1, 2, 3, 4, 5, 6, 7, 8]
workfolder = "D:/Repositories/auper1-stor_SVN/41801573_FreePort_SVN/work/model/Localmodels/Tenke/femdata/"
femfilename = "Tenke_2014_r136_PEST_A_Cal1SS.fem"

# script implementation

wb = Workbook()
ws = wb.active
ws.title = "Speedup"

ws.append(["FEFLOW Speedup Test"])
ws.append([""])
ws.append([""])
ws.append(["folder:", workfolder])
ws.append(["model:", femfilename])
ws.append([""])

ws.append(["threads", "time", "speedup"])

os.chdir(workfolder)
speeduptable = {}
logfile = open(femfilename+".parperformance", "w")

single_run = None

for threadnumber in sequence:
    print("running model "+femfilename+" using "+str(threadnumber)+" threads:")
    t0 = time.time()
    time.sleep(1/threadnumber)  # dummy model for testing
    # call(["feflow62c.exe", "-threads", str(threadnumber), femfilename])
    dt = time.time() - t0
    if dt == 0:
        dt = 0.001
    print("finished in "+str(dt))
    speeduptable[int(threadnumber)] = dt
    logfile.write("threads="+str(threadnumber)+"\t"+str(dt))

    if threadnumber <= 1:
        single_run = dt

    if single_run is not None:
        speedup = single_run / dt.real
        ws.append([threadnumber, dt.real, speedup])
    else:
        ws.append([threadnumber, dt.real])

n = len(sequence)

threadref = Reference(ws, (8, 1), (8+n, 1))
runtimeref = Reference(ws, (8, 2), (8+n, 2))
speedupref = Reference(ws, (8, 3), (8+n, 3))

runtimeseries = Series(runtimeref, "Run Time", xvalues=threadref)
speedupseries = Series(speedupref, "Speedup", xvalues=speedupref)

chart = ScatterChart()
chart.append(runtimeseries)

chart.append(speedupseries)
ws.add_chart(chart)

chart.title = "Run Time"

chart.x_axis.title = "Number of Threads"
chart.y_axis.title = "Run Time [sec]"

logfile.close()
outfile = femfilename+".parperformance.xlsx"
try:
    wb.save(outfile)
except PermissionError:
    while True:
        if input("Error Saving File. Enter to retry? (enter 'n' abort)") in ["n", "N"]:
            exit(1)
        else:
            try:
                wb.save(outfile)
                print(outfile+" written OK.")
                break
            except:
                pass
