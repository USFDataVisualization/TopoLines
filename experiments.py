import fnmatch
import os
import time

import simplejson as json
import numpy as np

import math

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
        min_level = math.exp(0)
        max_level = math.exp(1)
        scaled_level = filter1d.__linear_map(filter_level, 0, 1, min_level, max_level)
        level = filter1d.__linear_map(math.log(scaled_level), 0, 1, 0, 1.0)
        filter_data = filter1d.cutoff(input_signal, level)
    elif filter_name == 'subsample':
        min_level = math.exp(0)
        max_level = math.exp(1)
        scaled_level = filter1d.__linear_map(filter_level, 0, 1, min_level, max_level)
        level = filter1d.__linear_map(math.log(scaled_level), 0, 1, 0, 1.0)
        filter_data = filter1d.subsample(input_signal, level)
    elif filter_name == 'tda':
        min_level = math.log(1)
        max_level = math.log(100)
        scaled_level = filter1d.__linear_map(filter_level, 1, 0, min_level, max_level)
        level = filter1d.__linear_map(math.exp(scaled_level), 1, 100, 0, 1.0)
        # level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        # level = filter1d.__linear_map(filter_level, 0, 1, 1, 0)
        filter_data = filter1d.tda(input_signal, level)
    elif filter_name == 'rdp':
        # level = filter1d.__linear_map(filter_level, 0, 1, 0, input_range)
        # level = filter1d.__linear_map(filter_level, 0, 1, 1, 0)
        min_level = math.log(1)
        max_level = math.log(100)
        scaled_level = filter1d.__linear_map(filter_level, 1, 0, min_level, max_level)
        level = filter1d.__linear_map(math.exp(scaled_level), 1, 100, 0, 1.0)
        filter_data = filter1d.rdp(input_signal, level)
    elif filter_name == 'gaussian':
        min_level = math.log(0.1)
        max_level = math.log(len(input_signal) * 0.1)
        scaled_level = filter1d.__linear_map(filter_level, 0, 1, min_level, max_level)
        level = math.exp(scaled_level)
        # level = filter1d.__linear_map(filter_level, 0, 1, 0.1, len(input_signal)*0.1 )
        filter_data = filter1d.gaussian(input_signal, level)
    elif filter_name == 'median':
        min_level = math.log(1)
        max_level = math.log(len(input_signal) * 0.1)
        scaled_level = filter1d.__linear_map(filter_level, 0, 1, min_level, max_level)
        level = math.exp(scaled_level)
        # level = filter1d.__linear_map(filter_level, 0, 1, 1, len(input_signal)*0.1)
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

    precomp_dir = 'docs/json/results/' + _dataset + '/' + _datafile + '/'
    if not os.path.exists('docs/json/results/'):
        os.mkdir('docs/json/results/')
    if not os.path.exists('docs/json/results/' + _dataset + '/'):
        os.mkdir('docs/json/results/' + _dataset + '/')
    if not os.path.exists(precomp_dir):
        os.mkdir(precomp_dir)

    if _input_signal is None:
        _input_signal = load_dataset(_dataset, _datafile)

    results = []
    if _filter_name == 'all':
        for _filter in filter_list:
            results += generate_metric_data(_dataset, _datafile, _filter_name=_filter, _input_signal=_input_signal,
                                            quiet=quiet)
    else:
        if not os.path.exists(precomp_dir + _filter_name + '/'):
            os.mkdir(precomp_dir + _filter_name + '/')
        res = process_smoothing(_input_signal, _filter_name, 0)  # warm up
        with open(precomp_dir + _filter_name + '/level_0.json', 'w') as outfile:
            json.dump(res, outfile)

        for i in range(100):
            res = process_smoothing(_input_signal, _filter_name, float(i + 1) / 100)

            with open(precomp_dir + _filter_name + '/level_' + str(i+1) + '.json', 'w') as outfile:
                json.dump(res, outfile)

            res.pop('input')
            res.pop('output')
            results.append(res)

    if not quiet:
        print("Saving: " + out_filename)
    with open(out_filename, 'w') as outfile:
        json.dump(results, outfile, indent=4, separators=(',', ': '))

    return results


