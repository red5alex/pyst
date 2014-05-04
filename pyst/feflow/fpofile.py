__author__ = 'are'

from pyst.feflow.fepestobservation import FePestObservation


class FpoFile:
    obsnames = []
    obs = {}

    def __init__(self, filename):
        self.filename = filename
        file = open(filename)
        lines = file.readlines()
        for line in lines:
            name, value = line.split()
            self.obsnames.append(name)
            self.obs[name] = FePestObservation()
            self.obs[name].name = name
            self.obs[name].value = float(value)
        file.close()

    def save(self, filename):
        outfile = open(filename, "w")
        for o in self.obsnames:
            outfile.write(o+" "+self.obs[o].value)
        outfile.close()
