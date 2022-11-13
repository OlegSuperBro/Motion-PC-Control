import cv2
import numpy as np

class CameraCapture:

    def __init__(self, camID) -> None:
        self.videoCapture = cv2.VideoCapture(camID) # webcam

    def cap(self) -> np.ndarray:
        _, img = self.videoCapture.read()
        img = cv2.flip(img, 1)
        img.flags.writeable = False # google says this will optimize a little bit
        return img
    
    def get_resolution(self) -> list:
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))