from typing import Iterable


class DisjointSet:
    """class that holds a disjoint set"""

    def __init__(self, items: Iterable = [], key=(lambda x: x)) -> None:
        self._data = dict()
        self._key_func = key
        for item in items:
            self._data[self._key_func(item)] = item

    def contains(self, item) -> bool:
        return self._key_func(item) in self._data

    def put(self, item):
        self._data[self._key_func(item)] = item

    def find(self, item):
        key = self._key_func(item)
        if key not in self._data:
            self._data[key] = item
        elif item != self._data[key]:
            self._data[key] = self.find(self._data[key])
        return self._data[key]

    def union(self, old_parent, new_parent) -> None:
        parent0, parent1 = self.find(old_parent), self.find(new_parent)
        self._data[self._key_func(parent0)] = parent1
        return parent1
