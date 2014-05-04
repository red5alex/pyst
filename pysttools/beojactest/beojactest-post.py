__author__ = 'are'

import pyst
import sys
import os


def readArguments():
    try:
        if len(sys.argv) == 4:
            runrecord = sys.argv[1]
            parname = sys.argv[2]
            datfilename = sys.argv[3]

        else:
            raise ValueError

        return runrecord, parname, datfilename

    except ValueError:
        usage_file = open(os.path.dirname(__file__) + "\\beojactest-post_usage.txt")
        print(usage_file.read())
        usage_file.close()
        exit(0)


def main():

    print("BeoJACTEST pre-processing:")
    runrecordfilename, parname, datfilename = readArguments()
    print("reading run record file " + runrecordfilename)
    runRecord = pyst.RunRecordFile(runrecordfilename)
    print("saving to results file " + datfilename)
    runRecord.saveToDat(parname, datfilename)
    print("BeoJACTEST post-processing completed")

main()
