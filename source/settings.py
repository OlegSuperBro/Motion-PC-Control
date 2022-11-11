import configparser
from os import listdir
from pyautogui import size
import mediapipe as mp

from camera import CameraCapture

class Config(configparser.ConfigParser):

    GESTURES = dict
        
    SCREEN_WIDTH, SCREEN_HEIGHT = size()

    mpHands = mp.solutions.hands
    mpDraw  = mp.solutions.drawing_utils
    

    def __init__(self) -> None:
        super().__init__()

        if "settings.ini" not in listdir():
            self["CAMERA"] = {
                "ID": 1,
                "Brightness": 1,
                "MaxFPS": 1000,
            }
            self["DISPLAY"] = {
                "ShowCamera": True,
                "ShowFPS": True,
                "ResizeMultiplier": 1,
            }
            self["DETECTION"] = {
                "MaxHands": 2,
                "DetectionConfidence": 0.7,
                "TrackingConfidence": 0.5,
            }
            self["GENERAL"] = {
                "RestartGesturesOnSuccess": True,
                "SuDots": (9, 13),
            }
            self["DEBUG"] = {
                "Debug": False,
                "OutputIfFalse": False,
            }
            self["GESTURES"] = {
                0:[
                    ("True",
                    "print",
                    "(\"\\nYou forgot to add gestures. Please, download from my github page or make the by yourself. Don't forget to remove this gesture\")" ),
                ],
                
            }

            self.save()
        
        else:
            self.read("settings.ini")

        self.update()

    def save(self) -> None:
        self.write(open("settings.ini", "w"))

    def update(self) -> None:
        self.DEBUG_MODE = self.getboolean("DEBUG", "Debug")
        self.DEBUG_OUTPUT_IF_FALSE = self.getboolean("DEBUG", "OutputIfFalse")

        self.CAMERA_ID   = self.getint("CAMERA", "ID")
        self.BRIGHTNESS  = self.getint("CAMERA", "Brightness")    # image brightness
        self.MAX_FPS     = self.getint("CAMERA", "MaxFPS")
        
        self.SHOW_CAM    = self.getboolean("DISPLAY", "ShowCamera")
        self.SHOW_FPS    = self.getboolean("DISPLAY", "ShowFPS")
        self.RESIZE_MULT = self.getint("DISPLAY", "ResizeMultiplier")    # multiply image size by this var

        self.RESTART_GESTURES_ON_SUCCESS = self.getboolean("GENERAL", "RestartGesturesOnSuccess")

        self.SU_DOTS = eval(self.get("GENERAL", "SuDots"))

        self.MAX_HANDS = self.getint("DETECTION", "MaxHands")
        self.DETECTION_CONFIDENCE = self.getfloat("DETECTION", "DetectionConfidence")
        self.TRACKING_CONFIDENCE = self.getfloat("DETECTION", "TrackongConfidence")

        self.MPHAND  = self.mpHands.Hands(static_image_mode        = False, # It's video stream, you dumbass
                            max_num_hands            = self.MAX_HANDS,     
                            min_detection_confidence = self.DETECTION_CONFIDENCE,
                            min_tracking_confidence  = self.TRACKING_CONFIDENCE)


        camera = CameraCapture(self.CAMERA_ID)
        
        self.CAMERA_SIZE = camera.get_resolution()

        self.MOUSE_MULT_WIDTH  = round(self.SCREEN_WIDTH / self.CAMERA_SIZE[0])
        self.MOUSE_MULT_HEIGHT = round(self.SCREEN_HEIGHT / self.CAMERA_SIZE[1])

    def update_gestures(self):
        self.GESTURES = {}

        key = 0

        while True:
            try:
                # priority
                self.GESTURES[key] = []
                for value in eval(self.get("GESTURES", str(key))):
                    try:
                        self.GESTURES[key].append((value[0], eval(value[1]), [eval(value[2])]))
                    except NameError as e:
                        exec(eval(str(e).split()[1]) + "= None")
                        self.GESTURES[key].append((value[0], eval(value[1]), [eval(value[2])]))

            except configparser.NoOptionError:
                _ = self.GESTURES.pop(key)
                break
            key += 1

settings = Config()

from controller import *

settings.update_gestures()
