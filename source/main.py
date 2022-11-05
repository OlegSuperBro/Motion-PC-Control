import time
import cv2

from camera import CameraCapture
import processImage

# --------SETTINGS-------- #
SHOW_CAM    = True # show cam
SHOW_FPS    = True # show fps (only if SHOW_CAM is true)
MAX_FPS     = 1000

RESIZE_MULT = 1    # multiply image size by this var
BRIGHTNESS  = 1    # image brightness

camera = CameraCapture()
pTime = 0

while True:

    time_elapsed = time.time() - pTime

    if time_elapsed > 1./MAX_FPS:

        img = camera.cap()

        img_result = processImage.fullProcess(img)

        if img_result:
            processImage.drawLandmarks(img, img_result)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)

        cv2.waitKey(1)