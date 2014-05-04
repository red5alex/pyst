__author__ = 'are'

import pyst
import pyst.feflow

fpopath = "D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\example_files\\dam_jactest.fpo"
fpofile = pyst.feflow.FpoFile(fpopath)

testobs = fpofile.obs['hea-10'].value

print(str(testobs))

pass
