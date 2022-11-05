import time
import cv2

from dummy import dummy
from camera import CameraCapture
import processImage

# --------SETTINGS-------- #
SHOW_CAM    = True # show cam
SHOW_FPS    = True # show fps (only if SHOW_CAM is true)
MAX_FPS     = 1000

RESIZE_MULT = 1    # multiply image size by this var
BRIGHTNESS  = 1    # image brightness

SU_POINTS = (0, 5)
# you can get all points here:
# https://google.github.io/mediapipe/solutions/hands.html

camera = CameraCapture(1)

CAMERA_SIZE = (
            camera.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
            camera.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            )

img_result = dummy()
img_result.multi_hand_landmarks = None

print("Please, show your hands on comfort distance from camera")
while not img_result.multi_hand_landmarks:
    img = camera.cap()
    img_result = processImage.fullProcess(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()

SU = processImage.distBeetwenDots(
        processImage.handDots(
            img_result,
            CAMERA_SIZE[0],
            CAMERA_SIZE[1]
            ),
        SU_POINTS[0],
        SU_POINTS[1]
        
        )

print(SU)

pTime = 0

while True:

    time_elapsed = time.time() - pTime

    if time_elapsed > 1./MAX_FPS:

        img = camera.cap()

        img_result = processImage.fullProcess(img)

        if img_result:
            processImage.drawLandmarks(img, img_result)
            dist = processImage.distBeetwenDots(processImage.handDots(img_result, CAMERA_SIZE[0], CAMERA_SIZE[1]), 8, 5)
            print("NO SU = ", dist)
            print("SU    =", processImage.calcSU(dist, SU))


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)

        cv2.waitKey(1)