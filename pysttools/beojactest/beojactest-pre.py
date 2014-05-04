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
        absPathThisPyScript = os.path.realpath(__file__)  # directory of THIS script
        usage_file = open(absPathThisPyScript.replace("beojactest.py", "beojactest_usage.txt"))
        print(usage_file.read())
        usage_file.close()
        os._exit(0)


def generateParameterLevels(pestfile, parname, n):

    parBaseVal = pestfile.params[parname].PARVAL1
    parGroup = pestfile.params[parname].PARGP
    increment = pestfile.paramGroups[parGroup].DERINC
    incrementType = pestfile.paramGroups[parGroup].INCTYP

    if incrementType == "relative":
        a = 1. + increment
        b = 0.
    else:  # = "absolute"
        a = 1.
        b = increment

    #TODO: rel_to_max
    #TODO: regard bounds

    parLevels = [parBaseVal]
    direction = 1
    for i in range(0, n):
        if direction == 1:  # upwards direction
            parLevels.append(parLevels[-1] * a + b)
            direction = -direction
        else:  # downwards direction
            parLevels.insert(0, parLevels[0] / a - b)
            direction = -direction
    return parLevels


def writeparfiles(pestfile, parname, parlevels):
    workPath = "."

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

        parFile.write(parname + str(i) + ".par")


def main():

    pestfile, parname, npar, outfile = readArguments()
    parLevels = generateParameterLevels(pestfile, parname, npar)
    writeparfiles(pestfile, parname, parLevels)

main()


