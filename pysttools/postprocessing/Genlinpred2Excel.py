__author__ = 'are'

from openpyxl import Workbook
from pyst.genlinpredout import GenlinpredOutFile
import os

workpath = "D:/Repositories/deber1-stor/41801573-2_Freeport_DRC/work/model/Localmodels/Tenke/femdata/Tenke_2014_r136_PEST_001/"
filename = "xco-sele~001.genlinpred.out"

os.chdir(workpath)

result = GenlinpredOutFile(filename)
result.write2Excel(filename+".xlsx")
