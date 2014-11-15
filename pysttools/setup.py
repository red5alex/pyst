from distutils.core import setup
import py2exe

BuildList = ['FePestServerMonitor/FePESTServerMonitor.py ',
             'miniPyCalc/miniPyCalc.py',
             'montecarlo/rrf2table.py',
             'montecarlo/montecarlo.py',
             'ObsPostProcessing/correctDrawdowns.py',
             'beojactest/beojactest-pre.py',
             'beojactest/beojactest-post.py',
             'beojactest/analyseJacTest.py',
             'helloWorld.py',
             ]

ResourceFiles = ['../pyst/pestdef.controlData.vardef.txt',
                 '../pyst/pestdef.observationData.vardef.txt',
                 '../pyst/pestdef.observationGroupData.vardef.txt',
                 '../pyst/pestdef.par.fileDef.txt',
                 '../pyst/pestdef.parameterData.vardef.txt',
                 '../pyst/pestdef.parameterGroupData.vardef.txt',
                 '../pyst/pestdef.pst.bfileDef.txt',
                 ]

packages = ['pyst',
            'pyst.feflow',
            'pysttools',
            'pysttools.beoscan',
            'pysttools.beojactest',
            ]

setup(name='pysttools',
      version='0.8',
      url='www.feflow.com',
      license='',
      author='Alexander Renz',
      author_email='are@dhigroup.com',
      description='A collection of productivity tools for PEST and FEFLOW',
      console=BuildList,
      data_files=[('resources', ResourceFiles)],
      options={"py2exe": {
          "unbuffered": True,
          "optimize": 2,
          "excludes": ["email"],
          "skip_archive": True,
          "bundle_files": 2,  # this tells py2exe to bundle everything
      }}
      )
