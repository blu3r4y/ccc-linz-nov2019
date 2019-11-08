import numpy as np
from collections import defaultdict
from scipy.spatial.distance import euclidean
import math


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
    closest = sorted(minima, key=lambda xy: (xy[1], xy[0]))[0]  # row, column sort (but transposed)
    return closest


def get_dominance(direction):  # 0: x, 1: y
    dx, dy = direction
    if dx > dy:
        return 0
    elif dy > dx:
        return 1
    else:
        return 0


def iter_in_dominance(cells, dominance):  # 0: x, 1: y
    if dominance == 1:
        return sorted(cells, key=lambda e: (e[0], e[1]))
    else:
        return sorted(cells, key=lambda e: (e[1], e[0]))


def gasser_kahlhofer(origin, direction, shape):
    ox, oy = origin
    dx, dy = direction

    maxx, maxy = shape

    cells = {(int(math.floor(ox)), int(math.floor(oy)))}

    px = int(math.ceil(ox))
    while px < maxx:
        lmb = (px - ox) / dx
        py = oy + lmb * dy

        is_cross = py % 1 == 0
        py = int(math.floor(py))

        if py >= maxy:
            break

        cells.add((px, py))
        if is_cross:
            cells.add((px, py - 1))

        px += 1

    py = int(math.ceil(oy))
    while py < maxy:
        lmb = (py - oy) / dy
        px = ox + lmb * dx

        is_cross = px % 1 == 0
        px = int(math.floor(px))

        if px >= maxx:
            break

        cells.add((px, py))
        if is_cross:
            cells.add((px - 1, py))

        py += 1

    # lmb = (px - ox) / dx
    # lmb = (py - oy) / dy

    # px = ox + lmb * dx
    # py = oy + lmb * dy

    return list(cells)


def solve(data):
    nrows, ncols, queries = data["nrows"], data["ncols"], data["queries"]

    solutions = []

    for query in queries:
        origin, direction = query
        origin = (origin[0] + 0.5, origin[1] + 0.5)
        gk = gasser_kahlhofer(origin, direction, [nrows, ncols])
        itered = iter_in_dominance(gk, get_dominance(direction))
        solutions.append(itered)

    return "\n".join([" ".join([f"{x} {y}" for x, y in xy]) for xy in solutions])
