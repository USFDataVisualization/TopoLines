'''
    Compute RFFT  Filter
    - computes rfft then runs bandpass filter to
    smooth the values, then turns it back from signal to
    the data we need. It then prints it to stdout so that
    the java program can read it and utilize.

    Note: keep range large to make values close to original dataset

    run: python calcRfft.py Orig_Vals.txt -60000 60000 -> no change
    PointContainer: python calcRfft.py Orig_Vals -5 25000

    code starts ~line 75
'''

import sys
import time
import scipy.fftpack as sci


def bandPass_Filter(t,x1,x2):
    temp = []
    for count, value in enumerate(t):
        if count == 0:
            temp.append(value)
            continue

        if( count > x1 and count < x2 ):
            temp.append(value)

        #elif( value < x1 and value > x2 ):
        #    temp.append(value)

        else:
            temp.append(0)

    return temp


def R_FFT( fname, x1, x2 ):

    # Read data and calc rfft
    data = fname.readlines()
    rfft = sci.rfft(data)

    x1 = float(x1)
    x2 = float(x2)

    # value need to be between some range to keep
    filtered_data = bandPass_Filter(rfft,x1,x2)

    # take inverse of rfft
    result = sci.irfft( filtered_data )

    # print result
    for i in result:
        print( "%.8f " %i )


def main():
    # filename to read
    fname = sys.argv[ 1 ]
    original = open( fname )

    # x1 : start
    x1 = sys.argv[ 2 ]
    # x2 : end
    x2 = sys.argv[ 3 ]

    R_FFT( original, x1, x2 )


# Code starts here #
if __name__ == '__main__':
    main()
