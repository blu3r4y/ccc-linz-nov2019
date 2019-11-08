import numpy as np


def neighbours(x, y):
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    neigh = [(x + dx, y + dy) for dx, dy in offsets]
    return neigh


def neighbours_values(x, y, grid):
    if is_edge(x, y, grid.shape):
        return [-1]
    return [grid[nx, ny] for nx, ny in neighbours(x, y)]


def is_edge(x, y, shape):
    return x == 0 or y == 0 or (x == shape[0] - 1) or (y == shape[1] - 1)


def solve(data):
    _gr, _co = data["grid"], data["countries"]
    _grs = _gr.shape
    num_countries = len(np.unique(_co))

    num_borders = [0] * num_countries

    for (x, y), cid in np.ndenumerate(_co):
        edge = is_edge(x, y, _grs)
        nids = neighbours_values(x, y, _co)

        border = any([nid != cid for nid in nids])

        num_borders[cid] += edge or border

    return "\n".join(map(str, num_borders))
