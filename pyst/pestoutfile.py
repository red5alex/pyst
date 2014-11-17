__author__ = 'are'

class PestOutFile:

    class Iteration:

        def __init__(self, number):
            self.itNumber = number
            self.totalPhi = None
            self.currentRegFactor = None
            self.adjustedRegFactor = None
            self.startingPhis = {}.copy()
            self.adjustedPhis = {}.copy()

    Iterations = []
    obsGroups = []

    def __init__(self, filename):
        self.fileName = filename
        self.load(filename)

    def load(self, filename):

        file = open(filename)

        itObject0 = self.Iteration(0)
        self.Iterations.append(itObject0)
        regFactorType = "current"

        for l in file.readlines():

            if 'Current regularisation weight factor' in l:
                regFactorType = "current"
                text = l.replace("=",":")
                self.Iterations[-1].currentRegFactor = text.split(":")[1].strip()

            if 'Re-calculated regularisation weight factor' in l:
                regFactorType = "recalculated"
                text = l.replace("=",":")
                self.Iterations[-1].adjustedRegFactor = text.split(":")[1].strip()

            if 'Sum of squared weighted residuals (ie phi)' in l:
                self.Iterations[-1].totalPhi = l.split("=")[1].strip()

            if 'Contribution to phi from observation group' in l:
                text = l.replace("=", ":")
                groupName = text.split()[6].strip(":").strip("\"")
                groupPhi = float(text.split(":")[1])

                if regFactorType == "current":
                    self.Iterations[-1].startingPhis[groupName] = groupPhi
                if regFactorType == "recalculated":
                    self.Iterations[-1].adjustedPhis[groupName] = groupPhi

            if 'OPTIMISATION ITERATION NO.' in l:
                itNumber = l.split(':')[1].strip()
                ItObject = self.Iteration(itNumber)
                self.Iterations.append(ItObject)
                pass

        file.close()

    def getObsGroups(self):
        groups = []
        if len(self.Iterations) > 0:
            return self.Iterations[0].startingPhis.keys()
        return groups
