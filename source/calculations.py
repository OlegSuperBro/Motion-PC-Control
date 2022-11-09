from math import hypot

def distBeetwenDots(dots: list, dot1: int, dot2: int):
    if dots:
        return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2])
    else:
        return None

def calcDistBySU(dots: list, dot1: int, dot2: int, SU: float = 1):
    if dots and SU:
        return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2]) / SU
    else:
        return None