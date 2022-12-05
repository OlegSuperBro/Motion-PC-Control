from math import hypot
from numpy import ndarray
import logging

from settings import settings


class SimpleGestureBase:
    def __init__(self) -> None:
        pass

    def dots_from_result(self, result) -> None:
        dotList = []
        for handLandmark in result.multi_hand_landmarks:
            for test_id, lm in enumerate(handLandmark.landmark):
                cx, cy, cz = lm.x, lm.y, lm.z
                dotList.append([cx, cy, cz])
        return dotList

    def dist_beetwen_dots_2d(self, dots, dot1: int, dot2: int) -> float:
        if dots:
            return hypot(dots[dot1][0] - dots[dot2][0],
                         dots[dot1][1] - dots[dot2][1])
        else:
            return None

    def dist_beetwen_dots_3d(self, dots, dot1: int, dot2: int) -> float:
        if dots:
            return hypot((dots[dot2][0] - dots[dot1][0]) ** 2 +
                         (dots[dot2][1] - dots[dot1][1]) ** 2 +
                         (dots[dot2][2] - dots[dot1][2]) ** 2)
        else:
            return None

    def dist_beetwen_dots_with(self, dots, dot1: int, dot2: int) -> float:
        # TODO: return distance in standartised(?) unit
        pass

    def action(self, result, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"action\"")

    def check(self, result, *args, **kwargs) -> bool:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"check\"")

    def process_image(self, image, *args, **kwargs) -> ndarray:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"process_image\"")
        return image

    def interface_settings(self, parent, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"interface_settings\"")

    def interface_debug_settings(self, parent, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"interface_debug_settings\"")

    def interface_debug(self, parent, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"interface_debug\"")

    def debug(self, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"debug\"")

    def save(self, *args, **kwargs) -> dict:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"save\"")

    def load(self, *args, **kwargs) -> None:
        logging.log(logging.getLevelName("NotImplemented"),
                    str(type(self).__name__) + " don't have \"load\"")


class AdvancedGestureBase:
    # TODO: a lot of work with this cool shit
    def __init__(self) -> None:
        raise NotImplementedError("This type of gesture not implemented yet.")


gestures = {}

if __name__ == "__main__":
    pass
