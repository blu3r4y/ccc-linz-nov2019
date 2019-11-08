import numpy as np
from collections import defaultdict
from scipy.spatial.distance import euclidean


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


def get_borders(countries):
    borders = defaultdict(lambda: np.zeros_like(countries))

    for (x, y), cid in np.ndenumerate(countries):
        edge = is_edge(x, y, countries.shape)
        nids = neighbours_values(x, y, countries)

        border = any([nid != cid for nid in nids])
        borders[cid][x, y] = edge or border

    return dict(borders)


def get_country_area_coords(countries, borders, cid):
    area = (countries == cid)
    area = area - borders[cid]
    return area.astype(int)


def get_closest(countries, borders, cid, cx, cy):
    distances = np.full_like(countries, np.inf, dtype=float)
    valid = get_country_area_coords(countries, borders, cid)
    for (x, y) in np.argwhere(valid == 1):
        distances[x, y] = euclidean([x, y], [cx, cy])

    minima = np.argwhere(distances == distances.min())
    closest = sorted(minima, key=lambda xy: (xy[1], xy[0]))[0]  # row, column
    return closest


def solve(data):
    _grid, _countries = data["grid"], data["countries"]
    num_countries = len(np.unique(_countries))
    _borders = get_borders(_countries)

    capitals = []

    for cid in range(num_countries):
        country_coords = np.argwhere(_countries == cid)
        cx, cy = np.floor(np.average(country_coords, axis=0)).astype(int)

        on_border = _borders[cid][cx, cy]  # == 1
        outside = _countries[cx, cy] != cid

        if on_border or outside:
            cx, cy = get_closest(_countries, _borders, cid, cx, cy)

        capitals.append((cx, cy))

        # print(cid, "--", cx, cy, on_border)

    return "\n".join([f"{x} {y}" for x, y in capitals])
