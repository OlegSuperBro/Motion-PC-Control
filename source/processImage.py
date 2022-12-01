import numpy as np
import cv2

from settings import settings


def process_image(image: np.ndarray) -> type:
    return settings.MPHAND.process(image)


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


if __name__ == "__main__":
    from camera import CameraCapture

    cam = CameraCapture(1)
    print(cam.get_resolution())
    save_img = np.zeros((500, 500, 3), dtype=np.uint8)
    while True:
        img = cam.cap()

        save_img.fill(255)

        result = process_image(img)
        print(result.multi_hand_landmarks)

        draw_landmarks(img, result)
        draw_landmarks(save_img, result)

        cv2.imwrite("hand.png", save_img)

        cv2.imshow("a", img)
        cv2.waitKey(1)
