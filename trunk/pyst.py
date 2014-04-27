__author__ = 'are'

class PestObservation:
    def __init__(self,name,value, weight, group):
        self.name = name
        self.value = value
        self.weight = weight
        self.group = group

class PestParameter:
    def __init__(self,name,value, weight, group):
        pass

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

    def __init__(self):
        self.loadVarDef('controlData.vardef.txt')
        self.loadFileFormatTemplate('pst.fileDef.txt')

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

class PestCtrlFile(BlockFile):

    vars = {}   #dictionary of variables
    obs = {}    #dictionary of observations
    params = {} #dictionary of observations

    _pstDefInfo = PestDefinitions()

    def __init__(self,filename):
        BlockFile.__init__(self,filename)
        self.loadObs()

    def loadObs(self):
        for line in self.fileBlocksDict["observation data"].content:
            name, value, weight, group = line.split()
            self.obs[name] = PestObservation(name,float(value), float(weight), group)

    def loadParams(self):
        for line in self.fileBlocksDict["observation data"].content:
            name, value, weight, group = line.split()
            self.obs[name] = PestObservation(name,float(value), float(weight), group)



class PestCtrlFile2:
    _pstDefInfo = PestDefinitions()
    blockNames = []
    blockContents = {}
    obs = {}
    ctd = {}
    def __init__(self):
        pass

    def __init__(self,filename):
        self.load(filename)

    def _parseWords(self,words,names,counts):
        if len(words) in counts:
            for word in words:
                name = names[words.index(word)].strip('[',']')
                type = self._pstDefInfo.pestVariables[name].type
                if type == 'text':
                    self.ctd[names] = word
                if type == 'integer':
                    self.ctd[names] = int(word)
                if type == 'real':
                    self.ctd[names] = float(word)
        else:
            print('wrong number of args found in line:')
            print(words)
            raise('wrong number of args')

    def loadBlocks(self,filename):
        pstfile = open(filename)
        currentBlock = ""
        for line in pstfile:
            if line[0] == "*":
                currentBlock = line.strip("*").strip()
                self.blockNames.append(currentBlock)
                self.blockContents[currentBlock] = []
                continue
            if currentBlock != "":
                self.blockContents[currentBlock].append(line)
                continue


    #TODO: use the above routine to read blocks first, then process them selectively



   # load control data
    def load(self,filename):

        self.loadBlocks(filename)

        pstfile = open(filename)
        #import
   #       self.ctd = {}
   #       while pstfile.readline() != "* control data\n":
   #            pass
   #
   #      controlDataStart = self._pstDefInfo.fileFormatTemplates['pst'].index('* control data')
   #
   #     #line 1
   #     names = ['RSTFLE','PESTMODE']
   #     types = ['str'   ,'str']
   #     counts = [2]
   #     words = pstfile.readline().split()
   #     self.parseWords(words,names,types,counts)
   #
   #     #line 2
   #     self.parseWords(pstfile.readline().split(),
   #                     "NPAR NOBS NPARGP NPRIOR NOBSGP [MAXCOMPDIM]".split(),
   #                     "int  int  int    int    int     int".split(),
   #                     [5,6])


   # load observation data
   # def load(self,filename):
   #     pstfile = open(filename)
        #import observations
        while pstfile.readline() != "* observation data\n":
            pass
        line = pstfile.readline()
        while line.__len__() > 0 and line[0] != "*":
            name, value, weight, group = line.split()
            self.obs[name] = PestObservation(name,float(value), float(weight), group)
            line = pstfile.readline()
        pstfile.close()

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