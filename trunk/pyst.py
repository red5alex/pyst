__author__ = 'are'
import math

class PestObservationGroup:
    def __init__(self,OBGNME, GTARG = float('nan'), COVFLE = ""):
        pd = PestDefinitions()

        self.OBGNME = pd.pestcast("OBGNME",OBGNME)

        if not math.isnan(GTARG):
            self.GTARG = pd.pestcast("GTARG",GTARG)

        if COVFLE != "":
            self.COVFLE = pd.pestcast("COVFLE",COVFLE)

class PestObservation:
    def __init__(self,name,value, weight, group):
        pd = PestDefinitions()
        self.name = name
        self.value = value
        self.weight = weight
        self.group = group

class PestParameterGroup:
    def __init__(self,PARGPNME, INCTYP, DERINC, DERINCLB, FORCEN, DERINCMUL, DERMTHD, SPLITTHRESH=float('nan'), SPLITRELDIFF=float('nan'), SPLITACTION=""):
        pd = PestDefinitions()

        self.PARGPNME = pd.pestcast("PARGPNME",PARGPNME)
        self.INCTYP = pd.pestcast("INCTYP",INCTYP)
        self.DERINC = pd.pestcast("DERINC",DERINC)
        self.DERINCLB = pd.pestcast("DERINCLB",DERINCLB)
        self.FORCEN = pd.pestcast("FORCEN",FORCEN)
        self.DERINCMUL = pd.pestcast("DERINCMUL",DERINCMUL)
        self.DERMTHD = pd.pestcast("DERMTHD",DERMTHD)

        if not math.isnan(SPLITTHRESH):
            self.SPLITTHRESH = pd.pestcast("SPLITTHRESH",SPLITTHRESH)
            self.SPLITRELDIFF = pd.pestcast("SPLITRELDIFF",SPLITRELDIFF)
            self.SPLITACTION = pd.pestcast("SPLITACTION",SPLITACTION)

        # TODO: This would be generalized code, but eval does not work ...
        # for v in ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM']:
        #    command = 'self.'+v+' = pd.pestcast("'+v+'",'+v+')'
        #    eval(command)
        #
        # example for command with v = PARNME:
        # self.PARNME = pd.pestcast("PARNME",PARNME)

class PestParameter:
    def __init__(self,PARNME, PARTRANS, PARCHGLIM, PARVAL1, PARLBND, PARUBND, PARGP, SCALE, OFFSET, DERCOM):
        pd = PestDefinitions()

        self.PARNME = pd.pestcast("PARNME",PARNME)
        self.PARTRANS = pd.pestcast("PARTRANS",PARTRANS)
        self.PARCHGLIM = pd.pestcast("PARCHGLIM",PARCHGLIM)
        self.PARVAL1 = pd.pestcast("PARVAL1",PARVAL1)
        self.PARLBND = pd.pestcast("PARLBND",PARLBND)
        self.PARUBND = pd.pestcast("PARUBND",PARUBND)
        self.PARGP = pd.pestcast("PARGP",PARGP)
        self.SCALE = pd.pestcast("SCALE",SCALE)
        self.OFFSET = pd.pestcast("OFFSET",OFFSET)
        self.DERCOM = pd.pestcast("DERCOM",DERCOM)

        # TODO: This would be generalized code, but eval does not work ...
        # for v in ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM']:
        #    command = 'self.'+v+' = pd.pestcast("'+v+'",'+v+')'
        #    eval(command)
        #
        # example for command with v = PARNME:
        # self.PARNME = pd.pestcast("PARNME",PARNME)

class PestVariable:
    name = ''
    type = ''
    value = ''
    description = ''
    section = ''

    def __init__(self, name, type, values, description, section):
        self.name = name
        self.type = type
        self.value = values
        self.description = description
        self.section = section

class BlockFile:

    class fileBlock:
        name = ""
        content = []
        def __init__(self,name = ""):
            self.name = name
            self.content = []

    fileHeader = []
    fileBlocks = []
    fileBlocksDict = {}

    def _loadblocks(self,lines):
        self.fileHeader = []
        self.fileBlocks = []
        bname = "__header__"
        for line in lines:
            if line[0] == "*":
                bname = line.strip("*").strip()
                self.fileBlocks.append(self.fileBlock(bname)) #add a new block
                continue

            if bname == "__header__":
                #add the line to the fileHeader
                self.fileHeader.append(line.strip())
            else:
                #add the line to the content of the last (current) block
                self.fileBlocks[-1].content.append(line.strip())

    def _createBlockDict(self):
        self.fileBlocksDict = {}

        for block in self.fileBlocks:
            if block.name in self.fileBlocksDict == "multiple instances!":
                continue

            if block.name in self.fileBlocksDict:
                self.fileBlocksDict[block.name] = "multiple instances!"
            else:
                self.fileBlocksDict[block.name] = block

    def __init__(self,filename):
        bfile = open(filename)
        lines = bfile.readlines()
        bfile.close()
        self._loadblocks(lines)
        self._createBlockDict()

