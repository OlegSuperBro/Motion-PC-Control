import cv2
import logging
import numpy as np

from settings import settings


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
            logging.warning("Could not capture image on cam with id %s. Maybe this cam don't exists?" % self.camID)
            return np.zeros((1, 1, 3), np.uint8)

        if process:
            tmp_img = img
            tmp_img = self.change_color_channel(tmp_img)
            tmp_img = self.change_brightness(tmp_img, settings.get("CAMERA", "Brightness"))
            tmp_img = self.resize_image(tmp_img, settings.get("CAMERA", "ResizeMultiplier"))
            img = tmp_img

        img = cv2.flip(img, 1)

        return img

    def get_resolution(self) -> tuple[int, int]:
        """Doing what it says.

        Returns:
            list: x and y resolution of camera
        """
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def resize_image(self,
                     image: np.ndarray,
                     multiply: float = None,
                     size: tuple[int, int] = None) -> np.ndarray:
        """Doing what it says.

        Args:
            image (cv2 image (np.ndarray)): image to resize.
            multiply (float, optional): multiply x and y by this value.
            Defaults to ResizeMultiplier setting.
            size (tuple[int, int], optional): resize image to exact size.
            If not provided used \"multiply\" option Defaults to None.

        Returns:
            cv2 image (np.ndarray): resized image.
        """

        if size:
            return cv2.resize(image, size)
        elif multiply:
            return cv2.resize(image,
                              (round(image.shape[1] * multiply),
                               round(image.shape[0] * multiply)))
        else:
            return image

    def change_color_channel(self, image: np.ndarray) -> np.ndarray:
        """Change color channel for better hands recognition.

        Args:
            image (cv2 image (np.ndarray)): image to process

        Returns:
            cv2 image (np.ndarray): processed image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def change_brightness(self,
                          image: np.ndarray,
                          _alpha: float = 1,
                          _beta: float = 1) -> np.ndarray:
        """Doing what it says.

        Args:
            image (cv2 image (np.ndarray)): image to procees
            _alpha (int, optional): brightness. Defaults to \"Brightness\" setting.
            _beta (int, optional): idk what is this. Defaults to 1.

        Returns:
            cv2 image (np.ndarray): processed image.
        """

        return cv2.convertScaleAbs(image, alpha=_alpha, beta=_beta)


if __name__ == "__main__":
    pass
    # cam = CameraCapture(1)
    # print(cam.cap().shape)
