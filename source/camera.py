import cv2
import logging
import numpy as np

from settings import settings


class Image(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def resize_image(self, multiply: float = None, size: tuple[int, int] = None) -> None:
        """Doing what it says.

        Args:
            image (cv2 image (np.ndarray)): image to resize.
            multiply (float, optional): multiply x and y by this value.
            Defaults to ResizeMultiplier setting.
            size (tuple[int, int], optional): resize image to exact size.
            If not provided used \"multiply\" option Defaults to None.
        """

        if size:
            return Image(cv2.resize(self, size))
        elif multiply:
            return Image(cv2.resize(self,
                                    (round(self.get_size[1] * multiply),
                                    round(self.get_size[0] * multiply))))

    def change_color_channel(self, color_channel: str = cv2.COLOR_BGR2RGB) -> None:
        """Change color channel."""
        return Image(cv2.cvtColor(self, color_channel))

    def change_brightness(self,
                          _alpha: float = 1,
                          _beta: float = 1) -> None:
        """Doing what it says.

        Args:
            _alpha (int, optional): brightness. Defaults to \"Brightness\" setting.
            _beta (int, optional): contrast. Defaults to 1.
        """

        return Image(cv2.convertScaleAbs(self, alpha=_alpha, beta=_beta))

    def flip(self, flip_code: int = 1):
        return Image(cv2.flip(self, flip_code))

    def put_text(self,
                 text,
                 org: tuple[int, int] = (0, 0),
                 fontFace: int = cv2.FONT_HERSHEY_PLAIN,
                 fontScale: float = 1,
                 thickness: float = 1,
                 color: list[int, int, int] = [255, 255, 255]) -> None:

        color = list(color)
        color.reverse()
        return Image(cv2.putText(self,
                                 text=str(text),
                                 org=org,
                                 fontFace=fontFace,
                                 fontScale=fontScale,
                                 thickness=thickness,
                                 color=color
                                 ))

    def get_size(self) -> tuple[int, int]:
        """ Doing what it says

        Returns:
            tuple: x and y resolution of image
        """
        return self.shape()[:2]


class CameraCapture:
    def __init__(self, camID) -> None:
        self.camID = camID
        self.videoCapture = cv2.VideoCapture(camID)  # webcam

    def cap(self, process: bool = True) -> Image:
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
            return Image(np.zeros((1, 1, 3), np.uint8))

        return Image(img)

    def get_resolution(self) -> tuple[int, int]:
        """Doing what it says.

        Returns:
            tuple: x and y resolution of camera
        """
        return (self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))


if __name__ == "__main__":
    cam = CameraCapture(1)
    while True:
        img = cam.cap()
        cv2.imshow("a", img)
        cv2.waitKey(1)
