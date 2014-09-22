__author__ = 'are'

import pyst
import sys
import os


def readArguments():
    try:
        if len(sys.argv) == 3:
            runrecord = sys.argv[1]
            datfilename = sys.argv[2]

        else:
            raise ValueError

        return runrecord, datfilename

    except ValueError:
        usage_file = open(os.path.dirname(__file__) + "\\beoscan-post_usage.txt")
        print(usage_file.read())
        usage_file.close()
        exit(0)


def main():

    print("BeoSCAN post-processing:")
    runrecordfilename, datfilename = readArguments()
    print("reading run record file " + runrecordfilename)
    runRecord = pyst.RunRecordFile(runrecordfilename)
    print("saving to results file " + datfilename)
    runRecord.saveastable(datfilename)
    print("BeoJACTEST post-processing completed")


main()
