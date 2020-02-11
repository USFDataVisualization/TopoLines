import statistics as stats
import numpy as np
import math
import scipy.fftpack as scifft
import scipy.stats as scistat
from entropy import *
import numpy as np
import lcsmooth.__tda as tda
import random
import string
import os


def mean(data):
    return stats.mean(data)


def stdev_population(data):
    return stats.pstdev(data)


def stdev_sample(data):
    return stats.stdev(data)


def variance_population(data):
    return stats.pvariance(data)


def variance_sample(data):
    return stats.variance(data)


def snr(data):
    return mean(data) / stdev_sample(data)


def covariance(d0, d1):
    cov = np.cov(d0, d1)
    return cov[0, 1]


def pearson_correlation(d0, d1):
    pcc = np.corrcoef(d0, d1)
    return pcc[0, 1]


def spearman_correlation(d0, d1):
    src = scistat.spearmanr(d0, d1)
    return src[0]


def __approx_ent_max_d(pc, i, j, m):
    maxD = 0;
    for k in range(0, m):
        maxD = max(maxD, abs(pc[i + k] - pc[j + k]))
    return maxD


def __approx_ent_c(pc, i, m, r):
    cnt = 0
    for j in range(0, len(pc) - m + 1):
        d = __approx_ent_max_d(pc, i, j, m)
        if d < r:
            cnt += 1
    return cnt / (len(pc) - m + 1)


def __approx_ent_phi(pc, m, r):
    sum = 0
    for i in range(0, len(pc) - m + 1):
        c = __approx_ent_c(pc, i, m, r)
        sum += math.log(c)
    return sum / (len(pc) - m + 1)


def approximate_entropy(pc, window_size, filter_level):
    return __approx_ent_phi(pc, window_size, filter_level) - __approx_ent_phi(pc, window_size + 1, filter_level)


def l1_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=1)


def l2_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=2)


def linf_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=np.inf)


def delta_volume(d0, d1):
    return np.sum(d1) - np.sum(d0)


# Calculate of the L2norm of frequency domain
def frequency_preservation(d0, d1):
    fft0 = scifft.rfft(d0)
    fft1 = scifft.rfft(d1)
    diff = np.subtract(fft0, fft1)
    return np.linalg.norm(diff, ord=2)


def signal_to_noise(original, filtered):
    noise = np.subtract(original, filtered)
    n_var = variance_sample(noise)
    if n_var <= 1e-8:
        return 1e10
    else:
        return variance_sample(filtered) / n_var


def approximate_entropy_v2(x):
    # print(perm_entropy(x, order=3, normalize=True))  # Permutation entropy
    # print(spectral_entropy(x, 100, method='welch', normalize=True))  # Spectral entropy
    # print(svd_entropy(x, order=3, delay=1, normalize=True))  # Singular value decomposition entropy
    # print(app_entropy(x, order=2, metric='chebyshev'))  # Approximate entropy
    # print(sample_entropy(x, order=2, metric='chebyshev'))  # Sample entropy
    # print(lziv_complexity('01111000011001', normalize=True))  # Lempel-Ziv complexity
    return app_entropy(x, order=2, metric='chebyshev')


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def peakiness_bottleneck(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = randomString(10) + '.pd'
    file_flt = randomString(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.bottleneck_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness_wasserstein(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = randomString(10) + '.pd'
    file_flt = randomString(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = randomString(10) + '.pd'
    file_flt = randomString(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res_b = tda.bottleneck_distance(file_org, file_flt)
    res_w = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return {'peak bottleneck': res_b, 'peak wasserstein': res_w}

#
# public
# float
# phaseShifted(FilteredSignal
# phi ) {
# float
# tot = 0;
# for (int i = 0; i < size() - 1 & & i < phi.size(); i++ ) {
# float o = phi.orig_graph.get(i) - phi.get(i);
# float f = orig_graph.get(i+1) - get(i+1);
# tot += Math.pow(o-f, 2);
# }
# return (float)
# Math.sqrt(tot);
# }
#
