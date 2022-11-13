import os
import time
import cv2

from settings import settings

import calculations
import processImage
from camera import CameraCapture
from controller import *

camera = CameraCapture(settings.CAMERA_ID)

dots = None 
su = None # standart unit

if settings.DEBUG_MODE:
    def parse(gestures: dict, dots: list, SU: float = 1) -> None:
        for key in gestures.keys():
            for line in gestures.get(key):
                try:
                    result = eval(line[0])
                except:
                    return
                if settings.DEBUG_OUTPUT_IF_FALSE or result:
                    print(line[0].replace("                 ", "\n"), "\n", result)
                    print("")

else:
    def parse(gestures: dict, dots: list, SU: float = 1) -> None:
        for key in gestures.keys():
            for line in gestures.get(key):
                try:
                    result = eval(line[0])
                except Exception:
                    return
                else:
                    if result:
                        line[1](dots, *line[2])
                        if settings.RESTART_GESTURES_ON_SUCCESS:
                            return

def main():
    pTime = 0

    while True:

        time_elapsed = time.time() - pTime

        if time_elapsed > 1./settings.MAX_FPS:

            img = camera.cap()

            img_result = processImage.full_process(img)

            if img_result:
                dots = processImage.hand_dots(
                    img_result,
                    settings.CAMERA_SIZE[0],
                    settings.CAMERA_SIZE[1]
                    )
                
                su = calculations.dist_beetwen_dots(
                    dots,
                    settings.SU_DOTS[0],
                    settings.SU_DOTS[1]
                )

                processImage.draw_landmarks(img, img_result)

                os.system("cls")
                parse(settings.GESTURES, dots, su)

            if settings.SHOW_FPS:  
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime  
                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            
            if settings.SHOW_CAM:
                if settings.DEBUG_MODE:
                    processImage.draw_line_between_dots(img, dots, settings.settings.DEBUG_DOTS[0], settings.DEBUG_DOTS[1])
                    cv2.putText(img, str(dist_beetwen_dots(dots, settings.DEBUG_DOTS[0], settings.DEBUG_DOTS[1])), (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    cv2.putText(img, str(calc_dist_by_su(dots,  settings.DEBUG_DOTS[0], settings.DEBUG_DOTS[1], su)), (10, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                cv2.imshow("Image", img)

            cv2.waitKey(1)

if __name__ == "__main__":
    main()