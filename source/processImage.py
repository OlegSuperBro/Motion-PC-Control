import mediapipe as mp
import cv2

import numpy as np

from math import hypot

mpHands = mp.solutions.hands
mpDraw  = mp.solutions.drawing_utils
mpHand  = mpHands.Hands(static_image_mode        = False, # It's video stream, you dumbass
                        max_num_hands            = 2,     
                        min_detection_confidence = .7,
                        min_tracking_confidence  = .5)

def resizeImage(image: np.ndarray):
    pass

def changeColorChannel(image: np.ndarray):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def changeBrightness(image: np.ndarray, _alpha: int = 1, _beta: int = 0):
    return cv2.convertScaleAbs(image, alpha = _alpha, beta = _beta) 

def processImage(image: np.ndarray):
    return mpHand.process(image)

def fullProcess(image: np.ndarray, _alpha: int = 1, _beta: int = 0):
    return processImage(
        changeColorChannel(
            changeBrightness(
                image, _alpha, _beta
            )
        )
    )

def drawLandmarks(image: np.ndarray, result):
    if result.multi_hand_landmarks:
        for handLandmark in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(image, handLandmark, mpHands.HAND_CONNECTIONS)

def handDots(result, image_width, image_height):
    dotList = []

    if result.multi_hand_landmarks:
        for handLandmark in result.multi_hand_landmarks:
                for test_id, lm in enumerate(handLandmark.landmark):
                    cx, cy = int(lm.x * image_width), int(lm.y * image_height)
                    dotList.append([test_id, cx, cy])
        return dotList
    
    return None 

def distBeetwenDots(dots: list, dot1: int, dot2: int):
    if dots:
        return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2])
    else:
        return None

def calcSU(dist: int, SU: float = 1):
    if dist and SU:
        return dist / SU
    else:
        return None
