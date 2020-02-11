import scipy.fftpack as scifft
import scipy.ndimage as scind
import numpy as np

import mod_rdp
import mod_tda


def __linear_map(val, in0, in1, out0, out1):
    t = (val - in0) / (in1 - in0)
    return out0 * (1 - t) + out1 * t


def __linear_map_points(data, points):
    outdata = []
    j = 0
    for i in range(0,len(data)-1):
        if points[j+1][0] < i :
            j += 1
        p0 = points[j]
        p1 = points[j + 1]
        outdata.append([i, __linear_map(i, p0[0], p1[0], p0[1], p1[1])])
    outdata.append([len(data) - 1, data[-1]])
    return outdata


def lowpass(data, max_freq: int):
    fft = scifft.rfft(data)
    fft[max_freq:] = 0
    res = scifft.irfft(fft)
    return list(enumerate(res))


def gaussian(data, sigma_val):
    res = scind.gaussian_filter1d(data, sigma=sigma_val, mode='nearest')
    return list(enumerate(res))


def median(data, width: int):
    res = scind.median_filter(data, size=width, mode='nearest')
    return list(enumerate(res))


def mean(data: list, width: int) -> list:
    pad_pre = int(width/2)
    pad_post = width-1-pad_pre
    tmp = np.pad( data, [( pad_pre,pad_post)], mode='edge' )
    res = np.convolve(tmp, np.ones((width,)) / width, mode='valid')
    return list(enumerate(res))


def rdp(data, eps):
    dtmp = list(enumerate(data))
    tmp = mod_rdp.rdp(dtmp, epsilon=eps)
    return __linear_map_points(data, tmp)


def tda(data, threshold):
    cp_keys = mod_tda.filter_tda(data, threshold)
    return __linear_map_points(data, cp_keys)


def subsample(data, num_out_points):
    keys = [[0, data[0]]]
    for i in range(1, num_out_points - 1):
        idx = __linear_map(i, 0, num_out_points - 1, 0, len(data) - 1)
        i0 = int(np.math.floor(idx))
        i1 = i0 + 1

        keys.append([idx, __linear_map(idx, i0, i1, data[i0], data[i1])])
    keys.append([len(data) - 1, data[-1]])

    #print( keys )

    return __linear_map_points(data, keys)
