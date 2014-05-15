__author__ = 'are'


class UncertaintyFile:

    blocks = []

    class StdevBlock:
        type = "standard deviation block"
        stdev = {}

        def __init__(self, std_multiplier=1.):
            self.std_multiplier = std_multiplier
            self.stdev = {}

        def addstdev(self, name, value):
            self.stdev[name] = value

    class CovmatBlock:
        type = "covariance matrix block"

        def __init__(self, filename, variance_multiplier=1.):
            self.filename = filename
            self.variance_multiplier = variance_multiplier

    class PstflBlock:
        type = "PEST control file block"

        def __init__(self, filename, variance_multiplier=1.):
            self.filename = filename
            self.variance_multiplier = variance_multiplier

    def __init__(self, filename=''):
        self.blocks = []
        if filename == '':
            self.stdevs = {}
        else:
            pass
            #TODO: implement reading procedure here

    def addstdev(self, name, value):
        """This is a convenience function. instead of creating and accessing blocks, one can simply add a standard
        deviation entry to the file. It will be added to the first standard deviation block in the list. If this
        does not exist, it will be created with multiplier one. You can therefore use this method with an empty file,
        and save it afterwards.
        """
        if self.blocks is None:
            self.blocks = []

        stdevblocks = [b for b in self.blocks if b.type == "standard deviation block"]
        if len(stdevblocks) == 0:
            self.addstdevblock()
            stdevblocks = [b for b in self.blocks if b.type == "standard deviation block"]

        stdevblocks[0].addstdev(name, value)

    def addstdevblock(self):
        self.blocks.append(self.StdevBlock())

    def addcovariancematrix(self, filename, variance_multiplier=1.):
        self.blocks.append(self.CovmatBlock(filename, variance_multiplier))

    def addpestfile(self, filename, variance_multiplier=1.):
        self.blocks.append(self.PstflBlock(filename, variance_multiplier))

    def save(self, filename, ):
        outfile = open(filename, 'w')

        for b in self.blocks:
            if b.type == "standard deviation block":
                outfile.write('START STANDARD_DEVIATION\n')
                outfile.write('std_multiplier ' + str(b.std_multiplier) + '\n')
                for item in b.stdev:
                    outfile.write(item+' '+str(b.stdev[item]) + '\n')
                outfile.write('END STANDARD_DEVIATION\n\n')

            if b.type == "covariance matrix block":
                outfile.write('START COVARIANCE_MATRIX\n')
                outfile.write('file "' + b.filename + '"\n')
                outfile.write('variance_multiplier ' + str(b.variance_multiplier) + '\n')
                outfile.write('END COVARIANCE_MATRIX\n\n')

            if b.type == "PEST control file block":
                outfile.write('START PEST_CONTROL_FILE\n')
                outfile.write('file "' + b.filename + '"\n')
                outfile.write('variance_multiplier ' + str(b.variance_multiplier) + '\n')
                outfile.write('END PEST_CONTROL_FILE\n\n')

        outfile.close()