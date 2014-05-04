__author__ = 'are'

from . import FePestObservation, FePestTimeSeries

class FePestObsTable:
    obs = {}
    ts = {}
    def __init__(self,filename):
        self.load(filename)

    def load(self,filename):
        obsfile = open(filename)
        #import observations
        obsfile.readline()  # jump over header
        #process lines
        #line = obsfile.readline()
        lines = obsfile.readlines()
        obsfile.close()
        for line in lines:
            #add observations to observations list
            if line.__len__() > 0 and line[0] != "*":
                obsdef, type, obspoint, X, Y, Z, slice, active, name, time, value, weight, group, sync = line.split()
                self.obs[name] = FePestObservation()
                self.obs[name].obsdef = obsdef
                self.obs[name].type = type
                self.obs[name].obspoint = obspoint
                self.obs[name].X = float(X)
                self.obs[name].Y = float(Y)
                self.obs[name].Z = float(Z)
                self.obs[name].slice = int(slice)
                self.obs[name].active = bool(active)
                self.obs[name].name = name
                self.obs[name].time = float(time)
                self.obs[name].value =float(value)
                self.obs[name].weight = float(weight)
                self.obs[name].group = group
                self.obs[name].sync = bool(sync)

                #add observations to time-series list:
                if obspoint not in self.ts:
                    self.ts[obspoint] = FePestTimeSeries(obspoint)
                    self.ts[obspoint].obsNames = []
                    self.ts[obspoint].obs = []
                self.ts[obspoint].obsNames.append(name)
                self.ts[obspoint].obs.append(self.obs[name])
        #sort all ts-lists by time
        for i in self.ts:
            self.ts[i].obs.sort(key=lambda obs: obs.time)