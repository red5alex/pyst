__author__ = 'are'

import os
from pyst.blockfile import BlockFile

class PestDef:
    """This object is a kind of database that contains information about the definition of different
    entities in PEST.
    Members:
    - pestVariables:        Dictionary containing information about variables used in PEST; includes
                            name, type, a description, allowed values and the location where it is stored.
                            Example: PestDefinitions.pestVariables['NPAR'] = "number of parameters".
    - fileFormatsTemplates: Dictionary containing the contents of file templates, e.g. of the pst file format

    """


    class PestVariable:
        name = ''
        type = ''
        value = ''
        description = ''
        section = ''

        def __init__(self, name, vartype, values, description, section):
            self.name = name
            self.type = vartype
            self.value = values
            self.description = description
            self.section = section

    pestVariables = {}
    fileFormatTemplates = {}
    fileFormatTemplatesBlocks = {}

    def loadVarDef(self,filename):
        descFile = open(filename)
        section = descFile.readline().strip()
        descFile.readline() #jump table header
        lines = descFile.readlines() #read all other
        for line in lines:
            name, type, value, description = line.split('\t')
            self.pestVariables[name] = self.PestVariable(name, type, value, description.strip(), section)
        descFile.close()

    def loadFileFormatTemplate(self, filename):
        defFile = open(filename)
        extension = filename.split('\\')[-1].split('.')[0]
        lines = defFile.readlines()
        self.fileFormatTemplates[extension] = [item.strip() for item in lines]
        defFile.close()

    def loadBlockFileFormatTemplate(self, filename):
        extension = filename.split('\\')[-1].split('.')[1]
        self.fileFormatTemplatesBlocks[extension] = BlockFile(filename)

    def __init__(self):

        # Get directory where this script is located.
        # definition files are expected in the same directory
        basePath = os.path.realpath(__file__).replace("pestdef.py","")

        # load variable definitions
        listOfVarDefFiles =['pestdef.controlData.vardef.txt',
                            'pestdef.parameterData.vardef.txt',
                            'pestdef.observationData.vardef.txt',
                            'pestdef.parameterGroupData.vardef.txt',
                            'pestdef.observationGroupData.vardef.txt']
        for VarDefFile in listOfVarDefFiles:
            self.loadVarDef(str(basePath)+VarDefFile)

        # load file definitions of block-type file formats
        self.loadBlockFileFormatTemplate(str(basePath)+'pestdef.pst.bfileDef.txt')

    def pestcast(self,varName,value):
            varType = self.pestVariables[varName].type
            if varType == 'text':
                return value
            if varType == 'integer':
                return int(value)
            if varType == 'real':
                return float(value)
