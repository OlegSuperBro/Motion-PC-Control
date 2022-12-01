import json
import mediapipe as mp
import logging

from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH

from os import listdir
from pyautogui import size

from importlib import import_module

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
                            "GENERAL": {

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

        self.update_vars()

    def update_vars(self) -> None:
        """Configure settings that can't be saved or useless for saving."""
        self.MPHAND = self.MPHANDS.Hands(static_image_mode=False,
                                         max_num_hands=self.get("DETECTION", "MaxHands"),
                                         min_detection_confidence=self.get("DETECTION", "DetectionConfidence"),
                                         min_tracking_confidence=self.get("DETECTION", "TrackingConfidence"))

        self.CAMERA_SIZE = (int(VideoCapture(self.get("CAMERA", "ID")).get(CAP_PROP_FRAME_WIDTH)),
                            int(VideoCapture(self.get("CAMERA", "ID")).get(CAP_PROP_FRAME_HEIGHT)))

    def update_gestures(self) -> None:
        # TODO: Import gestures if them presented as list

        """Basically just re-importing all gestures and if them in
        \"active\" list add class to \"settings.ACTIVE_GESTURE_CLASSES\"."""

        self.ACTIVE_GESTURES_CLASSES = []
        for gesture_module in get_gestures():
            import_module("gestures." + gesture_module)
            try:
                gestures_dict = eval("gestures." + gesture_module + ".gestures")

            except AttributeError:
                print(gesture_module + " don't have \"gestures\" list.")
                logging.warning(gesture_module + " don't have \"gestures\" list.")

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

    def set(self, value: any, *dir: str) -> None:
        """Set an value in settings

        Args:
            value (any): value to set
            *dir: directory to setting ("OPTION1", "OPTION2", ...)

        """
        command = "self.settings"
        for i in dir:
            command += f"[\"{i}\"]"
        exec(command + " = value")


settings = Config()

if __name__ == "__main__":
    # print("gestures." + get_gestures()[0])

    # import_module("gestures." + get_gestures()[0])

    # print(dir(eval("gestures." + get_gestures()[0])))
    # print(getmembers({ "gestures." + get_gestures()[0]], isclass))

    print(settings.get("GESTURES", "Active"))
    print(settings.ACTIVE_GESTURES_CLASSES)
    print(settings.get("GESTURES", "NotActive"))
