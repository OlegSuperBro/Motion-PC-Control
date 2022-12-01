import time
import cv2
import logging
import numpy as np

from settings import settings

import processImage
import appInterface
from camera import CameraCapture


def configure_logs():
    logging.basicConfig(filename='test.log',
                        level=settings.get("LOGS", "LogLevel"),
                        format=settings.get("LOGS", "Format"),
                        datefmt=settings.get("LOGS", "DateFormat"))

    logging.addLevelName(1, "NotImplemented")


def img_draw_fps(img, fps):
    if settings.get("DISPLAY", "ShowOnlyDots"):
        cv2.putText(img=img,
                    text=str(fps),
                    org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=1.5,
                    thickness=2,
                    color=(0, 0, 255))
    else:
        cv2.putText(img=img,
                    text=str(fps),
                    org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=1.5,
                    thickness=2,
                    color=(255, 255, 255))
    return img


def img_draw_hand(img, img_result):
    if img_result:
        if settings.get("DISPLAY", "ShowOnlyDots"):
            img = np.zeros(img.shape, np.uint8)
            img.fill(255)
    processImage.draw_landmarks(img, img_result)
    return img


def main():
    if settings.get("DEBUG", "Debug"):
        UI = appInterface.DebugWind()
    else:
        UI = appInterface.MainWind()

    old_cam_id = -1
    prev_time = 0

    configure_logs()
    settings.update_gestures()
    UI.update_interface()

    while True:
        if old_cam_id != (new_camera_id := settings.get("CAMERA", "ID")):
            camera = CameraCapture(new_camera_id)
            old_cam_id = new_camera_id

        time_elapsed = time.time() - prev_time

        if time_elapsed > 1./settings.get("CAMERA", "MaxFPS"):

            img = camera.cap()

            img_result = processImage.process_image(img)

            if img_result.multi_hand_landmarks:
                for gesture in settings.ACTIVE_GESTURES_CLASSES:
                    if gesture.check(img_result):
                        gesture.action(img_result)

            if settings.get("DISPLAY", "ShowCamera"):
                if settings.get("DISPLAY", "ShowFPS"):
                    current_time = time.time()
                    fps = round(1 / (current_time - prev_time))
                    prev_time = current_time

                    img = img_draw_fps(img, fps)

                img = img_draw_hand(img, img_result)

                UI.update_image(img)

            UI.update()


if __name__ == "__main__":
    main()
