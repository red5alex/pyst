__author__ = 'are'
import sys, os, shutil
import pystpak

#READ PARAMETERS FROM COMMAND LINE:
try:
    if len(sys.argv) in [4,5]:
        pestfilename = sys.argv[1]
        pestfile = pystpak.PestCtrlFile(pestfilename)

        parname = sys.argv[2]
        if not parname in pestfile.params:
            print("ERROR: " + parname + " not defined in " + pestfilename)
            raise ValueError

        n = int(float(sys.argv[3]))
        if not n > 0:
            print('ERROR: n must be positive!')
            raise ValueError


        if len(sys.argv) == 5:
            outfile = sys.argv[4]
        else:
            outfile = parname+".dat"
    else:
        raise ValueError

except ValueError:
    absPathThisPyScript = os.path.realpath(__file__) # directory of THIS script
    usage_file = open(absPathThisPyScript.replace("beojactest.py","beojactest_usage.txt"))
    print(usage_file.read())
    usage_file.close()
    os._exit(0)

# CREATE PARAMETER FILES
# calculate parameter levels:
parBaseVal      = pestfile.params[parname].PARVAL1
parGroup        = pestfile.params[parname].PARGP
increment       = pestfile.paramGroups[parGroup].DERINC
incrementType   = pestfile.paramGroups[parGroup].INCTYP

if incrementType == "relative":
    a = 1. + increment
    b = 0.
else: # = "absolute"
    a = 1.
    b = increment

#TODO: rel_to_max
#TODO: regard bounds

parLevels = [parBaseVal]
direction = 1
for i in range(0,n):
    if direction == 1:  #upwards
        parLevels.append(parLevels[-1]*a+b)
        direction = -direction
    else:               #downwards
        parLevels.insert(0,parLevels[0]/a-b)
        direction = -direction

del a, b, direction, i, increment, incrementType

# write parFiles:

workPath = "."
#if outfile in os.listdir("."):
#    shutil.rmtree(workPath)
#os.mkdir(workPath)
#os.chdir(workPath)

for i in range(0,n):
    parFile = pystpak.ParamValueFile()
    pp = pestfile.params
    for p in pp:
        name = p
        value = pp[p].PARVAL1
        scale = pp[p].SCALE
        offset = pp[p].OFFSET

        if name == parname:
            value = parLevels[i]
        #TODO: tied parameters

        parFile.addPar(name,value,scale,offset)

    parFile.write(parname+str(i)+".par")

del parFile, i, name, offset, scale, value, p, pp

#EXECUTE PEST

fin = open("pest.in","w")
fin.write(parname+"\n")
fin.write(str(0)+"\n")
fin.write(str(n-1)+"\n")
fin.write(outfile+".rrf")
fin.close()

pestCommand = '"C:\\Program Files\\PEST\\pest_.exe" ' + pestfilename + ' /f < pest.in'
os.system(pestCommand)

# READ RUN RECORD FILE
rrffile = pystpak.RunRecordFile()
rrffile.parsefrom(outfile+".rrf")
#TODO: Parameter sets are not written correctly, rework RRF parser (based on blocked file)


os._exit(0)


