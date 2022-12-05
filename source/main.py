import time
import cv2
import logging
import numpy as np

from settings import settings

import appInterface
from camera import CameraCapture


def draw_landmarks(image: np.ndarray, result) -> None:
    if result.multi_hand_landmarks:
        for handLandmark in result.multi_hand_landmarks:
            settings.MPDRAW.draw_landmarks(image,
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


def process_image(image: np.ndarray) -> type:
    return settings.MPHAND.process(image)


def configure_logs():
    logging.basicConfig(filename='test.log',
                        level=settings.get("LOGS", "LogLevel"),
                        format=settings.get("LOGS", "Format"),
                        datefmt=settings.get("LOGS", "DateFormat"))

    logging.addLevelName(1, "NotImplemented")


def img_draw_fps(img, fps):
    if settings.get("DISPLAY", "ShowOnlyDots"):
        return img.put_text(text=fps,
                            org=(0, 20),
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=1.5,
                            thickness=2,
                            color=(0, 0, 255),
                            )
    else:
        return img.put_text(text=fps,
                            org=(0, 20),
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=1.5,
                            thickness=2,
                            color=(255, 255, 255))


def img_draw_hand(img, img_result):
    if img_result:
        if settings.get("DISPLAY", "ShowOnlyDots"):
            img.fill(255)
    draw_landmarks(img, img_result)
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
            img = img.change_color_channel(cv2.COLOR_BGR2RGB)
            img = img.flip()

            img_result = process_image(img)

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


if __name__ == "__main__":
    main()
