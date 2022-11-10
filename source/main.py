import os
import time
import cv2

import calculations
import processImage
from camera import CameraCapture
from controller import *
from settings import *

# ------GESTURES FORMATING------ #

# First index is priority

# ("statement", func, args)

GESTURES = \
        {
            0:[
                ("(calcDistBySU(dots, 8, 12, SU) < 1.3) and \
                (calcDistBySU(dots, 8, 12, SU) < 1.3) and \
                (calcDistBySU(dots, 8, 12, SU) < 1.3) and \
                (calcDistBySU(dots, 8, 12, SU) < 1.3)",
                mouse_move,
                () )
            ],
            1:[

            ],
        }

camera = CameraCapture(CAMERA_ID)

dots = None 
su = None

DEBUG_DOTS = (8, 12)

if DEBUG_MODE:
    def parse(gestures: dict, dots: list, SU: float = 1):
        for key in gestures.keys():
            for line in gestures.get(key):
                try:
                    result = eval(line[0])
                except:
                    return
                if DEBUG_OUTPUT_IF_FALSE or result:
                    print(line[0].replace("                 ", "\n"), "\n", result)
                    print("")

else:
    def parse(gestures: dict, dots: list, SU: float = 1):
        for key in gestures.keys():
            for line in gestures.get(key):
                try:
                    result = eval(line[0])
                except:
                    return
                else:
                    if result:
                        line[1](dots, *line[2])
                        if RESTART_GESTURES_ON_SUCCESS:
                            return

def main():
    pTime = 0        

    while True:

        time_elapsed = time.time() - pTime

        if time_elapsed > 1./MAX_FPS:

            img = camera.cap()

            img_result = processImage.fullProcess(img)

            if img_result:
                dots = processImage.handDots(
                    img_result,
                    CAMERA_SIZE[0],
                    CAMERA_SIZE[1]
                    )
                
                su = calculations.distBeetwenDots(
                    dots,
                    SU_DOTS[0],
                    SU_DOTS[1]
                )

                processImage.drawLandmarks(img, img_result)

                os.system("cls")
                parse(GESTURES, dots, su)

                if DEBUG_MODE:
                    processImage.drawLineBetweenDots(img, dots, DEBUG_DOTS[0], DEBUG_DOTS[1])
                    cv2.putText(img, str(distBeetwenDots(dots, DEBUG_DOTS[0], DEBUG_DOTS[1])), (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    cv2.putText(img, str(calcDistBySU(dots,  DEBUG_DOTS[0], DEBUG_DOTS[1], su)), (10, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            if SHOW_FPS:  
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime  
                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            
            if SHOW_CAM:
                cv2.imshow("Image", img)

            cv2.waitKey(1)

if __name__ == "__main__":
    main()