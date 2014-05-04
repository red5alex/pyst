__author__ = 'are'


class ParamValueFile:

    class Param:
        name = ""
        value = float
        scale = 1.0
        offset = 0.0

        def __init__(self, name, value, scale=1.0, offset=0.0):
            self.name = name
            self.value = value
            self.scale = scale
            self.offset = offset

    precis = 'single'
    dpoint = 'point'
    params = []

    def __init__(self, precis='single', dpoint='point'):
        self.precis = precis
        self.dpoint = dpoint
        self.params = []

    def addPar(self, name, value, scale=1.0, offset=0.0):
        self.params.append(self.Param(name, value, scale, offset))

    def write(self, filename):
        outfile = open(filename, "w")
        outfile.write(self.precis + ' ' + self.dpoint + '\n')
        for p in self.params:
            outfile.write(p.name + ' ' +
                          str(p.value) + ' ' +
                          str(p.scale) + ' ' +
                          str(p.offset) + '\n')
        outfile.close()