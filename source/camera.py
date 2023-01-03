import cv2
import logging
import numpy as np


class CameraCapture:
    def __init__(self, camID) -> None:
        self.camID = camID
        self.videoCapture = cv2.VideoCapture(camID)  # webcam

    def cap(self, process: bool = True) -> np.ndarray:
        """Capture image.

        If process is true, doing process(img)

        Args:
            process (bool, optional): Process image via changing
            color channel, brightness, resizing. Defaults to True.

        Returns:
            cv2 image (np.ndarray): captured image
        """
        success, img = self.videoCapture.read()
        if not success:
            logging.warning("Could not capture image on cam with id %s" % self.camID)

        try:
            img.flags.writeable = False  # google says this will optimize a little bit
        except AttributeError:
            logging.error("Could not capture image on cam with id %s. Maybe this cam don't exists?" % self.camID)
            return np.zeros((1, 1, 3), np.uint8)

        return img

    def get_resolution(self) -> tuple[int, int]:
        """Doing what it says.

        Returns:
            tuple: x and y resolution of camera
        """
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
