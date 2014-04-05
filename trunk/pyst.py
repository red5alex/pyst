__author__ = 'are'

class Observation:
    def __init__(self,name,value, weight, group):
        self.name = name
        self.value = value
        self.weight = weight
        self.group = group

class PestCtrlFile:
    obs = {}

    def __init__(self):
        pass

    def __init__(self,filename):
        self.load(filename)

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
        null, *self.paramValues = line.split()
        self.paramValues = list(map(float, self.paramValues)) #convert to float


        #process lines
        #line = obsfile.readline()
        lines = obsfile.readlines()
        obsfile.close()
        for line in lines:
            #add observations to observations list
            obs_name, *obs_values = line.split()
            obs_values = list(map(float, obs_values)) #convert to float
            self.obsValues[obs_name] = obs_values
