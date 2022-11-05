import mediapipe as mp
import cv2
import numpy as np

from math import hypot

class CapturedImage():

    mpHands = mp.solutions.hands
    mpDraw  = mp.solutions.drawing_utils
    mpHand  = mpHands.Hands(static_image_mode        = False, # It's video stream, you dumbass
                            max_num_hands            = 2,     
                            min_detection_confidence = 0.7,
                            min_tracking_confidence  = 0.5)

    def __init__(self, image: np.ndarray):
        self.image   = image
        self.result  = self.processImage()

    def processImage(self, brightness = 1):
        return self.mpHand.process(
            cv2.cvtColor(
                cv2.convertScaleAbs(self.image, alpha = brightness, beta = 0), 
                cv2.COLOR_BGR2RGB
                )
            )

    def handDots(self):
        dotList = []

        if self.result.multi_hand_landmarks:
            for handLandmark in self.result.multi_hand_landmarks:
                for test_id, lm in enumerate(handLandmark.landmark):
                    h, w, _ = self.image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    dotList.append([test_id, cx, cy])

        return dotList

    def drawLandmarks(self):
        if self.result.multi_hand_landmarks:
            for handLandmark in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(self.image, handLandmark, self.mpHands.HAND_CONNECTIONS)

    def distBeetwenDots(self, dot1: int, dot2: int):
        dots = self.handDots()
        if dots:
            return hypot(dots[dot1][1]-dots[dot2][1], dots[dot1][2] - dots[dot2][2])
        else:
            return None