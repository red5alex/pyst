__author__ = 'are'

from subprocess import call
import os
import time

# user settings

sequence = range(1, 8)
workfolder = "D:/Repositories/auper1-stor_SVN/41801573_FreePort_SVN/work/model/Localmodels/Tenke/femdata/"
femfilename = "Tenke_2014_r136_PEST_A_Cal1SS.fem"

# script implementation
os.chdir(workfolder)
speeduptable = {}
logfile = open(femfilename+".log", "w")
for threadnumber in sequence:
    print("running model "+femfilename+" using "+str(threadnumber)+" thread:")
    t0 = time.time()
    call(["feflow62c.exe", femfilename, "threads "+str(threadnumber)])
    dt = time.time() - t0
    print("finished in "+str(dt))
    speeduptable[int(threadnumber)] = dt
    logfile.write("threads="+str(threadnumber)+"\t"+str(dt))
logfile.close()

