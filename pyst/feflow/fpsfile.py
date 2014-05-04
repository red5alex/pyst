__author__ = 'are'

import xml.parsers.expat as xmlp



class FpsFile:

    def __init__(self, filename):
        p = xmlp.ParserCreate()
        file = open("D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\testmodel\\FMG\\femdata\\Ore_D4.fps")
        lines = file.readlines()
        p.Parse(file)