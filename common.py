import fnmatch
import os
import time
from operator import itemgetter

import simplejson as json

import lcsmooth.filter1d as filter1d
import lcsmooth.measures as measures

import math

filter_list = ['cutoff','subsample','tda','rdp','gaussian', 'median', 'mean', 'min', 'max', 'savitzky_golay',
               'butterworth', 'chebyshev']

def process_smoothing(input_signal, filter_name, filter_level):
    input_min = min(input_signal)
    input_max = max(input_signal)
    input_range = input_max - input_min

    start = time.time()
    # filter_data = []
    if filter_name == 'cutoff':
        filter_data = filter1d.cutoff(input_signal, filter_level)
    elif filter_name == 'subsample':
        filter_data = filter1d.subsample(input_signal, filter_level)
    elif filter_name == 'tda':
        level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        filter_data = filter1d.tda(input_signal, level)
    elif filter_name == 'rdp':
        level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        filter_data = filter1d.rdp(input_signal, level)
    elif filter_name == 'gaussian':
        level = filter1d.__linear_map(filter_level, 0, 1, 0.1, 30)
        filter_data = filter1d.gaussian(input_signal, level)
    elif filter_name == 'median':
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 100)
        filter_data = filter1d.median(input_signal, int(level))
    elif filter_name == 'mean':
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 100)
        filter_data = filter1d.mean(input_signal, int(level))
    elif filter_name == 'min':
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 100)
        filter_data = filter1d.min_filter(input_signal, int(level))
    elif filter_name == 'max':
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 100)
        filter_data = filter1d.max_filter(input_signal, int(level))
    elif filter_name == 'savitzky_golay':
        level = filter1d.__linear_map(filter_level, 0, 1, 1, len(input_signal) / 4)
        filter_data = filter1d.savitzky_golay(input_signal, int(level) * 2 + 1, 2)
    elif filter_name == 'butterworth':
        level_tmp = filter1d.__linear_map(filter_level, 0, 1, 1.1, 9999.9)
        level = math.log(level_tmp)/math.log(10000)
        filter_data = filter1d.butterworth(input_signal, 1-level, 2)
    elif filter_name == 'chebyshev':
        level_tmp = filter1d.__linear_map(filter_level, 0, 1, 1.1, 9999.9)
        level = math.log(level_tmp)/math.log(10000)
        filter_data = filter1d.chebyshev(input_signal, 1-level, 2, 0.001)
    else:
        filter_data = list(enumerate(input_signal))
    end = time.time()

    output_signal = list(map(lambda x: x[1], filter_data))

    info = {}
    info["processing time"] = end - start
    info["filter level"] = filter_level
    info["filter name"] = filter_name

    res_stats = {}
    res_stats["mean"] = measures.mean(output_signal)
    res_stats["pop stdev"] = measures.stdev_population(output_signal)
    res_stats["sample stdev"] = measures.stdev_sample(output_signal)
    res_stats["pop variance"] = measures.variance_population(output_signal)
    res_stats["sample variance"] = measures.variance_sample(output_signal)
    res_stats["snr"] = measures.snr(output_signal)
    res_stats["minimum"] = min(output_signal)
    res_stats["maximum"] = max(output_signal)

    metrics = {}
    metrics["covariance"] = measures.covariance(input_signal, output_signal)
    metrics["pearson cc"] = measures.pearson_correlation(input_signal, output_signal)
    metrics["spearman rc"] = measures.spearman_correlation(input_signal, output_signal)
    metrics["L1 norm"] = measures.l1_norm(input_signal, output_signal)
    metrics["L2 norm"] = measures.l2_norm(input_signal, output_signal)
    metrics["L_inf norm"] = measures.linf_norm(input_signal, output_signal)
    metrics["delta volume"] = measures.delta_volume(input_signal, output_signal)
    metrics["approx entropy"] = measures.approximate_entropy_v2( output_signal )
    metrics["frequency preservation"] = measures.frequency_preservation(input_signal, output_signal)
    metrics["signal to noise"] = measures.signal_to_noise(input_signal, output_signal)
    metrics.update( measures.peakiness(input_signal, output_signal) )
    # if (Float.isFinite(f.phaseShifted(fPhi))) ret.setFloat( "phaseShift", f.phaseShifted(fPhi) );

    return {'original': list(enumerate(input_signal)), 'filtered': filter_data,
            'info': info, 'statistics': res_stats, 'metrics': metrics}


def get_datasets(data_dir):
    ret = {}
    for dataset in os.listdir(data_dir):
        if os.path.isdir(data_dir + "/" + dataset):
            cur_ds = []
            for data_file in os.listdir(data_dir + "/" + dataset):
                if fnmatch.fnmatch(data_file, "*.json"):
                    cur_ds.append(data_file[:-5])
                if fnmatch.fnmatch(data_file, "*.csv"):
                    cur_ds.append(data_file[:-4])
            ret[dataset] = cur_ds
    return ret


def load_dataset(data_dir, datasets, ds, df):
    input_signal = None

    if ds == 'climate' and df in datasets[ds]:
        filename = data_dir + "/" + ds + "/" + df + ".json"

        with open(filename) as json_file:
            cur_dataset = json.load(json_file)
            cur_dataset['data'].sort(reverse=False, key=itemgetter('timestamp'))
            return list(map(lambda X: float(X['value']), cur_dataset['data']))

    elif (ds == 'stock' or ds == 'temperature' or ds == 'radioAstronomy' or ds == 'statistical') and df in datasets[ds]:
        filename = data_dir + "/" + ds + "/" + df + ".json"

        with open(filename) as json_file:
            cur_dataset = json.load(json_file)
            return list(map(lambda X: float(X['value']), cur_dataset['results']))

    elif ds == 'eeg' and df in datasets[ds]:
        filename = data_dir + "/" + ds + "/" + df + ".csv"
        with open(filename) as csv_file:
            data = [next(csv_file) for x in range(1000)]
            return list(map(lambda X: float(X), data))

    return None
