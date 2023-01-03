import time
import cv2
import logging
import numpy as np

from settings import settings

import appInterface
from camera import CameraCapture


def draw_landmarks(img: np.ndarray, result) -> None:
    if result.multi_hand_landmarks:
        for handLandmark in result.multi_hand_landmarks:
            settings.MPDRAW.draw_landmarks(img,
                                           handLandmark,
                                           settings.MPHANDS.HAND_CONNECTIONS)


def draw_line_between_dots(img: np.ndarray,
                           dots: list,
                           dot1: int,
                           dot2: int) -> None:
    if dots:
        x1, y1 = dots[dot1][1], dots[dot1][2]
        x2, y2 = dots[dot2][1], dots[dot2][2]

        cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)


def process_image(img: np.ndarray) -> np.ndarray:
    tmp_img = img

    tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2RGB)
    tmp_img = cv2.flip(tmp_img, 1)
    tmp_img = cv2.convertScaleAbs(tmp_img, alpha=settings.get("CAMERA", "Brightness"), beta=1)

    resize_mult = settings.get("CAMERA", "ResizeMultiplier")
    tmp_img = cv2.resize(tmp_img, (int(tmp_img.shape[1]*resize_mult), int(tmp_img.shape[0]*resize_mult)))

    return tmp_img


def configure_logs():
    logging.basicConfig(filename='logs.log',
                        level=settings.get("LOGS", "LogLevel"),
                        format=settings.get("LOGS", "Format"),
                        datefmt=settings.get("LOGS", "DateFormat"))

    logging.addLevelName(1, "NotImplemented")


def img_draw_fps(img, fps):
    if settings.get("DISPLAY", "ShowOnlyDots"):
        return cv2.putText(img,
                           text=str(fps),
                           org=(0, 20),
                           fontFace=cv2.FONT_HERSHEY_PLAIN,
                           fontScale=1.5,
                           thickness=2,
                           color=(0, 0, 255),
                           )
    else:
        return cv2.putText(img,
                           text=str(fps),
                           org=(0, 20),
                           fontFace=cv2.FONT_HERSHEY_PLAIN,
                           fontScale=1.5,
                           thickness=2,
                           color=(255, 255, 255))


def img_draw_hand(img, img_result):
    if settings.get("DISPLAY", "ShowOnlyDots"):
        img.fill(255)
    draw_landmarks(img, img_result)
    return img


if __name__ == "__main__":
    if settings.get("DEBUG", "Debug"):
        UI = appInterface.DebugWind()
    else:
        UI = appInterface.MainWind()

    old_cam_id = -1
    prev_time = 0

    configure_logs()
    settings.update_gestures()
    settings.update_hands()
    UI.update_interface()

    while True:
        if old_cam_id != (new_camera_id := settings.get("CAMERA", "ID")):
            camera = CameraCapture(new_camera_id)
            settings.update_camera_size(camera)
            old_cam_id = new_camera_id

        time_elapsed = time.time() - prev_time

        if time_elapsed > 1./settings.get("CAMERA", "MaxFPS"):

            img = camera.cap()

            img = process_image(img)

            img_result = settings.MPHAND.process(img)

            if settings.get("DISPLAY", "ShowCamera"):
                img = img_draw_hand(img, img_result)

                if settings.get("DISPLAY", "ShowFPS"):
                    current_time = time.time()
                    fps = round(1 / (current_time - prev_time))
                    prev_time = current_time

                    img = img_draw_fps(img, fps)

        tmp_img = img
        for gesture in settings.ACTIVE_GESTURES_CLASSES:
            if img_result.multi_hand_landmarks:
                if gesture.check(img_result):
                    gesture.action(img_result)
            tmp_img = gesture.process_image(tmp_img)

        UI.update_image(tmp_img)

        UI.update()
