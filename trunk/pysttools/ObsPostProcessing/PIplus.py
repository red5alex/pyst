__author__ = 'are'

from pyst.feflow.fpifile import FpiFile
from pyst.feflow.fpofile import FpoFile

ifmfpopath = "ifm.fpo"
fpipath = "PIcalibTest.fpi"

fpi = FpiFile(fpipath)

kALU = fpi.par["xco-ALU"].value
kDET = fpi.par["xco-DET"].value
kCC = fpi.par["xco-CC"].value
kNAMORE = fpi.par["xco-NAMORE"].value
kNAMBIF = fpi.par["xco-NAMBIF"].value
kJER = fpi.par["xco-JER"].value

# generated from Excel table:
TA0 = 0 * kALU + 20 * kDET + 0 * kCC + 0 * kNAMORE + 15 * kNAMBIF + 1 * kJER
TA2 = 8 * kALU + 12 * kDET + 0 * kCC + 12 * kNAMORE + 10 * kNAMBIF + 2 * kJER
TA5 = 6 * kALU + 33 * kDET + 0 * kCC + 0 * kNAMORE + 0 * kNAMBIF + 0 * kJER
TA6 = 0 * kALU + 44 * kDET + 0 * kCC + 0 * kNAMORE + 0 * kNAMBIF + 0 * kJER
TA7 = 0 * kALU + 26 * kDET + 0 * kCC + 0 * kNAMORE + 2 * kNAMBIF + 0 * kJER
TB2 = 30 * kALU + 0 * kDET + 0 * kCC + 0 * kNAMORE + 18 * kNAMBIF + 2 * kJER
TB6 = 18 * kALU + 0 * kDET + 12 * kCC + 8 * kNAMORE + 12 * kNAMBIF + 4 * kJER
TB7 = 6 * kALU + 22 * kDET + 0 * kCC + 0 * kNAMORE + 0 * kNAMBIF + 8 * kJER
TC1 = 22 * kALU + 0 * kDET + 14 * kCC + 0 * kNAMORE + 8 * kNAMBIF + 0 * kJER
TNB03 = 0 * kALU + 7 * kDET + 0 * kCC + 12 * kNAMORE + 12 * kNAMBIF + 6 * kJER
TNB07 = 0 * kALU + 10 * kDET + 0 * kCC + 8 * kNAMORE + 20 * kNAMBIF + 12 * kJER
TNB09 = 0 * kALU + 14 * kDET + 0 * kCC + 18 * kNAMORE + 0 * kNAMBIF + 8 * kJER

fpo = FpoFile(ifmfpopath)

# generated from Excel table:
fpo.obs["T-A0"].value = TA0
fpo.obs["T-A2"].value = TA2
fpo.obs["T-A5"].value = TA5
fpo.obs["T-A6"].value = TA6
fpo.obs["T-A7"].value = TA7
fpo.obs["T-B2"].value = TB2
fpo.obs["T-B6"].value = TB6
fpo.obs["T-B7"].value = TB7
fpo.obs["T-C1"].value = TC1
fpo.obs["T-NB03"].value = TNB03
fpo.obs["T-NB07"].value = TNB07
fpo.obs["T-NB09"].value = TNB09

fpo.save("test.fpo")
pass
