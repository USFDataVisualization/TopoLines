import numpy as np
import scipy.fftpack as scifft
import scipy.ndimage as scind
import lcsmooth.__rdp as mod_rdp
import topolines.topolines as mod_tda
import math


def __linear_map(val, in0, in1, out0, out1):
    t = (val - in0) / (in1 - in0)
    return out0 * (1 - t) + out1 * t


def __linear_map_points(data, points):
    outdata = []
    j = 0
    for i in range(0, len(data) - 1):
        if points[j + 1][0] < i:
            j += 1
        p0 = points[j]
        p1 = points[j + 1]
        outdata.append([i, __linear_map(i, p0[0], p1[0], p0[1], p1[1])])
    outdata.append([len(data) - 1, data[-1]])
    return outdata


#
#
# RANK FILTERS
def median(data, width: int):
    res = scind.median_filter(data, size=width, mode='nearest')
    return list(enumerate(res))


#
#
# CONVOLUTIONAL FILTERS
def gaussian(data, sigma_val):
    res = scind.gaussian_filter1d(data, sigma=sigma_val, mode='nearest')
    return list(enumerate(res))


#
#
# FREQUENCY DOMAIN FILTERS
def cutoff(data, filter_level: float):
    max_freq = int(__linear_map(filter_level, 0, 1, len(data), 2))
    fft = scifft.rfft(data)
    fft[max_freq:] = 0
    res = scifft.irfft(fft)
    return list(enumerate(res))


#
#
# SUBSAMPLING FILTERS
def subsample(data, filter_level: float):
    num_out_points = int(__linear_map(filter_level, 0, 1, len(data), 4))
    keys = [[0, data[0]]]
    for i in range(1, num_out_points - 1):
        idx = __linear_map(i, 0, num_out_points - 1, 0, len(data) - 1)
        i0 = int(np.math.floor(idx))
        i1 = i0 + 1

        keys.append([idx, __linear_map(idx, i0, i1, data[i0], data[i1])])
    keys.append([len(data) - 1, data[-1]])
    return __linear_map_points(data, keys)


def rdp(data, eps):
    dtmp = list(enumerate(data))
    count = math.ceil(__linear_map(eps, 0, 1, 1, len(dtmp)))
    tmp = mod_rdp.rdp_iter_count(dtmp, count)
    return __linear_map_points(data, tmp)


def tda(data, threshold):
    return list(enumerate(mod_tda.filter_tda_count(data, threshold)))
