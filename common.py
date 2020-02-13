import fnmatch
import os
import time

import simplejson as json
import numpy as np

import lcsmooth.filter1d as filter1d
import lcsmooth.measures as measures

data_dir = './data'
filter_list = ['cutoff', 'subsample', 'tda', 'rdp', 'gaussian', 'median']
data_sets = ['astro', 'climate', 'eeg', 'stock']


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
        # level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 0)
        filter_data = filter1d.tda(input_signal, level)
    elif filter_name == 'rdp':
        # level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        level = filter1d.__linear_map(filter_level, 0, 1, 1, 0)
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
    metrics["L1 norm"] = measures.l1_norm(input_signal, output_signal)
    metrics["L_inf norm"] = measures.linf_norm(input_signal, output_signal)
    metrics["approx entropy"] = measures.approximate_entropy(output_signal)
    metrics.update(measures.peakiness(input_signal, output_signal))

    return {'input': list(enumerate(input_signal)), 'output': filter_data, 'info': info, 'metrics': metrics}


def get_datasets():
    ret = {}
    for dataset in data_sets:
        cur_ds = []
        for data_file in os.listdir(data_dir + "/" + dataset):
            if fnmatch.fnmatch(data_file, "*.json"):
                cur_ds.append(data_file[:-5])
        ret[dataset] = cur_ds
    return ret


def load_dataset(ds, df):
    filename = data_dir + "/" + ds + "/" + df + ".json"
    with open(filename) as json_file:
        return json.load(json_file)


def valid_dataset(datasets, ds, df):
    return ds in data_sets and df in datasets[ds]


def generate_metric_data(_dataset, _datafile, _filter_name='all', _input_signal=None, quiet=False):
    out_dir = data_dir + '/' + _dataset + '/' + _datafile + '/'
    out_filename = out_dir + _filter_name + '.json'

    if os.path.exists(out_filename):
        with open(out_filename) as json_file:
            return json.load(json_file)

    if not os.path.exists(out_dir):
        if not quiet:
            print("Creating: " + out_dir)
        os.mkdir(out_dir)

    if _input_signal is None:
        _input_signal = load_dataset(_dataset, _datafile)

    results = []
    if _filter_name == 'all':
        for _filter in filter_list:
            results += generate_metric_data(_dataset, _datafile, _filter_name=_filter, _input_signal=_input_signal,
                                            quiet=quiet)
    else:
        process_smoothing(_input_signal, _filter_name, 0)  # warm up
        for i in range(100):
            res = process_smoothing(_input_signal, _filter_name, float(i + 1) / 100)
            res.pop('input')
            res.pop('output')
            results.append(res)

    if not quiet:
        print("Saving: " + out_filename)
    with open(out_filename, 'w') as outfile:
        json.dump(results, outfile, indent=4, separators=(',', ': '))

    return results


def __metric_regression(metrics, fieldX, fieldY):
    x = np.array(list(map((lambda d: d['metrics'][fieldX]), metrics)))
    y = np.array(list(map((lambda d: d['metrics'][fieldY]), metrics)))

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]

    y_intercept = [0, c]
    if m < 0:
        x_intercept = [-c / m, 0]
    else:
        x_intercept = [1, c + m]
    area = (x_intercept[1] + y_intercept[1]) * (x_intercept[0] - y_intercept[0]) / 2
    r2 = abs(np.corrcoef(x, y)[0][1])

    return {'x-intercept': x_intercept,
            'y-intercept': y_intercept,
            'area': area,
            'r^2': r2}


def metric_regression(metrics, fieldX, fieldY):
    metric_reg = {}
    for f in filter_list:
        filtered = list(filter(lambda m: m['info']['filter name'] == f, metrics))
        metric_reg[f] = __metric_regression(filtered, fieldX, fieldY)

    rank = list(metric_reg.keys())
    rank.sort(key=(lambda m: metric_reg[m]['area']))
    for i in range(len(rank)):
        metric_reg[rank[i]]['rank'] = i + 1

    return {'x': fieldX, 'y': fieldY, 'result': metric_reg}
