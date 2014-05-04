__author__ = 'are'

import pystpak
import pystpak.feflow

fpopath = "D:\\Repositories\\red5alex.cloudforge\\pyst\\trunk\\example_files\\dam_jactest.fpo"
fpofile = pystpak.feflow.FpoFile(fpopath)

testobs = fpofile.obs['hea-10'].value

print(str(testobs))

pass
