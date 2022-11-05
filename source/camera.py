import cv2

from captured_image import CapturedImage

class CameraCapture():

    videoCapture = cv2.VideoCapture(1) # webcam

    def __init__(self):
        self.image    = self.cap()

    def cap(self):
        _, img = self.videoCapture.read()
        img = cv2.flip(img, 1)
        img.flags.writeable = False # google says this will optimize a little bit
        return CapturedImage(img)
    
    def getResolution(self):
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))