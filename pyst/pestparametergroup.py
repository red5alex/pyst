__author__ = 'are'

from . import PestDef
import math


class PestParameterGroup:
    def __init__(self, PARGPNME, INCTYP, DERINC, DERINCLB, FORCEN, DERINCMUL, DERMTHD,
                 SPLITTHRESH=float('nan'), SPLITRELDIFF=float('nan'), SPLITACTION=""):
        pd = PestDef()

        self.PARGPNME = pd.pestcast("PARGPNME", PARGPNME)
        self.INCTYP = pd.pestcast("INCTYP", INCTYP)
        self.DERINC = pd.pestcast("DERINC", DERINC)
        self.DERINCLB = pd.pestcast("DERINCLB", DERINCLB)
        self.FORCEN = pd.pestcast("FORCEN", FORCEN)
        self.DERINCMUL = pd.pestcast("DERINCMUL", DERINCMUL)
        self.DERMTHD = pd.pestcast("DERMTHD", DERMTHD)

        if not math.isnan(SPLITTHRESH):
            self.SPLITTHRESH = pd.pestcast("SPLITTHRESH", SPLITTHRESH)
            self.SPLITRELDIFF = pd.pestcast("SPLITRELDIFF", SPLITRELDIFF)
            self.SPLITACTION = pd.pestcast("SPLITACTION", SPLITACTION)

        # TODO: This would be generalized code, but eval does not work ...
        # for v in ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM']:
        #    command = 'self.'+v+' = pd.pestcast("'+v+'",'+v+')'
        #    eval(command)
        #
        # examples for command with v = PARNME:
        # self.PARNME = pd.pestcast("PARNME",PARNME)