class PestDefinitions:
    """This object is a kind of database that contains information about the definition of different
    entities in PEST.
    Members:
    - pestVariables:        Dictionary containing information about variables used in PEST; includes
                            name, type, a description, allowed values and the location where it is stored.
                            Example: PestDefinitions.pestVariables['NPAR'] = "number of parameters".
    - fileFormatsTemplates: Dictionary containing the contents of file templates, e.g. of the pst file format

    """

    pestVariables = {}
    fileFormatTemplates = {}
    fileFormatTemplatesBlocks = {}

    def loadVarDef(self,filename):
        descFile = open(filename)
        section = descFile.readline().strip()
        descFile.readline() #jump table header
        lines = descFile.readlines() #read all other
        for line in lines:
            name, type, value, description = line.split('\t')
            self.pestVariables[name] = PestVariable(name, type, value, description.strip(), section)
        descFile.close()

    def loadFileFormatTemplate(self, filename):
        defFile = open(filename)
        extension = filename.split('.')[0]
        lines = defFile.readlines()
        self.fileFormatTemplates[extension] = [item.strip() for item in lines]
        defFile.close()

    def loadBlockFileFormatTemplate(self, filename):
        extension = filename.split('.')[0]
        self.fileFormatTemplatesBlocks[extension] = BlockFile(filename)

    def __init__(self):

        # load variable definitions
        listOfVarDefFiles = [ 'controlData.vardef.txt',
                            'parameterData.vardef.txt',
                            'observationData.vardef.txt',
                            'parameterGroupData.vardef.txt',
                            'observationGroupData.vardef.txt']
        for VarDefFile in listOfVarDefFiles:
            self.loadVarDef(VarDefFile)

        # load file definitions of block-type file formats
        self.loadBlockFileFormatTemplate('pst.fileDef.txt')

    def pestcast(self,varName,value):
            varType = self.pestVariables[varName].type
            if varType == 'text':
                return value
            if varType == 'integer':
                return int(value)
            if varType == 'real':
                return float(value)

class PestCtrlFile(BlockFile):

    vars = {}        #dictionary of variables
    obs = {}         #dictionary of observations
    obsGroups = {}   #dictionary of observations groups
    params = {}      #dictionary of parameters
    paramGroups = {} #dictionary of parameter groups

    _pstDefInfo = PestDefinitions()

    def __init__(self,filename):
        BlockFile.__init__(self,filename)
        self.loadControlData()
        self.loadParamGroups()
        self.loadParams()
        self.loadObservationGroups()
        self.loadObs()

    def loadControlData(self):

        # this reads the values from the pst control file and automatically
        # assigns them to the correct variable name in the correct type (both using the information stored in the
        # _pstDefInfo object

        data = self.fileBlocksDict["control data"].content
        template = self._pstDefInfo.fileFormatTemplatesBlocks['pst'].fileBlocksDict['control data'].content

        for data_line in data:
            template_line = template[data.index(data_line)]

            values = data_line.split()
            names  = template_line.split()

            for value in values:
                index =  values.index(value)
                name = names[index].strip('[]')
                self.vars[name] = self._pstDefInfo.pestcast(name,value) #

    def loadObservationGroups(self):
        for line in self.fileBlocksDict["observation groups"].content:
            words = line.split()
            name = words[0]
            self.obsGroups[name] = PestObservationGroup(*words)

    def loadObs(self):
        for line in self.fileBlocksDict["observation data"].content:
            name, value, weight, group = line.split()
            self.obs[name] = PestObservation(name,float(value), float(weight), group)

    def loadParams(self):
        for line in self.fileBlocksDict["parameter data"].content:
            words = line.split()
            name = words[0]
            self.params[name] = PestParameter(*words)

    def loadParamGroups(self):
        for line in self.fileBlocksDict["parameter groups"].content:
            words = line.split()
            name = words[0]
            self.paramGroups[name] = PestParameterGroup(*words)

class JacTestResultsFile:
    paramValues = []
    obsValues = {}
    def __init__(self,filename):
        self.load(filename)

    def load(self,filename):
        obsfile = open(filename)
        #import observations
        line = obsfile.readline(); #header
        null, *self.paramValues = line.split() #
        self.paramValues = list(map(float, self.paramValues)) #convert to float


        #process lines
        lines = obsfile.readlines()
        obsfile.close()
        for line in lines:
            #add observations to observations list
            obs_name, *obs_values = line.split()
            obs_values = list(map(float, obs_values)) #convert to float
            self.obsValues[obs_name] = obs_values

    def calcSlopes(self):
        slopes = {}
        for ob in self.obsValues:
            ov = self.obsValues[ob]
            slopes[ob] = []
            for v in ov:
                i = ov.index(v)
                if i == len(ov)-1:
                    pass #
                else:
                   o1 = v
                   o2 = ov[i+1]
                   p1 = self.paramValues[i]
                   p2 = self.paramValues[i+1]
                   slope = (o2 - o1) / (p2 - p1)
                   slopes[ob].append(slope) # append the slope to the list

        return slopes

