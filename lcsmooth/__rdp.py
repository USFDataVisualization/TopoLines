import numpy as np
from queue import PriorityQueue


def pldist(point, start, end):
    if np.all(np.equal(start, end)):
        return np.linalg.norm(point - start)

    return np.divide(
        np.abs(np.linalg.norm(np.cross(end - start, start - point))),
        np.linalg.norm(end - start))


def __max_dist(M, start_index, last_index, dist=pldist):
    dmax = -1.0
    index = start_index

    for i in range(start_index + 1, last_index):
        d = dist(M[i], M[start_index], M[last_index])
        if d > dmax:
            index = i
            dmax = d
    return index, dmax


def rdp_iter_epsilon(_M, epsilon, dist=pldist):
    if "numpy" in str(type(_M)):
        M = _M
    else:
        M = np.array(_M)

    start_index, last_index = 0, len(M) - 1
    stk = [[start_index, last_index]]
    indices = np.ones(last_index - start_index + 1, dtype=bool)

    while stk:
        start_index, last_index = stk.pop()

        split_index, dmax = __max_dist(M, start_index, last_index, dist)

        if dmax > epsilon:
            stk.append([start_index, split_index])
            stk.append([split_index, last_index])
        else:
            for i in range(start_index + 1, last_index):
                indices[i] = False

    return M[indices]


def rdp_iter_count( _M, max_count, dist=pldist):
    if "numpy" in str(type(_M)):
        M = _M
    else:
        M = np.array(_M)

    pq = PriorityQueue()

    start_index, last_index = 0, len(M) - 1
    split_index, dmax = __max_dist(M, start_index, last_index, dist)
    pq.put((-dmax, [start_index, split_index, last_index]))

    count = 2
    while count < max_count:
        curr = pq.get()[1]

        start_index, split_index, last_index = curr[0], curr[1], curr[2]

        if start_index != split_index:
            sp0, dmax0 = __max_dist(M, start_index, split_index, dist)
            sp1, dmax1 = __max_dist(M, split_index, last_index, dist)

            pq.put((-dmax0, [start_index, sp0, split_index]))
            pq.put((-dmax1, [split_index, sp1, last_index]))

        count += 1

    indices = np.zeros(len(M), dtype=bool)
    while not pq.empty():
        curr = pq.get()[1]

        start_index, split_index, last_index = curr[0], curr[1], curr[2]

        indices[curr[0]] = True
        indices[curr[2]] = True

    return M[indices]
