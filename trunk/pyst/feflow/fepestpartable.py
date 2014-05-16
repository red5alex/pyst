__author__ = 'are'

from . import FePestObservation, FePestTimeSeries


class FePestParTable:
    par = {}

    class FePestParameter:
        pardef = ""
        type = ""
        zone = ""
        pilotpoint = -1
        active = False
        name = ""
        transform = ""
        tiedto = None
        changelimit = float('nan')
        initialvalue = float('nan')
        lowerbound	= float('nan')
        upperbound = float('nan')
        scale = float('nan')
        offset = float('nan')
        group = ''

    def __init__(self, filename):
        self.load(filename)

    def load(self,filename):
        partable = open(filename)
        partable.readline()  # jump over header
        lines = partable.readlines()  # read all other lines
        partable.close()
        for line in lines:
            #add parameter to parameters list
            if line.__len__() > 0 and line[0] != "*":
                words = line.split()
                transform = int(words[6])
                if transform == 3:  # includes a tied-to parameter
                    pardef, type, zone, pilotpoint, active, name, transform, tiedto, changelimit, \
                    initialvalue, lowerbound, upperbound, scale, offset, group = line.strip().split()
                else: #misses the tied-to parameter
                    pardef, type, zone, pilotpoint, active, name, transform, changelimit, \
                    initialvalue, lowerbound, upperbound, scale, offset, group = line.strip().split()

                self.par[name] = self.FePestParameter()
                self.par[name].pardef = pardef
                self.par[name].type = int(type)
                self.par[name].zone = type
                self.par[name].pilotpoint = int(pilotpoint)
                self.par[name].name = name
                self.par[name].transform = int(transform)
                if transform == 3:  # tied parameter
                    self.par[name].tiedto = tiedto
                self.par[name].changelimit = float(changelimit)
                self.par[name].initialvalue = float(initialvalue)
                self.par[name].lowerbound = float(lowerbound)
                self.par[name].upperbound = float(upperbound)
                self.par[name].scale = float(scale)
                self.par[name].offset = float(offset)
                self.par[name].group = group