class ParamValueFile:

    class Param:
        name = ""
        value = float
        scale = 1.0
        offset = 0.0
        def __init__(self,name,value,scale = 1.0, offset=0.0):
            self.name = name
            self.value = value
            self.scale = scale
            self.offset = offset

    precis = 'single'
    dpoint = 'point'
    params = []

    def __init__(self, precis = 'single', dpoint = 'point'):
        self.precis = precis
        self.dpoint = dpoint
        params = []

    def addPar(self,name,value,scale=1.0,offset=0.0):
        self.params.append(self.Param(name,value,scale,offset))

    def write(self, filename):
        outfile = open(filename,"w")
        outfile.write(self.precis + ' ' + self.dpoint + '\n' )
        for p in self.params:
            outfile.write(p.name + ' ' +
                          str(p.value)+ ' ' +
                          str(p.scale)+ ' ' +
                          str(p.offset)+'\n')
        outfile.close()

class RunRecordFile:

    class ParameterSet:
        id = -1
        sourcefile = ".par" #the filename of the pst file
        parVals =   {}      #dict of parameter values (key -> parNames list)
        obsVals =   {}      #dict of observation values (key ->obsNames list)
        phi =       -1.     #total objective function of this run
        phiObsGroup = {}      #list of obsgroup objective functions of this run

    pstctrlfile = ""
    parNames    = []  #list of parameters
    obsNames    = []  #list of observations
    obsGrpNames = []  #list of observation group names
    parGrpNames = []  #list of parameter group names
    paramSets   = []  #list of Parameter Set objections

    def parsefrom(self,filename):
        rrffile = open(filename)

        #skip line 1, read pest control file name from line 2
        line = rrffile.readline()
        line = rrffile.readline()
        self.pstctrlfile = line.strip('"\n')

        #advance to section parameter group names
        while not "* parameter group names" in line:
            line = rrffile.readline()

        #parse parameter group names until next section (parameter names) is reached
        line = rrffile.readline() #skip section header
        while not "* parameter names" in line:
            self.parGrpNames.append(line.strip())
            line = rrffile.readline()

        #parse parameter names until next section (observation group names) is reached
        line = rrffile.readline() #skip section header
        while not "* observation group names" in line:
            self.parNames.append(line.strip())
            line = rrffile.readline()

        #parse observation group names until next section (observation names) is reached
        line = rrffile.readline() #skip section header
        while not "* observation names" in line:
            self.obsGrpNames.append(line.strip())
            line = rrffile.readline()

        #parse observation names until next section (first parameter set index) is reached
        line = rrffile.readline() #skip section header
        while not "* parameter set index" in line:
            self.obsNames.append(line.strip())
            line = rrffile.readline()

        #TODO: write the parser for parameter sets!

        while line != "": #run until a blank line or the end of file is found

            if "* parameter set index" in line:
                # read parameter index
                self.paramSets.append(self.ParameterSet())
                line = rrffile.readline() #advance one line
                self.paramSets[-1].id = int(line.strip()) # read index

                # read parameter source name
                line = rrffile.readline()
                line = rrffile.readline() #read parameter value source
                self.paramSets[-1].sourcefile = line.strip()

            # read PARAMETERS values list:

                # read all lines of section:
                line = rrffile.readline() # skip parameter values section header
                lines = []
                line = rrffile.readline()
                while not "* model output values" in line:
                    lines.append(line)
                    line = rrffile.readline()

                # process the lines, store values in object
                for l in lines:
                    index = lines.index(l)
                    name = self.parNames[index]
                    self.paramSets[-1].parVals[name] = float(l.strip())


            # read OBSERVATIONS values list:

                # read all lines of section:
                lines = []
                line = rrffile.readline()
                while not "* total objective function" in line:
                    lines.append(line)
                    line = rrffile.readline()

                # process the lines, store values in object
                for l in lines:
                    index = lines.index(l)
                    name = self.obsNames[index]
                    self.paramSets[-1].obsVals[name] = float(l.strip())


            # read total objective function
                line = rrffile.readline()
                self.paramSets[-1].phi = float(line.strip())

            # read OBSERVATIONS values list:

                line = rrffile.readline()
                # read all lines of section:
                lines = []
                line = rrffile.readline()
                while not "* parameter set index" in line:
                    lines.append(line)
                    line = rrffile.readline()

                # process the lines, store values in object
                for l in lines:
                    index = lines.index(l)
                    name = self.obsGrpNames[index]
                    self.paramSets[-1].phiObsGroup[name] = float(l.strip())

            line = rrffile.readline()

        rrffile.close()