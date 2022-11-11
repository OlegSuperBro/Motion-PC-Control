from math import hypot

def dist_beetwen_dots(dots: list, dot1: int, dot2: int) -> float:
    if dots:
        return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2])
    else:
        return None

def calc_dist_by_su(dots: list, dot1: int, dot2: int, SU: float = 1) -> float:
    if dots and SU:
        return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2]) / SU
    else:
        return None