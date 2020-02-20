import os
import random
import string

from entropy import *

import topolines.topolines as tda


def __random_string(stringLength=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(stringLength))


def l1_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=1)


def linf_norm(d0, d1):
    diff = np.subtract(d0, d1)
    return np.linalg.norm(diff, ord=np.inf)


def peakiness_bottleneck(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = 'tmp_' + __random_string(7) + '.pd'
    file_flt = 'tmp_' + __random_string(7) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.bottleneck_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness_wasserstein(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = 'tmp_' + __random_string(7) + '.pd'
    file_flt = 'tmp_' + __random_string(7) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return res


def peakiness(original, filtered):
    pd_org = tda.get_persistence_diagram(original)
    pd_flt = tda.get_persistence_diagram(filtered)
    file_org = 'tmp_' + __random_string(7) + '.pd'
    file_flt = 'tmp_' + __random_string(7) + '.pd'
    tda.save_persistence_diagram(file_org, pd_org)
    tda.save_persistence_diagram(file_flt, pd_flt)
    res_b = tda.bottleneck_distance(file_org, file_flt)
    res_w = tda.wasserstein_distance(file_org, file_flt)
    os.remove(file_org)
    os.remove(file_flt)
    return {'peak bottleneck': res_b, 'peak wasserstein': res_w}


def approximate_entropy(x):
    return app_entropy(x, order=2, metric='chebyshev')
