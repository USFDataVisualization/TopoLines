import statistics as stats
import numpy as np
import math
import scipy.fftpack as scifft
import scipy.stats as scistat



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


def signal_to_noise(original,filtered):
    noise = np.subtract(original, filtered)
    n_var = variance_sample(noise)
    if n_var <= 1e-8:
        return 1e10
    else:
        return variance_sample(filtered) / n_var



#
# public
# float
# peakinessBottleneck()
# {
# if (Float.isNaN(peakinessbottleneck))
# {
#     SignalMergeTree
# m0 = new
# SignalMergeTree(this);
# SignalMergeTree
# m1 = new
# SignalMergeTree(orig_graph);
# peakinessbottleneck = (float)
# SignalMergeTree.BottleneckDistance(m1, m0);
# }
# return peakinessbottleneck;
# }
#
# public
# float
# peakinessWasserstein()
# {
# if (Float.isNaN(peakinesswasserstein)) {
# SignalMergeTree m0 = new SignalMergeTree( this );
# SignalMergeTree m1 = new SignalMergeTree( orig_graph );
# if ( m0.size() <= 1 )
# peakinesswasserstein = Float.POSITIVE_INFINITY;
# else
# peakinesswasserstein = (float)SignalMergeTree.WassersteinDistance(m1, m0);
# }
# return peakinesswasserstein;
# }
#


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

