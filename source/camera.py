import cv2

from captured_image import CapturedImage

class CameraCapture():

    videoCapture = cv2.VideoCapture(1) # video capture
    currentFPS   = 0 

    def __init__(self, maxfps: int = 60, showfps: bool = True):
        self.maxFPS   = maxfps
        self.showFPS  = showfps
        self.image    = self.cap()

    def cap(self):
        _, img = self.videoCapture.read()
        img = cv2.flip(img, 1)
        img.flags.writeable = False
        return CapturedImage(img)
    
    def getResolution(self):
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))