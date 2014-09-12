__author__ = 'are'

import sys
import pysttools

if len(sys.argv) > 1:
        if sys.argv[1] == "rrf2table":
            try:
                pysttools.montecarlo.rrf2table(sys.argv[2], sys.argv[3])
            except ValueError:
                pysttools.montecarlo.rrf2table_help()

        else:
            print(' ---- PyST toolbox --- v0.001')
            print('')
            print('available commands:')
            print('')
            print('rrf2table    converts a run records (rrf) file into a dat table (dat)')


