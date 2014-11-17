__author__ = 'are'
'''
This scripts is a convenience tool to implement regularization rules (Prior Information Items) into an exisiting pst
file. It does not require command line parameters. This it what it does:

- it looks up the pst-files in the current directory. If none or more than one pst is present it ceases execution.
- it looks for all GENREG control files, expected to have the extension ".genreg".
- for each GENREG control file found:
    - run GENREG to create an temporary pst file
    - please the original pst file with the temporary one (delete / rename)
'''

import os
import sys
import subprocess

# find the pst - files in calling directory
currentDir = os.getcwd()
pstfiles = []

for file in os.listdir(currentDir):
    if file.endswith(".pst"):
        pstfiles.append(file)

if len(pstfiles) > 1:
    print("Warning: More than one one pst-file found, aborting")
    sys.exit(1)

if len(pstfiles) < 1:
    print("Error: No pst-file found! Aborting...")
    sys.exit(1)

# find the genreg files

genregFiles = []
for file in os.listdir(currentDir):
    if file.endswith(".genreg"):
        genregFiles.append(file)

# run genreg

tempFileName = "temp.pst"

for genregFile in genregFiles:
    print("processing " + genregFile)
    # run genreg:
    genregInFile = open("genreg.in", "w")
    genregInFile.write("\"" + pstfiles[0] + "\"\n")
    genregInFile.write("\"" + genregFile + "\"\n")
    genregInFile.write(tempFileName + "\n")
    genregInFile.close()
    subprocess.call("genreg < genreg.in", shell=True)

    # exchange files:
    if os.path.isfile(tempFileName):
        subprocess.call('del ' + pstfiles[0], shell=True)
        subprocess.call('ren ' + tempFileName + ' ' + pstfiles[0], shell=True)
        print("success!")
    else:
        print("fail!")





