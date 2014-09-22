__author__ = 'are'

import pyst
import sys
import os


def readArguments():
    try:
        if len(sys.argv) in [4, 5]:
            pestfilename = sys.argv[1]
            pestfile = pyst.PestCtrlFile(pestfilename)

            parname = sys.argv[2]
            if not parname in pestfile.params:
                print("ERROR: " + parname + " not defined in " + pestfilename)
                raise ValueError

            n = int(float(sys.argv[3]))
            if not n > 0:
                print('ERROR: n must be positive!')
                raise ValueError

            if len(sys.argv) == 5:
                outfile = sys.argv[4]
            else:
                outfile = parname + ".dat"
        else:
            raise ValueError

        return pestfile, parname, n, outfile

    except ValueError:
        path = os.path.dirname(__file__)  # directory of THIS script; help text expected in same dir
        usage_file = open(path + "\\beoscan_usage.txt")
        print(usage_file.read())
        usage_file.close()
        os._exit(0)


def generateParameterLevels_uniform(pestfile, parname, n):

    if n < 1:
        raise ValueError

    parlbnd = pestfile.params[parname].PARLBND
    parubnd = pestfile.params[parname].PARUBND
    increment = (parubnd - parlbnd) / (n - 1)

    parLevels = []
    for i in range(0, n):
            parLevels.append(parlbnd + i * increment)

    return parLevels


def writeParFiles(pestfile, parname, parlevels):

    n = len(parlevels)

    for i in range(0, n):
        parFile = pyst.ParamValueFile()
        pp = pestfile.params
        for p in pp:
            name = p
            value = pp[p].PARVAL1
            scale = pp[p].SCALE
            offset = pp[p].OFFSET

            if name == parname:
                value = parlevels[i]
            #TODO: tied parameters

            parFile.addPar(name, value, scale, offset)

        filename = "_" + parname + str(i) + ".par"
        parFile.write(filename)


def writePestInFile(basename, first, last, rrffilename="", packagesize=-1, infilename="pest.in"):
    if packagesize == -1:
        packagesize = last - first + 1
    if rrffilename == "":
        rrffilename = basename + ".rrf"

    file = open(infilename, "w")
    file.write(basename + "\n")
    file.write(str(first) + "\n")
    file.write(str(last) + "\n")
    file.write(str(packagesize) + "\n")
    file.write(rrffilename)

    file.close()


def main():

    print("BeoSCAN pre-processing:")
    pestfile, parname, npar, outfile = readArguments()

    filename = parname + "<n>.par"
    print("generating parameter files " + filename)
    print("with n = 0 .." + str(npar-1))

    parLevels = generateParameterLevels_uniform(pestfile, parname, npar)
    writeParFiles(pestfile, parname, parLevels)

    print("Generating PEST keyboard input stream (pest.in)")
    writePestInFile(parname, 0, npar-1)

    print("BeoSCAN pre-processing completed")

main()
