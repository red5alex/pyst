__author__ = 'are'

import subprocess

# create the exe file
subprocess.call('del dist', shell=True)
subprocess.call("python setup.py py2exe", shell=True)