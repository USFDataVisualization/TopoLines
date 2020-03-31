import math
from operator import itemgetter
from DisjointSet import DisjointSet


class MergeTree:
    """class that holds a merge tree"""

    def __init__(self, points, edges):

        self.h0 = {}
        for p in points:
            self.h0[p['index']] = [p['time'], math.inf]

        djs = DisjointSet()
        edges.sort(key=itemgetter('time'))

        for d in edges:
            i0, i1 = d['p0']['index'], d['p1']['index']
            f0, f1 = djs.find(i0), djs.find(i1)
            if f0 != f1:
                djs.union(f0, f1)
                self.h0[f0][1] = d['time']

        self.h0 = list(map((lambda h: {'index': h, 'life': self.h0[h], 'persistence': (self.h0[h][1] - self.h0[h][0])}),
                           self.h0.keys()))
        self.h0 = list(filter((lambda h: h['persistence'] > 0), self.h0))
        self.h0.sort(key=itemgetter('persistence'))
