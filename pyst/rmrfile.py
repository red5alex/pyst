__author__ = 'are'

import datetime
import os


class RunManagementRecord:
    case = ""
    protocol = ""
    parlam = -1
    slowrunfactor = -1.
    events = []
    nodes = {}

    class Events:

        class GeneralEvent:
            def __init__(self, messagetext, eventtype="unknown"):
                self.message = messagetext
                self.type = eventtype

        class AssignmentEvent:
            def __init__(self, messagetext, timestamp, nodeindex, workdir):
                self.message = messagetext
                self.type = "Assignment"
                self.statusMessage = "Node index assigned"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.workdir = workdir

        class RunCommencementEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "RunCommencement"
                self.statusMessage = "Running model"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)

        class CommunicationFailureEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "CommunicationFailure"
                self.statusMessage = "Communication Failure"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)

        class RunCompletionEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "RunCompletion"
                self.statusMessage = "Model run complete"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)

        class LateCompletionEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex=-1):
                self.message = messagetext
                self.type = "LateCompletion"
                self.statusMessage = "Model run complete (late)"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)

        class OverdueRunEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex):
                self.message = messagetext
                self.type = "OverdueRun"
                self.statusMessage = "Overdue"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)

    class Node:
        def __init__(self, index, workdir):
            self.index = index
            self.workdir = workdir
            self.ipadress = workdir.split("\\\\")[0]
            if "@" in workdir:
                self.name = self.workdir.split('@')[-1].strip('".')
                if "~" in self.name:
                    self.hostname = self.name.split("~")[0]
                    self.localindex = int(self.name.split("~")[1])
                else:
                    self.hostname = self.name
                    self.localindex = 0
            self.events = []

        def registerevent(self, event):
            self.events.append(event)

        def getnumberofruns(self, eventtype="success"):
            count = len([e for e in self.events if e.type == eventtype])
            return count

        def gettimeoflastevent(self):
            return self.events[-1].timestamp

        def getcurrentrun(self):
            for event in reversed(self.events):
                if hasattr(event,"run"):
                    if event.run > 0:
                         return event.run
            return -1

        def getstatus(self):
            for event in reversed(self.events):
                if hasattr(event,"statusMessage"):
                        return event.statusMessage
            #else:
            return "unknown"

    def __init__(self, filename):

        self.filemodtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        self.filecrttime = datetime.datetime.fromtimestamp(os.path.getctime(filename))

        self.load(filename)
        self.searchnewnodes(self.events, self.nodes)
        self.registerevents(self.events, self.nodes)

    def load(self, filename):
        rmrfile = open(filename)
        lines = rmrfile.readlines()
        for l in lines:
            self.parseline(l)

    def parseline(self, line):

        def parsetime(timestring):
            months = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)

            v = timestring.split()
            t = v[2].split(':')
            r = t[2].split('.')

            y = self.filemodtime.year
            m = months[v[1]]
            d = int(v[0])
            h = int(t[0])
            mn = int(t[1])
            sec = int(r[0])
            ms = int(r[1])*10000

            if sec > 59:
                sec = 0
                mn += 1
            if mn > 59:
                mn = 59
                sec = 59

            return datetime.datetime(y, m, d, h, mn, sec, ms)

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
            self.slowrunfactor = float(line.split()[-1])
            return

        if "assigned to node at working directory" in line:
            timestamp = parsetime(line)
            w = line.split()
            if len(w) == 13:
                #self.events.append(self.Events.AssignmentEvent(line, timestamp, w[5], w[12]))
                path = w[12]
            else:
                path = ""
                for s in w[12:]:
                    path += s + " "
            self.events.append(self.Events.AssignmentEvent(line, timestamp, w[5], path.strip()))
            return

        if "commencing on node" in line:
            timestamp = parsetime(line)
            w = line.split()
            self.events.append(self.Events.RunCommencementEvent(line, timestamp, w[9].strip('.'), w[5]))
            return

        if ("communications failure on node " in line) and ("will be re-assigned to another node." in line):
            timestamp = parsetime(line)
            w = line.split()
            self.events.append(self.Events.CommunicationFailureEvent(line, timestamp, w[7].strip(';'), w[10]))
            return

        if " completed on node " in line:
            timestamp = parsetime(line)
            w = line.split()
            if "old run so results not needed" in line:
                self.events.append(self.Events.LateCompletionEvent(line, timestamp, w[8].strip(';')))
            else:
                self.events.append(self.Events.RunCompletionEvent(line, timestamp, w[9].strip('.'), w[5]))
            return

        if (" overdue run on node " in line) and ("may be re-assigned to another node." in line):
            timestamp = parsetime(line)
            w = line.split()
            self.events.append(self.Events.OverdueRunEvent(line, timestamp, w[7].strip(';'), w[10]))
            return

        #else
        if len(line.strip()) > 0:
            self.events.append(self.Events.GeneralEvent(line))

    def searchnewnodes(self, eventlist, nodelist):
        for e in eventlist:
            if e.type == "Assignment":
                if e.node not in nodelist.keys():
                    nodelist[e.node] = self.Node(e.node, e.workdir)

    @staticmethod
    def registerevents(eventlist, nodelist):
        for e in eventlist:
            if hasattr(e, 'node'):
                nodelist[e.node].events.append(e)

