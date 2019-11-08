import os
import sys
from pprint import pprint

from contest import solve
import numpy as np


def load(data):
    data = [list(map(int, e.split(" "))) for e in data]
    nrows, ncols = data[0]

    queries = []
    for ox, oy, dx, dy in data[2:]:
        queries.append(((ox, oy), (dx, dy)))

    return {
        "nrows": nrows,
        "ncols": ncols,
        "queries": queries
    }

    print(data)
    pass
    # data = [list(map(int, e.split(" "))) for e in data[1:]]
    # grid = np.array([d[::2] for d in data], dtype=int)
    # countries = np.array([d[1::2] for d in data], dtype=int)
    # return {
    #    "grid": grid.T,
    #    "countries": countries.T
    # }


if __name__ == "__main__":
    level, quests = 4, 0
    for q in ["example"] + list(range(1, quests + 1)):
        input_file = r'..\data\level{0}\level{0}_{1}.in'.format(level, q)
        output_file = os.path.splitext(input_file)[0] + ".out"

        with open(input_file, 'r') as fi:
            data = load(fi.read().splitlines())
            if data is None:
                sys.exit(0)
            # pprint(data)

            print("=== Input {}".format(q))
            print("======================")

            result = solve(data)
            pprint(result)

            with open(output_file, 'w+') as fo:
                fo.write(result)
