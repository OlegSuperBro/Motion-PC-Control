import json
import mediapipe as mp
import logging

from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH

from os import listdir
from pyautogui import size

import importlib.util

import gestures
from gestures.init import get_gestures


class Config():

    SCREEN_SIZE = size()

    MPHANDS = mp.solutions.hands
    MPDRAW = mp.solutions.drawing_utils

    def __init__(self) -> None:

        if "settings.json" not in listdir():
            self.settings = {"DEBUG": {
                                "Debug": False,
                                "OutputIfFalse": False,
                                "LogLevel": 0
                            },
                            "CAMERA": {
                                "ID": 1,
                                "Brightness": 1,
                                "ResizeMultiplier": 1,
                                "MaxFPS": 60,
                            },
                            "DISPLAY": {
                                "ShowCamera": True,
                                "ShowOnlyDots": False,
                                "ShowFPS": True,
                            },
                            "DETECTION": {
                                "MaxHands": 2,
                                "DetectionConfidence": 0.7,
                                "TrackingConfidence": 0.5,
                            },
                            "LOGS": {
                                "Format": "%(asctime)s:%(msecs)d - %(levelname)s - %(filename)s - %(message)s",
                                "DateFormat": "%H:%M:%S",
                                "LogLevel": 20
                            },
                            "GESTURES": {
                                "Active": [],
                                "NotActive": []
            }}

        else:
            self.settings = json.load(open("settings.json"))

    def update_camera_size(self, camera) -> None:
        self.CAMERA_SIZE = camera.get_resolution()

    def update_hands(self) -> None:
        """Configure settings that can't be saved or useless for saving."""
        self.MPHAND = self.MPHANDS.Hands(static_image_mode=False,
                                         max_num_hands=self.get("DETECTION", "MaxHands"),
                                         min_detection_confidence=self.get("DETECTION", "DetectionConfidence"),
                                         min_tracking_confidence=self.get("DETECTION", "TrackingConfidence"))

    def update_gestures(self) -> None:
        # TODO: Import gestures if them presented as list
        # that means if there more then 1 gesture then it should add all classes in list
        # can be useful for separeted gestures like
        # mouse_move and mouse_click

        """Basically just re-importing all gestures and if them in
        \"active\" list add class to \"settings.ACTIVE_GESTURE_CLASSES\"."""

        self.ACTIVE_GESTURES_CLASSES = []
        for gesture_module_name in get_gestures():
            gesture_module_spec = importlib.util.spec_from_file_location("gesture", gesture_module_name)
            gesture_module = importlib.util.module_from_spec(gesture_module_spec)
            gesture_module_spec.loader.exec_module(gesture_module)
            try:
                gestures_dict = gesture_module.gestures

            except AttributeError:
                print(gesture_module_name + " don't have \"gestures\" list.")
                logging.warning(gesture_module_name + " don't have \"gestures\" list.")

            else:
                for gesture in gestures_dict.items():
                    if (gesture[0] in self.get("GESTURES", "Active")
                       and gesture[1] not in self.ACTIVE_GESTURES_CLASSES):

                        self.ACTIVE_GESTURES_CLASSES.append(gesture[1])

                    elif (gesture[0] not in self.get("GESTURES", "Active")
                          and gesture[0] not in self.get("GESTURES", "NotActive")):

                        self.settings["GESTURES"]["NotActive"] = self.get("GESTURES", "NotActive") + [gesture[0]]

                    else:
                        pass

    def save(self) -> None:
        """Saves all settings in \"settings.json\" file."""
        json.dump(self.settings, open("settings.json", "w"), indent=4)

    def read(self, file) -> None:
        if file:
            self.settings = json.load(open(file))

    def get(self, *values: str) -> any:
        """Returns an saved setting, if required value don't exist,
        log an error and return none

        Args:
            *values: directory to setting ("OPTION1", "OPTION2", ...)

        Returns:
            any: Saved setting in \"values\" dir
        """
        value = self.settings
        for key in values:
            try:
                value = value.get(key)
            except KeyError:
                logging.error("Trying to get setting that don't exist: %s" % ".".join())
                return
        return value

    def set(self, value: any, *dirs: str) -> bool:
        """Set an value in settings and return True if changed

        Args:
            value (any): value to set
            *dir: directory to setting ("OPTION1", "OPTION2", ...)

        Returns:
            bool: True if changed, False otherwise
        """
        command = "self.settings"
        changed = False
        for i in dir:
            command += f"[\"{i}\"]"
        if eval(command) != value:
            changed = True
        exec(command + " = value")
        return changed


settings = Config()
