import fnmatch
import os
import time
from operator import itemgetter

import simplejson as json

import lcsmooth.filter1d as filter1d
import lcsmooth.measures as measures

filter_list = ['cutoff','subsample','tda','rdp','gaussian', 'median']


def process_smoothing(input_signal, filter_name, filter_level):
    input_min = min(input_signal)
    input_max = max(input_signal)
    input_range = input_max - input_min

    start = time.time()
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
    else:
        filter_data = list(enumerate(input_signal))
    end = time.time()

    output_signal = list(map(lambda x: x[1], filter_data))

    info = {}
    info["processing time"] = end - start
    info["filter level"] = filter_level
    info["filter name"] = filter_name
    info["minimum"] = min(output_signal)
    info["maximum"] = max(output_signal)

    metrics = {}
    metrics["pearson cc"] = measures.pearson_correlation(input_signal, output_signal)
    metrics["spearman rc"] = measures.spearman_correlation(input_signal, output_signal)
    metrics["L1 norm"] = measures.l1_norm(input_signal, output_signal)
    metrics["L2 norm"] = measures.l2_norm(input_signal, output_signal)
    metrics["L_inf norm"] = measures.linf_norm(input_signal, output_signal)
    metrics.update( measures.peakiness(input_signal, output_signal) )

    return {'original': list(enumerate(input_signal)), 'filtered': filter_data,
            'info': info, 'metrics': metrics}


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
