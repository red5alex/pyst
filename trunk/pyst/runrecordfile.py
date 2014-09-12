__author__ = 'are'

#TODO: should be reimplemented as a blockfile subclass

import copy


class RunRecordFile:

    class ParameterSet:
        id = -1
        sourcefile = ".par"  # the filename of the pst file
        parVals = {}  # dict of parameter values (key -> parNames list)
        obsVals = {}  # dict of observation values (key ->obsNames list)
        phi = -1.  # total objective function of this run
        phiObsGroup = {}  # list of obsgroup objective functions of this run

        def __deepcopy__(self, memo):
            newSet = copy.copy(self)
            newSet.parVals = copy.deepcopy(self.parVals)
            newSet.obsVals = copy.deepcopy(self.obsVals)
            newSet.phiObsGroup = copy.deepcopy(self.phiObsGroup)
            return newSet

    pstctrlfile = ""
    parNames = []  # list of parameters
    obsNames = []  # list of observations
    obsGrpNames = []  # list of observation group names
    parGrpNames = []  # list of parameter group names
    paramSets = []  # list of Parameter Set objections

    def parsefrom(self, filename):
        global index
        rrffile = open(filename)

        #skip line 1, read pest control file name from line 2
        line = rrffile.readline()
        line = rrffile.readline()
        self.pstctrlfile = line.strip('"\n')

        protoset = self.ParameterSet()

        #advance to section parameter group names
        while not "* parameter group names" in line:
            line = rrffile.readline()

        #parse parameter group names until next section (parameter names) is reached
        line = rrffile.readline()  # skip section header
        while not "* parameter names" in line:
            self.parGrpNames.append(line.strip())
            line = rrffile.readline()

        #parse parameter names until next section (observation group names) is reached
        line = rrffile.readline()  # skip section header
        while not "* observation group names" in line:
            self.parNames.append(line.strip())
            line = rrffile.readline()

        #parse observation group names until next section (observation names) is reached
        line = rrffile.readline()  # skip section header
        while not "* observation names" in line:
            self.obsGrpNames.append(line.strip())
            line = rrffile.readline()

        #parse observation names until next section (first parameter set index) is reached
        line = rrffile.readline()  # skip section header
        while not "* parameter set index" in line:
            self.obsNames.append(line.strip())
            line = rrffile.readline()

        while line != "":  # run until a blank line or the end of file is found

            if "* parameter set index" in line:
                # read parameter index

                newParamSet = copy.deepcopy(protoset)

                self.paramSets.append(newParamSet)
                line = rrffile.readline()  # advance one line
                self.paramSets[-1].id = int(line.strip())  # read index

                # read parameter source name
                line = rrffile.readline()
                line = rrffile.readline()  # read parameter value source
                self.paramSets[-1].sourcefile = line.strip()

            # read PARAMETERS values list:

                # read all lines of section:
                line = rrffile.readline()  # skip parameter values section header
                lines = []
                line = rrffile.readline()
                while not "* model output values" in line:
                    lines.append(copy.copy(line))
                    line = rrffile.readline()

                # process the lines, store values in object
                index = 0
                for l in lines:
                    name = self.parNames[index]
                    self.paramSets[-1].parVals[name] = float(l.strip())
                    index += 1

            # read OBSERVATIONS values list:

                # read all lines of section:
                lines = []
                line = rrffile.readline()
                while not "* total objective function" in line:
                    lines.append(line)
                    line = rrffile.readline()

                # process the lines, store values in object
                index = 0
                for l in lines:
                    #index = lines.index(l)
                    name = self.obsNames[index]
                    self.paramSets[-1].obsVals[name] = float(l.strip())
                    index += 1

            # read total objective function
                line = rrffile.readline()
                self.paramSets[-1].phi = float(line.strip())

            # read OBSERVATIONS values list:

                line = rrffile.readline()
                # read all lines of section:
                lines = []
                line = rrffile.readline()
                while not ("* parameter set index" in line or line == ""):
                    lines.append(line)
                    line = rrffile.readline()

                # process the lines, store values in object
                for l in lines:
                    index = lines.index(l)
                    name = self.obsGrpNames[index]
                    self.paramSets[-1].phiObsGroup[name] = float(l.strip())

            #line = rrffile.readline()

        rrffile.close()

    def __init__(self,filename):
        self.parsefrom(filename)

    def save(self, parname, filename, fileformat='dat'):
        if fileformat == 'dat':
            self.saveasjactest(parname, filename)
        else:
            raise ValueError('no support for fileformat "'+fileformat+'"')

    def saveasjactest(self, parname, filename):  # JACTESTRESULT
        outfile = open(filename, "w")
        #header
        outfile.write("param_value")
        for ps in self.paramSets:
            outfile.write("\t"+str(ps.parVals[parname]))
        outfile.write("\n")
        for obsname in self.obsNames:
            outfile.write(obsname)
            for ps in self.paramSets:
                outfile.write("\t"+str(ps.obsVals[obsname]))
            outfile.write("\n")

        outfile.close()

    def saveastable(self, filename):
        outfile = open(filename, "w")
        # header:
        outfile.write("RunID\tPhi")
        for pn in self.parNames:  # write parameters to header
            outfile.write("\t"+pn)
        for on in self.obsNames:  # write observations to header
            outfile.write("\t"+on)
        outfile.write("\n")  # close header

        for ps in self.paramSets:
            outfile.write(str(ps.id) + "\t" + str(ps.phi))  # ID and Objective function

            for pn in self.parNames:  # write parameters to header
                outfile.write("\t"+str(ps.parVals[pn]))
            for on in self.obsNames:  # write observations to header
                outfile.write("\t"+str(ps.obsVals[on]))
            outfile.write("\n")

        outfile.close()