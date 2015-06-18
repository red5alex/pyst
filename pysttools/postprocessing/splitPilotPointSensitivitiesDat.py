__author__ = 'are'

inFilePath = "D:/Repositories/deber1-stor/41801573-2_Freeport_DRC/work/model/Localmodels/Tenke/femdata/Tenke_2014_r136_PEST_002_prognosis_master/pilot_point_sensitivities.dat"
outFilePath =  "D:/Repositories/deber1-stor/41801573-2_Freeport_DRC/work/model/Localmodels/Tenke/femdata/Tenke_2014_r136_PEST_002_prognosis_master/"

inFile = open(inFilePath)

files = {}

header = inFile.readline()

for l in inFile.readlines():
    words = l.split()
    definition = words[0].split("-")[0]
    if definition not in files.keys():
        files[definition] = open(outFilePath+definition+"_sensitivities.dat", "w")
        files[definition].write(header)
    files[definition].write(l)


inFile.close()
for f in files:
    files[f].close()