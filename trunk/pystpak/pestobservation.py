__author__ = 'are'

from . import PestDef

class PestObservation:
    def __init__(self,name,value, weight, group):
        pd = PestDef()
        self.name = name
        self.value = value
        self.weight = weight
        self.group = group