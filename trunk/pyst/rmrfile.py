__author__ = 'are'

import datetime

class RunManagementRecord:
    case = ""
    protocol = ""
    parlam = -1
    slowRunFactor = -1.
    events = []

    class Events:

        class GeneralEvent:
            def __init__(self, messagetext, type="unknown"):
                self.message = messagetext
                self.type = type

        class AssignmentEvent:
            def __init__(self, messagetext, timestamp, nodeindex, workingdir):
                self.message = messagetext
                self.type = "Assignment"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.workdir = workingdir

        class RunCommencementEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "RunCommencement"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.runindex = int(runindex)

        class CommunicationFailureEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "CommunicationFailure"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.runindex = int(runindex)

        class RunCompletionEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "RunCompletion"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.runindex = int(runindex)

        class OverdueRunEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "OverdueRun"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.runindex = int(runindex)

    def __init__(self, filename):
        self.load(filename)

    def load(self, filename):
        rmrfile = open(filename)

        lines = rmrfile.readlines()

        for l in lines:
            self.parseLine(l)

    def parseLine(self, line):

        def parseTime(timeString):
            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)

            w = line.split()
            t = w[2].split(':')
            s = t[2].split('.')

            y = int(1900)
            m = months[w[1]]
            d = int(w[0])
            h = int(t[0])
            min = int(t[1])
            sec = int(s[0])
            ms = int(s[1])*10000

            return datetime.datetime(y, m, d, h, min, sec, ms )

        if "PEST RUN MANAGEMENT RECORD: " in line:
            self.case = line.split()[-1]
            return

        if "COMMUNICATIONS PROTOCOL =" in line:
            self.protocol = line.split()[-1].strip(".")
            return

        if "PARLAM has been assigned a value of " in line:
            #words = line.split(7)
            self.parlam = int(line.split()[7].strip("."))
            #TODO: error check
            return

        if "SLOW RUN DECLARATION FACTOR   :" in line:
            self.slowRunFactor = float(line.split()[-1])
            return

        if "assigned to node at working directory" in line:
            timestamp = parseTime(line)
            w = line.split()
            self.events.append(self.Events.AssignmentEvent(line, timestamp, w[5], w[12]))
            return

        if "commencing on node" in line:
            timestamp = parseTime(line)
            w = line.split()
            self.events.append(self.Events.RunCommencementEvent(line, timestamp, w[9].strip('.'), w[5]))
            return

        if ("communications failure on node " in line) and ("will be re-assigned to another node." in line):
            timestamp = parseTime(line)
            w = line.split()
            self.events.append(self.Events.CommunicationFailureEvent(line, timestamp, w[7].strip(';'), w[10]))
            return

        if " completed on node " in line:
            timestamp = parseTime(line)
            w = line.split()
            self.events.append(self.Events.RunCompletionEvent(line, timestamp, w[9].strip('.'), w[5]))
            return

        if (" overdue run on node " in line) and ("may be re-assigned to another node." in line):
            timestamp = parseTime(line)
            w = line.split()
            self.events.append(self.Events.OverdueRunEvent(line, timestamp, w[7].strip(';'), w[10]))
            return

        #else
        if len(line.strip()) > 0:
            self.events.append(self.Events.GeneralEvent(line))

testrmr = RunManagementRecord("D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\example_files\\runManagementRecord.rmr")
pass