import math


def solve(data):
    return data.min(), data.max(), math.floor(data.mean())
