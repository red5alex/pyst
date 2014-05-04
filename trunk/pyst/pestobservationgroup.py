__author__ = 'are'

import math
from . import PestDef

class PestObservationGroup:
    def __init__(self,OBGNME, GTARG = float('nan'), COVFLE = ""):
        pd = PestDef()

        self.OBGNME = pd.pestcast("OBGNME",OBGNME)

        if not math.isnan(GTARG):
            self.GTARG = pd.pestcast("GTARG",GTARG)

        if COVFLE != "":
            self.COVFLE = pd.pestcast("COVFLE",COVFLE)