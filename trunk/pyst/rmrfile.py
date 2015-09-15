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
    runs = {}
    servers = {}
    iterations = []

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
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "RunCommencement"
                self.statusMessage = "Running model"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)
                self.iteration = iterationindex
                self.phase = phase

        class CommunicationFailureEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "CommunicationFailure"
                self.statusMessage = "Communication Failure"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)
                self.iteration = iterationindex
                self.phase = phase

        class RunCompletionEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "RunCompletion"
                self.statusMessage = "Model run complete"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)
                self.iteration = iterationindex
                self.phase = phase

        class LateCompletionEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "LateCompletion"
                self.statusMessage = "Model run complete (late)"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                if runindex is not None:
                    self.run = int(runindex)
                else:
                    self.run = None
                self.iteration = iterationindex
                self.phase = phase

        class OverdueRunEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "OverdueRun"
                self.statusMessage = "Overdue"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)
                self.iteration = iterationindex
                self.phase = phase

        class RunFailureEvent:
            def __init__(self, messagetext, timestamp, nodeindex, runindex, iterationindex, phase):
                self.message = messagetext
                self.type = "RunFailure"
                self.statusMessage = "Failure"
                self.timestamp = timestamp
                self.node = int(nodeindex)
                self.run = int(runindex)
                self.iteration = iterationindex
                self.phase = phase

        class NewIterationEvent:
            def __init__(self, messagetext, timestamp, iteration):
                self.message = messagetext
                self.type = "NewIteration"
                self.statusMessage = "NewIteration"
                self.timestamp = timestamp
                self.iteration = int(iteration)

        class StartJacobianEvent:
            def __init__(self, messagetext, iteration):
                self.message = messagetext
                self.type = "JacobianStart"
                self.statusMessage = "Calculating Jacobian"
                self.iteration = int(iteration)

        class ParameterUpgradeEvent:
            def __init__(self, messagetext, iteration):
                self.message = messagetext
                self.type = "ParamUpgradeStart"
                self.statusMessage = "Testing Parameter Upgrade"
                self.iteration = int(iteration)

        class LastModelRunEvent:
            def __init__(self, messagetext, iteration):
                self.message = messagetext
                self.type = "LastRun"
                self.statusMessage = "Final Model Run"
                self.iteration = int(iteration)

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
            self.runs = []

        def registerevent(self, event):
            self.events.append(event)

        def registerrun(self, run):
            self.runs.append(run)

        def getnumberofruns(self, eventtype="RunCompletion"):
            count = len([e for e in self.events if e.type == eventtype])
            return count

        def gettimeoflastevent(self):
            return self.events[-1].timestamp

        def getaverageruntime(self):
            n = self.getnumberofruns()
            if n == 0:
                return None  # no runs completed yet
            D = datetime.timedelta()
            for r in self.runs:
                d = r.getduration()
                D+=d
            return (D / n)

        def getcurrentrun(self):
            for event in reversed(self.events):
                if hasattr(event, "run"):
                    if event.run > 0:
                        return event.run
            return -1

        def getcurrentruntime(self):
            for event in reversed(self.events):
                if hasattr(event, "type"):
                    if event.type == "RunCommencement":
                        return event.timestamp

        def getstatus(self):
            for event in reversed(self.events):
                if hasattr(event, "statusMessage"):
                        return event.statusMessage
            #else:
            return "unknown"

        def getsuccesfulruns(self):
            runs = []
            for r in self.runs:
                if r.getstatus() == "Model run complete":
                    runs.append(r)
            return runs

    class Run:
        def __init__(self, index, iteration, phase):
            self.events = []
            self.index = index
            self.iteration = iteration
            self.phase = phase

        def registerevent(self, event):
            self.events.append(event)

        def getkey(self):
            phasekey = self.phase.type[0].lower()
            return str(self.iteration)+phasekey+str(self.index)

        def getstatus(self):
            for event in reversed(self.events):
                if hasattr(event, "statusMessage"):
                        return event.statusMessage
            #else:
            return "unknown"

        def getlastnode(self):
            for event in reversed(self.events):
                if hasattr(event, "statusMessage"):
                    if hasattr(event, "node"):
                        return event.node
                    else:
                        return None

        def getduration(self):
            tend = -1
            tstart = -1
            successnode = -1

            if self.getstatus() == "Model run complete":
                for event in reversed(self.events):
                    if hasattr(event, "type"):
                        if event.type == "RunCompletion":
                            tend = event.timestamp
                            successnode = event.node
                        if event.type == "RunCommencement" and event.node == successnode:
                            tstart = event.timestamp

                if tstart != -1:
                    return tend - tstart

            else:
                return None

        def getcompletionnode(self):
            if self.getstatus() == "Model run complete":
                for event in reversed(self.events):
                    if hasattr(event, "type"):
                        if event.type == "RunCompletion":
                            return event.node
            else:
                return None

    class Server:
        def __init__(self, hostname):
            self.hostname = hostname

    class Iteration:
        def __init__(self, index):
            self.index = index
            self.phases = []
            self.runs = {}

        def registerRun(self, run):
            self.runs[run.run] = run

    class Phase:
        def __init__(self, type):
            self.type = type
            self.runs = {}

    def __init__(self, filename):

        self.filemodtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        self.filecrttime = datetime.datetime.fromtimestamp(os.path.getctime(filename))

        self.load(filename)
        self.searchnewnodes(self.events, self.nodes)
        self.searchnewservers(self.nodes, self.servers)
        self.searchnewruns(self.events, self.runs)
        self.registerevents(self.events, self.nodes, self.runs)
        self.registerruns(self.runs, self.nodes)

    def load(self, filename):
        self.events.clear()
        self.runs.clear()
        self.nodes.clear()
        self.servers.clear()
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

        if len(self.iterations) > 0:
            currentIteration = self.iterations[-1].index
            if len(self.iterations[-1].phases) > 0:
                currentPhase = self.iterations[-1].phases[-1]
            else: currentPhase = "None"
        else:
            currentIteration = -1
            currentPhase = "None"

        if "RUNNING MODEL WITH INITIAL PARAMETER VALUE" in line:
            self.events.append(self.Events.NewIterationEvent(line.lower(), None, 0))
            self.iterations = [(self.Iteration(1))]
            self.events.append(self.Events.StartJacobianEvent(line, self.iterations[-1].index))
            self.iterations[-1].phases.append(self.Phase("Derivative Calculation"))
            return

        if "OPTIMISATION ITERATION NO." in line:
            iterationindex = int(line.split()[-2])
            self.events.append(self.Events.NewIterationEvent(line.lower(), None, iterationindex))
            if iterationindex != 1:
                self.iterations.append(self.Iteration(iterationindex))
            return

        if 'Calculating Jacobian matrix: running model' in line:
            self.events.append(self.Events.StartJacobianEvent(line, currentIteration))
            self.iterations[-1].phases.append(self.Phase("Derivative Calculation"))
            return

        if 'Testing parameter upgrades .....' in line:
            self.events.append(self.Events.ParameterUpgradeEvent(line, currentIteration))
            self.iterations[-1].phases.append(self.Phase("Parameter Upgrade"))
            return

        if 'RUNNING MODEL ONE LAST TIME WITH BEST PARAMETERS' in line:
            self.events.append(self.Events.LastModelRunEvent(line, currentIteration))
            self.iterations[-1].phases.append(self.Phase("Running Final Model"))
            return


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
            iteration = self.iterations[-1].index
            phase = self.iterations[-1].phases[-1].type
            self.events.append(self.Events.RunCommencementEvent(line,
                                                                timestamp,
                                                                w[9].strip('.'),
                                                                w[5],
                                                                currentIteration,
                                                                currentPhase))
            return

        if ("communications failure on node " in line) and ("will be re-assigned to another node." in line):
            timestamp = parsetime(line)
            w = line.split()
            iteration = self.iterations[-1].index
            self.events.append(self.Events.CommunicationFailureEvent(line,
                                                                     timestamp,
                                                                     w[7].strip(';'),
                                                                     w[10],
                                                                     currentIteration,
                                                                     currentPhase)
                               )
            return
        #TODO: iteration number must be implemented for all relevant results!

        if " completed on node " in line:
            timestamp = parsetime(line)
            w = line.split()
            if "old run so results not needed" in line:
                self.events.append(self.Events.LateCompletionEvent(messagetext=line,
                                                                   timestamp=timestamp,
                                                                   nodeindex=w[8].strip(';'),
                                                                   runindex=None,
                                                                   iterationindex=currentIteration,
                                                                   phase=currentPhase))
            else:
                self.events.append(self.Events.RunCompletionEvent(line,
                                                                  timestamp,
                                                                  w[9].strip('.'),
                                                                  w[5],
                                                                  currentIteration,
                                                                  currentPhase))
                self.iterations[-1].registerRun(self.events[-1])
            return

        if (" overdue run on node " in line) and ("may be re-assigned to another node." in line):
            timestamp = parsetime(line)
            w = line.split()
            self.events.append(self.Events.OverdueRunEvent(line,
                                                           timestamp,
                                                           w[7].strip(';'),
                                                           w[10],
                                                           currentIteration,
                                                           currentPhase))
            return

        if ("- model run failure on node " in line) and ("will attempt model run " in line):
            timestamp = parsetime(line)
            w = line.split()
            self.events.append(self.Events.RunFailureEvent(line,
                                                           timestamp,
                                                           w[8].strip(';'),
                                                           w[13],
                                                           currentIteration,
                                                           currentPhase)
                               )
            return



        #else
        if len(line.strip()) > 0:
            self.events.append(self.Events.GeneralEvent(line))

    def searchnewnodes(self, eventlist, nodelist):
        for e in eventlist:
            if e.type == "Assignment":
                if e.node not in nodelist.keys():
                    nodelist[e.node] = self.Node(e.node, e.workdir)

    def searchnewservers(self, nodelist, serverlist):
        for n in nodelist:
            hostname = nodelist[n].hostname
            if hostname not in serverlist.keys():
                serverlist[hostname] = self.Server(hostname)

    def searchnewruns(self, eventlist, runlist):
        for e in eventlist:
            if hasattr(e, "run"):
                phasekey = e.phase.type[0]
                key = str(e.iteration)+phasekey+str(e.run)
                if key not in runlist.keys():
                    runlist[str(e.iteration)+phasekey+str(e.run)] = self.Run(e.run, e.iteration, e.phase)

    def registerevents(self, eventlist, nodelist, runlist):
        for e in self.events:
            if hasattr(e, 'node'):
                self.nodes[e.node].events.append(e)
            if hasattr(e, 'run'):
                it = e.iteration
                phasekey = e.phase.type[0]
                self.runs[str(it)+phasekey+str(e.run)].events.append(e)

    def registerruns(self, runlist, nodelist):
        for runkey in runlist:
            run = runlist[runkey]
            #register run to completion node
            node = run.getcompletionnode()
            if node:
                nodelist[node].runs.append(run)
            #register run to phase
            phase = run.phase
            phase.runs[runkey] = run


    def getnumberofcompletedruns(self):
        nn = 0
        for n in self.nodes:
            node = self.nodes[n]
            nn += len(node.getsuccesfulruns())
        return nn

    def getaverageruntime(self):
        n = 0
        T = datetime.timedelta()
        for n in self.nodes:
            t = self.nodes[n].getaverageruntime()
            if t is not None:
                T += t
                n += 1
        return T/n

    def getrunsperhour(self):
        Tau = 0.
        for n in self.nodes:
            t = self.nodes[n].getaverageruntime()
            if t is not None:
                Tau += datetime.timedelta(hours=1) / t
        return Tau