def __metric_regression(metrics, fieldX, fieldY, xmax, ymax):
    x = np.array(list(map((lambda d: d['metrics'][fieldX]), metrics)))
    y = np.array(list(map((lambda d: d['metrics'][fieldY]), metrics)))

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]

    r2 = abs(np.corrcoef(x, y)[0][1])

    x0 = [0, c]
    x1 = [xmax, m * xmax + c]

    if x0[1] < 0: x0 = [-c / m, 0]
    if x1[1] < 0: x1 = [-c / m, 0]

    area = (x0[1] + x1[1]) * (x1[0] - x0[0]) / 2

    # print(area)

    # if x0[1] > ymax: x0 = [(ymax - c) / m, ymax]
    # if x1[1] > ymax: x1 = [(ymax - c) / m, ymax]

    return {'points': [x0, x1],
            'area': area,
            'r^2': r2}


def metric_regression(metrics, fieldX, fieldY):
    metric_reg = {}

    xmax = max(map((lambda d: d['metrics'][fieldX]), metrics))
    ymax = max(map((lambda d: d['metrics'][fieldY]), metrics))

    for f in filter_list:
        filtered = list(filter(lambda m: m['info']['filter name'] == f, metrics))
        metric_reg[f] = __metric_regression(filtered, fieldX, fieldY, xmax, ymax)

    rank = list(metric_reg.keys())
    rank.sort(key=(lambda m: metric_reg[m]['area']))
    for i in range(len(rank)):
        metric_reg[rank[i]]['rank'] = i + 1

    return {'x': fieldX, 'y': fieldY, 'result': metric_reg}


def __sort_ds(a, b):
    if a['dataset'] < b['dataset']: return -1
    if a['dataset'] > b['dataset']: return 1
    if a['datafile'] < b['datafile']: return -1
    if a['datafile'] > b['datafile']: return 1


def metric_ranks(datasets):
    res = []
    measures = ['L1 norm','L_inf norm', 'peak wasserstein', 'peak bottleneck']

    for ds in datasets:

        overall = {}
        for m in measures:
            overall[m] = dict.fromkeys(filter_list, 0 )

        for df in datasets[ds]:
            metric_data = generate_metric_data(ds, df)

            metric_reg = {}
            for m in measures:
                metric_tmp = metric_regression(metric_data, 'approx entropy', m)
                metric_reg[m] = metric_tmp['result']
                for f in filter_list:
                    overall[m][f] += metric_tmp['result'][f]['rank']

            res.append({'dataset': ds, 'datafile': df, 'rank': metric_reg})

        for m in measures:
            keys = list(overall[m].keys())
            keys.sort( key=(lambda a: overall[m][a]) )
            for f in filter_list:
                overall[m][f] = {'rank':keys.index(f)+1,'r^2':1}

        res.append( {'dataset': ds+'_z', 'datafile': 'overall', 'rank': overall } )

    res.sort(key=(lambda a: (a['dataset'] + "_" + a['datafile']).lower() ))

    return res


if __name__ == "__main__":

    datasets = get_datasets()
    with open("docs/json/datasets.json", 'w') as outfile:
        json.dump(datasets, outfile)

    for _ds in datasets:
        for _df in datasets[_ds]:
            metric_data = generate_metric_data(_ds, _df)
            metric_reg = [metric_regression(metric_data, 'approx entropy', 'L1 norm'),
                          metric_regression(metric_data, 'approx entropy', 'L_inf norm'),
                          metric_regression(metric_data, 'approx entropy', 'peak wasserstein'),
                          metric_regression(metric_data, 'approx entropy', 'peak bottleneck')]
            with open("docs/json/metric/" + _ds + '_' + _df + ".json", 'w') as outfile:
                json.dump({'metric': metric_data, 'rank': metric_reg}, outfile)

    with open("docs/json/all_ranks.json", 'w') as outfile:
        json.dump(metric_ranks(datasets), outfile)
