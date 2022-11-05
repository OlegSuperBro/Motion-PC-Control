import time
import cv2

from camera import CameraCapture

# --------SETTINGS-------- #
MAX_FPS = 1000



camera = CameraCapture(maxfps = MAX_FPS)

pTime = 0

while True:

    time_elapsed = time.time() - pTime

    if time_elapsed > 1./MAX_FPS:

        img = camera.cap()

        img.drawLandmarks()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img.image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img.image)

        cv2.waitKey(1)