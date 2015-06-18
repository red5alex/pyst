__author__ = 'are'


# import xml.parsers.expat as xmlp

import xml.etree.ElementTree as ET

class FpsFile:

    def __init__(self, filename):
        """
        p = xmlp.ParserCreate()
        file = open(filename)
        lines = file.readlines()
        p.Parse(file)
        """
        tree = ET.parse(filename)
        root = tree.getroot()

        for child in root:
            print(child.tag, child.attrib)

        treeobject = obj



        pass