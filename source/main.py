import time
import cv2

from camera import CameraCapture
from controller import *
import parser
import processImage
import calculations

# --------SETTINGS-------- #
SHOW_CAM    = True # show cam
SHOW_FPS    = True # show fps (only if SHOW_CAM is true)
MAX_FPS     = 1000

RESTART_GESTURES_ON_SUCCESS = True #

RESIZE_MULT = 1    # multiply image size by this var
BRIGHTNESS  = 1    # image brightness

SU_DOTS = (9, 13)
# you can get all points here:
# https://google.github.io/mediapipe/solutions/hands.html

camera = CameraCapture(1)



# ------GESTURES FORMATING------ #

# First index is priority

# ("statement", func, args)

gestures = \
    {
        0:[
            ("calcDistBySU(dots, 8, 12, SU) < 1.3", mouse_move, () )
        ],
        1:[

        ],
    }

pTime = 0
while True:

    time_elapsed = time.time() - pTime

    if time_elapsed > 1./MAX_FPS:

        img = camera.cap()

        img_result = processImage.fullProcess(img)

        if img_result:
            parser.dots = processImage.handDots(
                img_result,
                CAMERA_SIZE[0],
                CAMERA_SIZE[1]
                )
            
            parser.SU = calculations.distBeetwenDots(
                 parser.dots,
                 SU_DOTS[0],
                 SU_DOTS[1]
            )

            processImage.drawLandmarks(img, img_result)

            parser.parse(gestures, parser.dots, parser.SU)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)

        cv2.waitKey(1)