__author__ = 'are'

import pystpak

parname = "con-sealing"

runRecord = pystpak.RunRecordFile(parname+".rrf")

runRecord.saveToDat(parname,"stabil-"+parname+".dat")

pass
