import cv2

class CameraCapture():

    def __init__(self, camID):
        self.videoCapture = cv2.VideoCapture(camID) # webcam

    def cap(self):
        _, img = self.videoCapture.read()
        img = cv2.flip(img, 1)
        img.flags.writeable = False # google says this will optimize a little bit
        return img
    
    def getResolution(self):
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))