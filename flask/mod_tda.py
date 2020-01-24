from typing import TypeVar
from operator import itemgetter, attrgetter

T = TypeVar('T')


class DisjointSet:

    def __init__(self) -> None:
        self._data = dict()

    def contains(self, item: T) -> bool:
        return item in self._data

    def find(self, x: T) -> T:
        if not x in self._data:
            self._data[x] = x
        if x != self._data[x]:
            self._data[x] = self.find(self._data[x])
        return self._data[x]

    def union(self, values, x: T, y: T) -> None:
        parent_x, parent_y = self.find(x), self.find(y)
        if values[parent_x] < values[parent_y]:
            self._data[parent_y] = parent_x
        else:
            self._data[parent_x] = parent_y


def extract_cps(data):
    ret = { 0: data[0], (len(data) - 1) : data[-1] }
    for i in range(1, len(data) - 1):
        if data[i] < data[i - 1] and data[i] < data[i + 1]:
            ret[i] = data[i]
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            ret[i] = data[i]
    return ret


def cp_pairs( data ) :
    data_enum = list( enumerate(data) )
    data_enum.sort(key=itemgetter(1))

    pairs = []
    ds = DisjointSet()
    for d in data_enum:
        if ds.contains(d[0] - 1) and ds.contains(d[0] + 1):
            min0 = ds.find(d[0] - 1)
            min1 = ds.find(d[0] + 1)
            if data[min0] < data[min1]:
                pairs.append( { 'c0':min1, 'c1':d[0], 'persistence': (d[1] - data[min1]) } )
            else:
                pairs.append( { 'c0':min0, 'c1':d[0], 'persistence': (d[1] - data[min0]) } )

        ds.find(d[0])
        if ds.contains(d[0] - 1):
            ds.union(data, d[0] - 1, d[0])
        if ds.contains(d[0] + 1):
            ds.union(data, d[0] + 1, d[0])

    return pairs


def filter_cps( data, cps, pairs, threshold ):

    for p in pairs:
        if p['persistence'] < threshold:
            cps.pop(p['c0'])
            cps.pop(p['c1'])

    cps[0] = data[0]
    cps[len(data) - 1] = data[-1]

    new_cps = list(cps.items())
    new_cps.sort(key=itemgetter(0))

    return new_cps
