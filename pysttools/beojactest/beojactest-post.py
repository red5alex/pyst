__author__ = 'are'

import pyst

parname = "con-sealing"

runRecord = pyst.RunRecordFile(parname+".rrf")

runRecord.saveToDat(parname,"stabil-"+parname+".dat")

pass
