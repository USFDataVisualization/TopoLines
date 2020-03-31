import math
from operator import itemgetter
import random
from sklearn.isotonic import IsotonicRegression
from topolines.DisjointSet import DisjointSet


def __linear_map(val, in0, in1, out0, out1):
    t = (val - in0) / (in1 - in0)
    return out0 * (1 - t) + out1 * t


def __extract_cps(data):
    ret = []

    b = {'idx': 0, 'val': data[0], 'type': ('min' if (data[0] < data[1]) else 'max')}
    if b['type'] == 'min': ret.append({'idx': -1, 'val': math.inf, 'type': 'max'})
    if b['type'] == 'max': ret.append({'idx': -1, 'val': -math.inf, 'type': 'min'})
    ret.append(b)

    for i in range(1, len(data) - 1):
        if data[i] < data[i - 1] and data[i] <= data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'min'})
        if data[i] >= data[i - 1] and data[i] > data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'max'})

    e = {'idx': len(data) - 1, 'val': data[-1], 'type': ('min' if (data[-1] < data[-2]) else 'max')}
    ret.append(e)
    if e['type'] == 'min': ret.append({'idx': len(data), 'val': math.inf, 'type': 'max'})
    if e['type'] == 'max': ret.append({'idx': len(data), 'val': -math.inf, 'type': 'min'})

    return ret


def __pair_cps(cps):
    pairs = []

    cps_max = list( filter( (lambda c: c['type'] == 'max'), cps ) )
    cps_max.sort(key=(lambda c: c['val']))

    proc = list(cps)
    for c in cps_max:
        if len(proc) == 1: break

        idx = proc.index(c)
        if idx == 0: rem = proc[idx+1]
        elif idx == len(proc)-1: rem = proc[idx-1]
        elif proc[idx-1]['val'] > proc[idx+1]['val']: rem = proc[idx-1]
        else: rem = proc[idx+1]

        pairs.append({'c0': c['idx'], 'c1': rem['idx'], 'persistence': (c['val']-rem['val'])})
        proc.remove( rem )
        proc.remove( c )

    pairs.sort(key=itemgetter('persistence'))

    return pairs


def __rebuild(data, filtered_pairs):
    indices = {0, len(data) - 1}

    for p in filtered_pairs:
        if 0 < p['c0'] < len(data)-1: indices.add(p['c0'])
        if 0 < p['c1'] < len(data)-1: indices.add(p['c1'])

    cp_keys = list(map(lambda x: [x, data[x]], indices))
    cp_keys.sort(key=itemgetter(0))

    tmp = [data[0]]
    for i in range(len(cp_keys) - 1):
        ir = IsotonicRegression(increasing=(cp_keys[i][1] < cp_keys[i + 1][1]))
        y = data[cp_keys[i][0]: cp_keys[i + 1][0] + 1]
        y_ = ir.fit_transform(range(len(y)), y)
        tmp.extend(y_[1:])

    return tmp


def filter_tda_threshold(data, threshold):
    cps = __extract_cps(data)
    pairs = __pair_cps(cps)
    filtered_pairs = filter(lambda p: p['persistence'] >= threshold, pairs)
    return __rebuild(data, filtered_pairs)


def filter_tda_count(data, threshold):
    threshold = min(1, max(0, threshold))
    cps = __extract_cps(data)
    pairs = __pair_cps(cps)
    count = math.ceil(__linear_map(threshold, 0, 1, len(pairs)-1, 0))
    return __rebuild(data, pairs[count:])


def get_persistence_diagram(data):
    dtmp = list(map(lambda d: d + random.uniform(-0.0001, 0.0001), data))
    cps = __extract_cps(dtmp)
    pairs = __pair_cps(cps)
    nonzero_pairs = filter(lambda p: p['persistence']>0 and not math.isinf(p['persistence']), pairs)
    return list(map(lambda p: [dtmp[p['c0']], dtmp[p['c1']]], nonzero_pairs))

