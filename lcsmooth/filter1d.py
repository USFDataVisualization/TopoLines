import numpy as np
import scipy.fftpack as scifft
import scipy.ndimage as scind
import scipy.signal as scisig
from sklearn.isotonic import IsotonicRegression

import lcsmooth.__rdp as mod_rdp
import lcsmooth.__tda as mod_tda


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


def min_filter(data, width: int):
    res = scind.minimum_filter(data, size=width, mode='nearest')
    return list(enumerate(res))


def max_filter(data, width: int):
    res = scind.maximum_filter(data, size=width, mode='nearest')
    return list(enumerate(res))


#
#
# CONVOLUTIONAL FILTERS
def gaussian(data, sigma_val):
    res = scind.gaussian_filter1d(data, sigma=sigma_val, mode='nearest')
    return list(enumerate(res))


def mean(data: list, width: int) -> list:
    pad_pre = int(width / 2)
    pad_post = width - 1 - pad_pre
    tmp = np.pad(data, [(pad_pre, pad_post)], mode='edge')
    res = np.convolve(tmp, np.ones((width,)) / width, mode='valid')
    return list(enumerate(res))


def savitzky_golay(data: list, window_length: int, polyorder: int):
    res = scisig.savgol_filter(data, window_length, polyorder, mode='nearest')
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


def butterworth(data, cutoff_freq: float, order: int):
    b, a = scisig.butter(order, cutoff_freq, btype='low')
    res = scisig.lfilter(b, a, data)
    return list(enumerate(res))

import matplotlib.pyplot as plt

def chebyshev(data, cutoff_freq: float, order: int, ripple_db: float):
    b, a = scisig.cheby1(order, ripple_db, cutoff_freq, btype='low')
    res = scisig.lfilter(b, a, data)
    return list(enumerate(res))


def elliptical(data, cutoff_freq: int, order: int, ripple_db: float, max_atten_db: float):
    b, a = scisig.ellip(order, ripple_db, max_atten_db, cutoff_freq, btype='low')
    res = scisig.lfilter(b, a, data)
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
    tmp = mod_rdp.rdp(dtmp, epsilon=eps)
    return __linear_map_points(data, tmp)


def tda(data, threshold):
    cp_keys = mod_tda.filter_tda(data, threshold)

    tmp = [data[0]]
    for i in range(len(cp_keys) - 1):
        ir = IsotonicRegression(increasing=(cp_keys[i][1] < cp_keys[i + 1][1]))
        y = data[cp_keys[i][0]: cp_keys[i + 1][0] + 1]
        y_ = ir.fit_transform(range(len(y)), y)
        tmp.extend(y_[1:])

    # return __linear_map_points(data, cp_keys)
    return list(enumerate(tmp))
