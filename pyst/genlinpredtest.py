__author__ = 'are'

from pyst.genlinpredout import GenlinpredOutFile
from pyst.utils.linearUncertainty import genlinpred
import os


path = "D:/Repositories/deber1-stor/41801573-2_Freeport_DRC/work/model/Localmodels/Tenke/femdata/Tenke_2014_r136_PEST_001/"
pstfilename = path + "noreg.pst"

genlinpred(pstfilename,
           workdir=path,
           prediction_par="xco-sele~00b",
           outfilename="genlinpred_00b.out")

testfile = GenlinpredOutFile(path+"genlinpred.out")

os.chdir(path)

stop = True
pass