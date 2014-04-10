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
    pestVariables = {}

    def loadVarDef(self,filename):
        descFile = open(filename)
        section = descFile.readline().strip()
        descFile.readline() #jump table header
        lines = descFile.readlines() #read all other
        for line in lines:
            name, type, value, description = line.split('\t')
            self.pestVariables[name] = _pestVariable(name, type, value, description.strip(), section)
        descFile.close()

    def __init__(self):
        pestVariables = {}
        self.loadVarDef('controlData.vardef.txt')

class PestCtrlFile:
    obs = {}
    ctd = {}
    def __init__(self):
        pass

    def __init__(self,filename):
        self.load(filename)

    def parseWords(self,words,names,types,counts):
        if len(words) in counts:
            for word in words:
                name = names[words.index(word)].strip('[',']')
                if types[name] == 'str':
                    self.ctd[names] = word
                if types[name] == 'int':
                    self.ctd[names] = int(word)
                if types[name] == 'float':
                    self.ctd[names] = float(word)
        else:
            print('wrong number of args found in line:')
            print(words)
            raise('wrong number of args')

   # load control data
   # def load(self,filename):
   #     pstfile = open(filename)
   #     #import
   #     self.ctd = {}
   #     while pstfile.readline() != "* control data\n":
   #         pass
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
    def load(self,filename):
        pstfile = open(filename)
        #import observations
        while pstfile.readline() != "* observation data\n":
            pass
        line = pstfile.readline()
        while line.__len__() > 0 and line[0] != "*":
            name, value, weight, group = line.split()
            pstCtrl.obs[name] = Observation(name,float(value), float(weight), group)
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


