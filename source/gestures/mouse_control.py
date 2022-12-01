from gestures.baseplate import SimpleGestureBase, settings

import mouse


class MouseControl(SimpleGestureBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self.load()

    def check(self, result, *args, **kwargs) -> bool:
        dots = self.dots_from_result(result)
        if self.dist_beetwen_dots_2d(dots, 8, 12) > 0:
            return True
        else:
            return False

    def action(self, result, *args, **kwargs) -> None:
        dots = self.dots_from_result(result)
        x = dots[8][0] * settings.SCREEN_SIZE[0]
        y = dots[8][1] * settings.SCREEN_SIZE[1]
        mouse.move(x, y)


gestures = {
    "Mouse control": MouseControl()
}

if __name__ == "__main__":
    pass
