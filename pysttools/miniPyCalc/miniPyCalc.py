__author__ = 'are'

"""
 This script facilitates postprocessing of PEST observation values or pre-processing of PEST parameter values.
 The values are loaded from the primary observation file (currently on FEFLOW fpo and fpi files supported).
 The values are processed using commands in the processing files, using Python syntax.
 The valies are finally written to the output file, using the template file (standard PEST tpl syntax).
"""

#TODO: make this accessible via command line:

primaryObsFilePath = "test.fpo"
templateFilePath = "obsTpl.tpl"
processingFilePath = "obsProc.txt"

# load primary parameters

varNames = []
varValues = {}

primaryObsFile = open(primaryObsFilePath)
for line in primaryObsFile.readlines():
    name, value = line.split()
    varNames.append(name)
    varValues[name] = float(value)
primaryObsFile.close()

# execute processing instructions

processingFile = open(processingFilePath)
lines = processingFile.readlines()
for line in lines:
    if "=" in line:
        name, expression = line.split("=")
        if name not in varNames:
            varNames.append(name.strip())
        words = expression.split()
        command = ""
        for word in words:
            for name in varNames:
                if name == word:
                    word = "varValues[\"" + name + "\"]"
            command = command + " " + word
        try:
            varValues[name] = eval(command)
        except:
            print("problem evaluating line " + str(lines.index(line)))
            varValues[name] = None
    pass

processingFile.close()

# write outPutFile

templateFile = open(templateFilePath)
outPutFileName = templateFilePath.replace(".tpl", ".out")
outPutFile = open(outPutFileName, "w")

line = templateFile.readline()
header = line.split()
marker = None
if header[0] != "ptf":
    print("not a PEST template file")
else:
    marker = header[1]

for line in templateFile.readlines():
    words = line.split()
    for word in words:
        if words.index(word) != 0:
            outPutFile.write(" ")
        if word[0] == word[-1] == marker:
            varName = word.strip(marker)
            if varName not in varNames:
                raise(varName + " is undefined!")
            word = str(varValues[varName])
        outPutFile.write(word)
    outPutFile.write("\n")

templateFile.close()
outPutFile.close()
