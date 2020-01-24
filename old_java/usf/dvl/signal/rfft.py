'''
    Compute RFFT  Filter
    - computes rfft and prints it to stdout so that
    the java program can read it and utilize.
    
    run: python rfft.py Orig_Vals.txt
    '''

import sys
import time
import scipy.fftpack as sci


def R_FFT( fname ):
    
    # Read data and calc rfft
    data = fname.readlines()
    result = sci.rfft(data)
    
    # print result
    for i in result:
        print( "%.4f " %i )


def main():
    # filename to read
    fname = sys.argv[ 1 ]
    original = open( fname )
    
    R_FFT( original )


# Code starts here #
if __name__ == '__main__':
    main()

