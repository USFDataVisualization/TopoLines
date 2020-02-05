from typing import TypeVar
from operator import itemgetter, attrgetter

T = TypeVar('T')


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
        if data[i] < data[i - 1] and data[i] < data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'min'})
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            ret.append({'idx': i, 'val': data[i], 'type': 'max'})

    ret.append(e)
    if e['type'] == 'max':
        ret.append({'idx': len(data), 'val': -float('inf'), 'type': 'min'})

    return ret


def cp_pairs(cps):
    cps_list = list(enumerate(cps))

    for c in cps_list:
        print(str(c[1]['idx']) + " " + c[1]['type'])

    # Init disjoint set with all local mins
    ds = DisjointSet(key=(lambda x: x[0]))
    for c in list(filter((lambda x: x[1]['type'] == 'min'), cps_list)):
        ds.put(c)

    # print(ds._data)
    pairs = []

    # process maxima from lowest to highest
    max_list = list(filter((lambda x: x[1]['type'] == 'max'), cps_list))
    max_list.sort(key=(lambda a: a[1]['val']))
    for c in max_list:
        min0, min1 = ds.find_key(c[0] - 1), ds.find_key(c[0] + 1)
        if min0[1]['val'] < min1[1]['val']:
            minp = min1
            ds.union(min0, min1)
        else:
            minp = min0
            ds.union(min1, min0)

        pairs.append({'c0': minp[1]['idx'], 'c1': c[1]['idx'], 'persistence': (c[1]['val'] - minp[1]['val'])})

    return pairs


def filter_cps(data, pairs, threshold):
    indices = {0, len(data) - 1}

    for p in pairs:
        if p['persistence'] > threshold:
            if 0 <= p['c0'] <= len(data): indices.add(p['c0'])
            if 0 <= p['c1'] <= len(data): indices.add(p['c1'])

    new_cps = list(map(lambda x: [x, data[x]], indices))

    return new_cps.sort(key=itemgetter(0))



def filter_tda(data, threshold):
    cps = extract_cps(data)
    pairs = cp_pairs(cps)
    return filter_cps(data, pairs, threshold)
