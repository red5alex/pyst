__author__ = 'are'

import pyst as ps
import pyst.feflow as fps

parameterTable = fps.FePestParTable('_partable.txt')

UncertaintyFile = ps.UncertaintyFile()

for pi in parameterTable.par:
    p = parameterTable.par[pi]

    stdev = (p.upperbound - p.lowerbound) / 4  # interprets bounds as 95% interval limits of a gaussian distribution
    #TODO: log-transformed calculation
    UncertaintyFile.addstdev(p.name, stdev)

UncertaintyFile.save('_dam.unc')



