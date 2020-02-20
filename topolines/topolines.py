import math
from operator import itemgetter
import os
import random
from sklearn.isotonic import IsotonicRegression


__hera_bottleneck = os.getenv('HERA_BOTTLENECK')
__hera_wasserstein = os.getenv('HERA_WASSERSTEIN')

if __hera_bottleneck is None or __hera_wasserstein is None or \
        (not os.path.exists(__hera_bottleneck)) or (not os.path.exists(__hera_wasserstein)):
    print("Path to Hera Bottleneck and Wasserstein not set correctly.")
    print("   For example: ")
    print("       > export HERA_BOTTLENECK=\"/bin/tda/hera/bottleneck_dist\"")
    print("       > export HERA_WASSERSTEIN=\"/bin/tda/hera/wasserstein_dist\"")
    print()
    print("These functionalities will be disabled.")
    __hera_bottleneck = None
    __hera_wasserstein = None


class DisjointSet:

    def __init__(self, key=(lambda k: k)) -> None:
        self._data = dict()
        self._key_func = key

    def contains_item(self, item) -> bool:
        return self._key_func(item) in self._data

    def contains_key(self, key) -> bool:
        return key in self._data

    def put(self, item):
        self._data[self._key_func(item)] = item

    def __find(self, key):
        data_key = self._key_func(self._data[key])
        if key != data_key:
            self._data[key] = self.__find(data_key)
        return self._data[key]

    def find_item(self, item):
        key = self._key_func(item)
        if key not in self._data:
            self._data[key] = item
        return self.__find(key)

    def find_key(self, key):
        if key not in self._data:
            return None
        return self.__find(key)

    def union(self, new_root, old_root) -> None:
        parent_new, parent_old = self.find_item(new_root), self.find_item(old_root)
        self._data[self._key_func(parent_old)] = parent_new


def extract_cps(data):
    ret = []
    b = {'idx': 0, 'val': data[0], 'type': ('min' if (data[0] < data[1]) else 'max')}
    e = {'idx': len(data) - 1, 'val': data[-1], 'type': ('min' if (data[-1] < data[-2]) else 'max')}

    if b['type'] == 'min' and e['type'] == 'min':
        ret.append({'idx': -2, 'val': -float('inf'), 'type': 'min'})
        ret.append({'idx': -1, 'val': float('inf'), 'type': 'max'})
    if b['type'] == 'max':
        ret.append({'idx': -1, 'val': -float('inf'), 'type': 'min'})

    ret.append(b)

    for i in range(1, len(data) - 1):
        if data[i] < data[i - 1] and data[i] <= data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'min'})
        if data[i] >= data[i - 1] and data[i] > data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'max'})

    ret.append(e)
    if e['type'] == 'max':
        ret.append({'idx': len(data), 'val': -float('inf'), 'type': 'min'})

    return ret


def cp_pairs(cps):
    cps_list = list(enumerate(cps))

    # for c in cps_list:
    #    print(str(c[1]['idx']) + " " + c[1]['type'])

    # Init disjoint set with all local mins
    ds = DisjointSet(key=(lambda x: x[0]))
    for c in filter((lambda x: x[1]['type'] == 'min'), cps_list):
        ds.put(c)

    # print(ds._data)
    pairs = []

    # process maxima from lowest to highest
    max_list = list(filter((lambda x: x[1]['type'] == 'max'), cps_list))
    max_list.sort(key=(lambda a: a[1]['val']))
    for c in max_list:
        # print( c )
        # print( str(c[0] - 1) + " " + str(c[0] + 1) + " " + str(len(max_list)) )
        # print( ds._data )
        min0, min1 = ds.find_key(c[0] - 1), ds.find_key(c[0] + 1)
        if min0[1]['val'] < min1[1]['val']:
            minp = min1
            ds.union(min0, min1)
        else:
            minp = min0
            ds.union(min1, min0)

        pairs.append({'c0': minp[1]['idx'], 'c1': c[1]['idx'], 'persistence': (c[1]['val'] - minp[1]['val'])})

    return pairs


def filter_cps_threshold(data, pairs, threshold):
    indices = {0, len(data) - 1}

    for p in filter(lambda pair: pair['persistence'] >= threshold, pairs):
        if 0 <= p['c0'] <= len(data): indices.add(p['c0'])
        if 0 <= p['c1'] <= len(data): indices.add(p['c1'])

    new_cps = list(map(lambda x: [x, data[x]], indices))
    new_cps.sort(key=itemgetter(0))
    return new_cps


def __linear_map(val, in0, in1, out0, out1):
    t = (val - in0) / (in1 - in0)
    return out0 * (1 - t) + out1 * t


def filter_cps_count(data, pairs, count_percent):
    indices = {0, len(data) - 1}

    pairs.sort(key=(lambda pair: pair['persistence']), reverse=True)
    count = math.ceil(__linear_map(count_percent, 0, 1, 1, len(pairs)))

    # print( count )

    for i in range(count):
        p = pairs[i]
        if 0 <= p['c0'] <= len(data): indices.add(p['c0'])
        if 0 <= p['c1'] <= len(data): indices.add(p['c1'])

    new_cps = list(map(lambda x: [x, data[x]], indices))
    new_cps.sort(key=itemgetter(0))
    return new_cps


def filter_tda_threshold(data, threshold):
    cps = extract_cps(data)
    pairs = cp_pairs(cps)
    return filter_cps_threshold(data, pairs, threshold)


def filter_tda_count(data, threshold):
    threshold = min(1, max(0, threshold))
    cps = extract_cps(data)
    pairs = cp_pairs(cps)
    cp_keys = filter_cps_count(data, pairs, threshold)

    tmp = [data[0]]
    for i in range(len(cp_keys) - 1):
        ir = IsotonicRegression(increasing=(cp_keys[i][1] < cp_keys[i + 1][1]))
        y = data[cp_keys[i][0]: cp_keys[i + 1][0] + 1]
        y_ = ir.fit_transform(range(len(y)), y)
        tmp.extend(y_[1:])

    return tmp


def get_persistence_diagram(data):
    dtmp = list(map(lambda d: d + random.uniform(-0.0001, 0.0001), data))
    cps = extract_cps(dtmp)
    pairs = cp_pairs(cps)
    nonzero_pairs = filter(lambda p: not dtmp[p['c0']] == dtmp[p['c1']], pairs)
    return list(map(lambda p: [dtmp[p['c0']], dtmp[p['c1']]], nonzero_pairs))


def save_persistence_diagram(outfile, pd0, pd1=None):
    f = open(outfile, "w")

    for x in pd0:
        f.write(str(x[0]) + " " + str(x[1]) + "\n")

    if pd1 is not None:
        for x in pd1:
            f.write(str(x[0]) + " " + str(x[1]) + "\n")

    f.close()


def wasserstein_distance(pd_file0, pd_file1, rel_error=0.01):
    if __hera_wasserstein is None:
        return 'nan'

    stream = os.popen(__hera_wasserstein + " " + pd_file0 + " " + pd_file1 + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)


def bottleneck_distance(pd_file0, pd_file1, rel_error=0.01):
    if __hera_bottleneck is None:
        return 'nan'

    stream = os.popen(__hera_bottleneck + " " + pd_file0 + " " + pd_file1 + " " + str(rel_error))
    output = stream.read()
    stream.close()
    return float(output)
