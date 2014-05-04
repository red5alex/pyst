__author__ = 'are'


class JacTestResultsFile:
    paramValues = []
    obsValues = {}

    def __init__(self, filename):
        self.load(filename)

    def load(self,filename):
        obsfile = open(filename)
        #import observations
        line = obsfile.readline()  # header

        self.paramValues = line.split()  # load all entries
        self.paramValues.pop(0)  # remove first word of line (not a parameter value)
        self.paramValues = list(map(float, self.paramValues))  # convert str to float

        #process lines
        lines = obsfile.readlines()
        obsfile.close()
        for line in lines:
            #add observations to observations list

            obs_values = line.split()  # load all entries
            obs_name = obs_values.pop(0)  # remove first word of line (not an observation value)
            obs_values = list(map(float, obs_values))  # convert to float
            self.obsValues[obs_name] = obs_values

    #TODO: test implementation of the class in JACTEST postprocessing (after relocation to package)
    def calcSlopes(self):
        slopes = {}
        for ob in self.obsValues:
            ov = self.obsValues[ob]
            slopes[ob] = []
            for v in ov:
                i = ov.index(v)
                if i == len(ov)-1:
                    pass
                else:
                    o1 = v
                    o2 = ov[i+1]
                    p1 = self.paramValues[i]
                    p2 = self.paramValues[i+1]
                    slope = (o2 - o1) / (p2 - p1)
                    slopes[ob].append(slope)  # append the slope to the list

        return slopes