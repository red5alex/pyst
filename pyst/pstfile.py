__author__ = 'are'

from . import BlockFile
from . import PestDef as PestDefinitions
from . import PestObservationGroup, PestObservation, PestParameter, PestParameterGroup


class PestCtrlFile(BlockFile):
    vars = {}  # dictionary of variables
    obs = {}  # dictionary of observations
    obsGroups = {}  # dictionary of observations groups
    params = {}  # dictionary of parameters
    paramGroups = {}  # dictionary of parameter groups

    _pstDefInfo = PestDefinitions()

    def __init__(self, filename):
        BlockFile.__init__(self, filename)
        self.loadControlData()
        self.loadParamGroups()
        self.loadParams()
        self.loadObservationGroups()
        self.loadObs()

    def loadControlData(self):

        # this reads the values from the pst control file and automatically
        # assigns them to the correct variable name in the correct type (both using the information stored in the
        # _pstDefInfo object

        data = self.fileBlocksDict["control data"].content
        template = self._pstDefInfo.fileFormatTemplatesBlocks['pst'].fileBlocksDict['control data'].content

        for data_line in data:
            template_line = template[data.index(data_line)]

            values = data_line.split()
            names = template_line.split()

            for value in values:
                index = values.index(value)
                name = names[index].strip('[]')
                self.vars[name] = self._pstDefInfo.pestcast(name, value)

    def loadObservationGroups(self):
        for line in self.fileBlocksDict["observation groups"].content:
            words = line.split()
            name = words[0]
            self.obsGroups[name] = PestObservationGroup(*words)

    def loadObs(self):
        for line in self.fileBlocksDict["observation data"].content:
            name, value, weight, group = line.split()
            self.obs[name] = PestObservation(name, float(value), float(weight), group)

    def loadParams(self):
        for line in self.fileBlocksDict["parameter data"].content:
            words = line.split()
            name = words[0]
            if len(words) == 10:
                self.params[name.lower()] = PestParameter(*words)
            else:
                pass  # TODO: read parameter tying relationships here

    def loadParamGroups(self):
        for line in self.fileBlocksDict["parameter groups"].content:
            words = line.split()
            name = words[0]
            self.paramGroups[name] = PestParameterGroup(*words)
