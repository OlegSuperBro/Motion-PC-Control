import pyautogui as pygui
import mouse

from calculations import *
from camera import CameraCapture

camera = CameraCapture(1)

SCREEN_WIDTH, SCREEN_HEIGHT  = pygui.size()

CAMERA_SIZE = camera.getResolution()

MOUSE_MULT_WIDTH  = round(SCREEN_WIDTH / CAMERA_SIZE[0])
MOUSE_MULT_HEIGHT = round(SCREEN_HEIGHT / CAMERA_SIZE[1])

def mouse_move(dots, mous_mult_width = MOUSE_MULT_WIDTH, mouse_mult_height = MOUSE_MULT_HEIGHT):
    x = dots[12][1] * mous_mult_width
    y = dots[12][2] * mouse_mult_height
    mouse.move(x, y)
