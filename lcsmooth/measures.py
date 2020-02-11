import os
import random
import string

import numpy as np
import scipy.stats as scistat

import lcsmooth.__tda as tda


def __random_string(stringLength=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(stringLength))


def pearson_correlation(d0, d1):
    pcc = np.corrcoef(d0, d1)
    return pcc[0, 1]


def spearman_correlation(d0, d1):
    src = scistat.spearmanr(d0, d1)
    return src[0]


def l1_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=1)


def l2_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=2)


def linf_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=np.inf)


def peakiness_bottleneck(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = __random_string(10) + '.pd'
    file_flt = __random_string(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.bottleneck_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness_wasserstein(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = __random_string(10) + '.pd'
    file_flt = __random_string(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = __random_string(10) + '.pd'
    file_flt = __random_string(10) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res_b = tda.bottleneck_distance(file_org, file_flt)
    res_w = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return {'peak bottleneck': res_b, 'peak wasserstein': res_w}
