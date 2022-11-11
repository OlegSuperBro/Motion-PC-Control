import numpy as np
import cv2

from settings import settings



def resize_image(image: np.ndarray) -> np.ndarray:
    return
    #cv2.resize(image)

def change_color_channel(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def change_brightness(image: np.ndarray, _alpha: int = 1, _beta: int = 0) -> np.ndarray:
    return cv2.convertScaleAbs(image, alpha = _alpha, beta = _beta) 

def process_image(image: np.ndarray) -> type:
    return settings.mpHand.process(image)

def full_process(image: np.ndarray, _alpha: int = 1, _beta: int = 0) -> type:
    return process_image(
        change_color_channel(
            change_brightness(
                image, _alpha, _beta
            )
        )
    )

def draw_landmarks(image: np.ndarray, result) -> None:
    if result.multi_hand_landmarks:
        for handLandmark in result.multi_hand_landmarks:
            settings.mpDraw.draw_landmarks(image, handLandmark, settings.mpHands.HAND_CONNECTIONS)

def hand_dots(result, image_width, image_height) -> list:

    if result.multi_hand_landmarks:
        dotList = []
        for handLandmark in result.multi_hand_landmarks:
                for test_id, lm in enumerate(handLandmark.landmark):
                    cx, cy = int(lm.x * image_width), int(lm.y * image_height)
                    dotList.append([test_id, cx, cy])
        return dotList
    
    return None

def draw_line_between_dots(img:np.ndarray, dots: list, dot1: int, dot2: int) -> None:
    if dots:
        x1, y1 = dots[dot1][1], dots[dot1][2]
        x2, y2 = dots[dot2][1], dots[dot2][2]
        
        cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
