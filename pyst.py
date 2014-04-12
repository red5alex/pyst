__author__ = 'are'

class Observation:
    def __init__(self,name,value, weight, group):
        self.name = name
        self.value = value
        self.weight = weight
        self.group = group

class _pestVariable:
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
            self.pestVariables[name] = _pestVariable(name, type, value, description.strip(), section)
        descFile.close()

    def loadFileFormatTemplate(self, filename):
        defFile = open(filename)
        extension = filename.split('.')[0]
        lines = defFile.readlines()
        self.fileFormatTemplates[extension] = [item.strip() for item in lines]
        defFile.close()

    def __init__(self):
        pestVariables = {}
        self.loadVarDef('controlData.vardef.txt')
        self.loadFileFormatTemplate('pst.fileDef.txt')


class PestCtrlFile:
    _pstDefInfo = PestDefinitions()
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
                type = _pstDefInfo.pestVariables[name].type
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

    #TODO: subdivide the whole string list in sections, and make these accesible through a disctionary


   # load control data
    def load(self,filename):
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
            self.obs[name] = Observation(name,float(value), float(weight), group)
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


