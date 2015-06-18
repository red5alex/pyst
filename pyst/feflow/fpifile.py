__author__ = 'are'

from pyst.feflow.fepestparameter import FePestParameter

class FpiFile:
    parnames = []
    par = {}

    def __init__(self, filename):
        self.filename = filename
        file = open(filename)
        lines = file.readlines()
        for line in lines:
            name, value = line.split()
            self.parnames.append(name)
            self.par[name] = FePestParameter()
            self.par[name].name = name
            self.par[name].value = float(value)
        file.close()

    def save(self, filename):
        outfile = open(filename, "w")
        for o in self.parnames:
            outfile.write(o+" "+self.par[o].value)
        outfile.close()