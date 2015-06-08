__author__ = 'are'

import sys

def mat2dat(matfile, datfile, pivot=False, verbose=False):
    
    # open mat File
    try:
        if verbose:
            print(('opening '+matfile+'...'))
        matfileinstance = open(matfile)
        if verbose:
            print('done.\n')
    except:
        print('Error opening file '+matfile)
        exit(1)
    
    # read meta-information
    try:
        if verbose : print('reading Meta-information...')
        line = matfileinstance.readline()
        nrow, ncol, icode  = line.split()
    
        ncol = int(ncol)
        nrow = int(nrow)
        icode = int(icode)
    
        print(str(ncol)+ ' columns / ' + str(nrow) + ' rows')
        if pivot: print('\t(will be swapped in output file)')
        if verbose : print('unknown value:\t' + str(icode))
        if verbose : print('done.\n')
    
    except:
        print('error reading meta data: file corrupt?')
        exit(1)
    
    if (icode!=2):
        print('Only MAT-files with ICODE=2 supported!')
        exit(1)
    
    if verbose : print('Reading file content ...')
    
    # read data
    datasets = []
    line = matfileinstance.readline()
    if verbose : print('Reading data')
    while(line.count('row') < 1):
        lcontent = line.split()
        datasets += lcontent
        line = matfileinstance.readline()
        if len(line) == 0:
            print('Empty line read in file data: file corrupt?')
            exit(1)
    
    # read row names
    rowNames = []
    n = 0
    line = matfileinstance.readline()
    if verbose : print('Reading row names')
    while(line.count('* column names') < 1):
        if len(line) == 0:
            print('Empty line read in row names: file corrupt?')
            exit(1)
        rowName = line.strip()
        rowNames = rowNames + [rowName]
        n += 1
        line = matfileinstance.readline()
    
    # read column names
    colNames = []
    line = matfileinstance.readline()
    if verbose : print('Reading column names')
    for n in range(0, ncol):
        if len(line) == 0:
            print('Empty line read in column names: file corrupt?')
            exit(1)
        colName = line.strip();
        colNames = colNames + [colName]
        line = matfileinstance.readline()
    
    if verbose : print('done.\n')
    
    # closing mat file
    try:
        matfileinstance.close()
    except:
        print('error closing file')
        exit(1)
    
    ######### WRITE FILE
    # opening dat file
    try:
        #print('Writing '+datfile+'...')
        sys.stdout.write('Writing '+datfile+'.') #
        sys.stdout.flush()
        DatFile = open(datfile,'w')
    except:
        print('error opening file '+datfile)
        exit(1)
    
    # write content
    # header lines
    if not pivot: # normal mode
        wline = 'dataset '
        for col in range(0, ncol):
            wline += colNames[col]
            wline += ' '
        wline += '\n'
        DatFile.writelines(wline)
    else:           # writes a pivoted table
        wline = 'dataset '
        for row in range(0, nrow):
            wline += rowNames[row]
            wline += ' '
        wline += '\n'
        DatFile.writelines(wline)
    
    # update progress display
    if not verbose:
        sys.stdout.write('.')
        sys.stdout.flush()
    
    # body - non-pivoted
    if not pivot:
        for row in range(0, nrow):
            wline = rowNames[row]
            wline += ' '
            for i in range(row*ncol,row*ncol+ncol):
                wline += datasets[i]
                wline += ' '
            wline += '\n'
            DatFile.writelines(wline)
    # body - pivoted
    else: # if pivot is activated, rows and columns are exchanged
        for col in range(0, ncol):
            wline = colNames[col]
            wline += ' '
            # read evey nth entry of dataset only, where n = ncol:
            for i in range(col,nrow*ncol,ncol):
                wline += datasets[i]
                wline += ' '
            wline += '\n'
            DatFile.writelines(wline)
    
    # update progress display
    if not verbose:
        sys.stdout.write('.')
        sys.stdout.flush()
    
    #closing file
    try:
        if verbose : print('Closing '+datfile)
        DatFile.close()
    except:
        print('\nerror closing file')
        exit(1)

    print('done')


def main():
    # read command line parameters, produce help text
    
    try:
        if len(sys.argv) < 2:
            raise ValueError
    
        pivot = False
        if len(sys.argv) == 3:
            if sys.argv[2] == '-pivot':
                pivot = True
            else:
                raise ValueError
    
        if len(sys.argv) > 4:
            raise ValueError
    
        MatFileName = sys.argv[1]
    
        name1, name2 = MatFileName.split('.')
        DatFileName = name1+'.dat'
    
    except ValueError:
        print('MAT2DAT version 0.8 DHI Water & Environment',
              'converts a PEST matrix (mat) file to ASCII table (dat) format ',
              '',
              'Usage:',
              '\tmat2dat file [-pivot]',
              '',
              'where',
              '\tfile:    matrix file (.mat)',
              '\t-pivot:  exchanges rows and columns',
              sep='\n')
        exit(1)
    
    verbose = False

    print('converting {} to {}'.format(MatFileName,DatFileName))
    if pivot:
        print('with pivot option')
    
    mat2dat(MatFileName, DatFileName, pivot, verbose)

if __name__ == "__main__":
    # only to run when not called via 'import'
    main()