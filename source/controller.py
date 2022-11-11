import mouse

from calculations import *
from settings import settings

def mouse_move(dots, mous_mult_width = settings.MOUSE_MULT_WIDTH, mouse_mult_height = settings.MOUSE_MULT_HEIGHT, *args) -> None:
    x = dots[12][1] * mous_mult_width
    y = dots[12][2] * mouse_mult_height
    mouse.move(x, y)

    return
