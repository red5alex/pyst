__author__ = 'are'

class SenFile:
    parhistory = {}
    senhistory = {}
    groups = []
    membership = {}
    case = None

    def __init__(self, filename):
        self.parsefrom(filename)

    def parsefrom(self,filename):

        iterationnumber = 0
        self.parhistory = {}
        self.senhistory = {}
        self.groups = []
        self.membership = {}
        self.case = None
        
        f = open(filename)

        # evaluate first line (contains the case name)
        l = f.readline()
        if "PARAMETER SENSITIVITIES:" not in l:
            raise EOFError("Seems not to be a PEST sensitivities file")
        self.case = l.split()[3]

        lines = f.readlines()
        f.close()

        parvals = {}
        senvals = {}


        for l in lines:

            if "COMPLETION OF OPTIMISATION PROCESS" in l:
                break

            if "OPTIMISATION ITERATION NO." in l:
                if iterationnumber > 0:
                    self.parhistory[iterationnumber] = parvals  # save current list of parameter values
                    self.senhistory[iterationnumber] = senvals  # save current list of sensitivity values
                    parvals = {}  # reset list of parameter values
                    senvals = {}  # reset list of sensitivity values
                iterationnumber = int(l.split()[3])  # read new iteration number
                continue

            if "Parameter name" in l:
                continue

            if len(l.split()) == 4:
                words = l.split()
                par = words[0]
                group = words[1]
                value = float(words[2])
                sen = float(words[3])
                parvals[par] = value
                senvals[par] = sen
                if group not in self.groups:
                    self.groups.append(group)
                self.membership[par] = group
                continue

        self.parhistory[iterationnumber] = parvals  # save last current list of parameter values
        self.senhistory[iterationnumber] = senvals  # save last current list of sensitivity values

    def getparamaternames(self):
        return self.parhistory[1].keys()

    def getnumberofiterations(self):
        return len(self.parhistory)