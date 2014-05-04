__author__ = 'are'

from . import PestDef

class PestParameter:
    def __init__(self,PARNME, PARTRANS, PARCHGLIM, PARVAL1, PARLBND, PARUBND, PARGP, SCALE, OFFSET, DERCOM):
        pd = PestDef()

        self.PARNME = pd.pestcast("PARNME",PARNME)
        self.PARTRANS = pd.pestcast("PARTRANS",PARTRANS)
        self.PARCHGLIM = pd.pestcast("PARCHGLIM",PARCHGLIM)
        self.PARVAL1 = pd.pestcast("PARVAL1",PARVAL1)
        self.PARLBND = pd.pestcast("PARLBND",PARLBND)
        self.PARUBND = pd.pestcast("PARUBND",PARUBND)
        self.PARGP = pd.pestcast("PARGP",PARGP)
        self.SCALE = pd.pestcast("SCALE",SCALE)
        self.OFFSET = pd.pestcast("OFFSET",OFFSET)
        self.DERCOM = pd.pestcast("DERCOM",DERCOM)

        # TODO: This would be generalized code, but eval does not work ...
        # for v in ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM']:
        #    command = 'self.'+v+' = pd.pestcast("'+v+'",'+v+')'
        #    eval(command)
        #
        # example for command with v = PARNME:
        # self.PARNME = pd.pestcast("PARNME",PARNME)