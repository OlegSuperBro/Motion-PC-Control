# TODO: complete this

from gestures.baseplate import SimpleGestureBase

import tkinter as tk
import tkinter.ttk as ttk

from PIL import Image, ImageTk, ImageOps
from typing import Literal
from os.path import dirname, join

dir = dirname(__file__)


class HandRepresentation(tk.Frame):
    def __init__(self, parent, hand: Literal["right", "left"] = "right") -> None:
        super().__init__(parent)

        self.img = Image.open(join(dir, "hand.png"))

        if hand == "left":
            self.img = ImageOps.mirror(self.img)

        tmp_img = ImageTk.PhotoImage(self.img)

        self.hand_img = tk.Label(self, image=tmp_img)
        self.hand_img.image = tmp_img
        self.hand_img.pack()

        self.cords_dots = {
            0: (170, 410),
            1: (120, 400),
            2: (65, 365),
            3: (35, 325),
            4: (5, 295),
            5: (95, 225),
            6: (60, 160),
            7: (40, 120),
            8: (30, 85),
            9: (130, 200),
            10: (120, 110),
            11: (110, 55),
            12: (100, 10),
            13: (170, 200),
            14: (180, 115),
            15: (190, 65),
            16: (200, 20),
            17: (210, 225),
            18: (240, 170),
            19: (260, 130),
            20: (275, 100),
        }

        if hand == "left":
            for key in self.cords_dots.keys():
                self.cords_dots[key] = (140 + (152 - self.cords_dots.get(key)[0]),
                                        self.cords_dots.get(key)[1])

        self.v_dots = {
            0: tk.BooleanVar(),
            1: tk.BooleanVar(),
            2: tk.BooleanVar(),
            3: tk.BooleanVar(),
            4: tk.BooleanVar(),
            5: tk.BooleanVar(),
            6: tk.BooleanVar(),
            7: tk.BooleanVar(),
            8: tk.BooleanVar(),
            9: tk.BooleanVar(),
            10: tk.BooleanVar(),
            11: tk.BooleanVar(),
            12: tk.BooleanVar(),
            13: tk.BooleanVar(),
            14: tk.BooleanVar(),
            15: tk.BooleanVar(),
            16: tk.BooleanVar(),
            17: tk.BooleanVar(),
            18: tk.BooleanVar(),
            19: tk.BooleanVar(),
            20: tk.BooleanVar(),
        }

        self.b_dots = {
            0: ttk.Checkbutton(self),
            1: ttk.Checkbutton(self),
            2: ttk.Checkbutton(self),
            3: ttk.Checkbutton(self),
            4: ttk.Checkbutton(self),
            5: ttk.Checkbutton(self),
            6: ttk.Checkbutton(self),
            7: ttk.Checkbutton(self),
            8: ttk.Checkbutton(self),
            9: ttk.Checkbutton(self),
            10: ttk.Checkbutton(self),
            11: ttk.Checkbutton(self),
            12: ttk.Checkbutton(self),
            13: ttk.Checkbutton(self),
            14: ttk.Checkbutton(self),
            15: ttk.Checkbutton(self),
            16: ttk.Checkbutton(self),
            17: ttk.Checkbutton(self),
            18: ttk.Checkbutton(self),
            19: ttk.Checkbutton(self),
            20: ttk.Checkbutton(self),
        }

        for key in self.b_dots.keys():
            self.b_dots[key].config(text=str(key), variable=self.v_dots[key], onvalue=True, offvalue=False, style="TRadiobutton", )
            self.b_dots[key].place(x=self.cords_dots[key][0], y=self.cords_dots[key][1])

    def get_active(self) -> list:
        return [key[0] for key in self.v_dots.items() if key[1].get()]


class DebugGesture(SimpleGestureBase):
    def __init__(self) -> None:
        super().__init__()

    def interface_debug(self, parent, *args, **kwargs) -> None:
        self.debug_outputs_tab = ttk.Frame(parent)
        self.debug_outputs_tab.pack(anchor="nw")

        self.v_display_distance = tk.BooleanVar()

        self.b_display_distance = ttk.Checkbutton(self.debug_outputs_tab, variable=self.v_display_distance, onvalue=True, offvalue=False)
        self.b_display_distance.pack(side="top", anchor="nw")

        self.hands_tab = ttk.Notebook(parent)
        self.hands_tab.pack(anchor="nw")

        self.left_hand_tab = ttk.Frame(self.hands_tab)
        self.left_hand_tab.pack(anchor="nw")
        self.hands_tab.add(self.left_hand_tab, text="Left")

        self.left_hand = HandRepresentation(self.left_hand_tab, hand="left")
        self.left_hand.pack(side="top", anchor="nw")

        self.right_hand_tab = ttk.Frame(self.hands_tab)
        self.right_hand_tab.pack(anchor="nw")
        self.hands_tab.add(self.right_hand_tab, text="Right")

        self.right_hand = HandRepresentation(self.right_hand_tab)
        self.right_hand.pack(side="top", anchor="nw")

        parent.add(self.debug_outputs_tab, text="Debug outputs")
        parent.add(self.hands_tab, text="Hands dots")

        return "Debug"


gestures = {
    "Debug gesture": DebugGesture(),
}
