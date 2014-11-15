__author__ = 'are'

import pyst


def rrf2table(rrffilename, tablefilename):
    runrecord = pyst.RunRecordFile(rrffilename)
    runrecord.saveastable(tablefilename)


def rrf2table_help():
    print("Error in rrf2table. Help text not available.")
    #TODO: write a proper help text

rrfname = 'D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\testmodels\\dam\\dam_sobmontecarlo\\_sobmc.rrf'
tbalefname = 'D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\testmodels\\dam\\dam_sobmontecarlo\\_sobmcresult.dat'

rrf2table(rrfname,tbalefname)