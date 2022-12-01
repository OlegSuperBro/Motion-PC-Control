import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog

import tkinter.scrolledtext as ScrolledText

from PIL import Image, ImageTk
import logging

from camera import CameraCapture
from settings import settings


class PickWidget(tk.Frame):
    def __init__(self, parent,
                 left_text: str = "Left",
                 right_text: str = "Right",
                 left_vars: list = [],
                 right_vars: list = [],):
        super().__init__(parent)

        self.left_list_vars = left_vars
        self.right_list_vars = right_vars

        self.left_side = tk.LabelFrame(self, text=left_text)
        self.left_side.pack(anchor="nw", side="left")

        self.left_list_scrollbar = tk.Scrollbar(self.left_side)

        self.left_list = tk.Listbox(self.left_side, yscrollcommand=self.left_list_scrollbar.set)
        self.left_list.pack(anchor="nw", side="left")
        self.update_listbox(self.left_list, self.left_list_vars)
        self.left_list_scrollbar.config(command=self.left_list.yview)

        self.middle_buttons = tk.Frame(self)
        self.middle_buttons.pack(anchor="w", side="left")

        self.move_to_right_button = tk.Button(self.middle_buttons, text="->", command=self.move_selection_to_right)
        self.move_to_right_button.pack()

        self.move_to_left_button = tk.Button(self.middle_buttons, text="<-", command=self.move_selection_to_left)
        self.move_to_left_button.pack()

        self.right_side = tk.LabelFrame(self, text=right_text)
        self.right_side.pack(anchor="nw", side="left")

        self.right_list_scrollbar = tk.Scrollbar(self.right_side)

        self.right_list = tk.Listbox(self.right_side, yscrollcommand=self.right_list_scrollbar.set)
        self.right_list.pack(anchor="nw", side="left")
        self.update_listbox(self.right_list, self.right_list_vars)
        self.right_list_scrollbar.config(command=self.right_list.yview)

    def update_listbox(self, parent: tk.Listbox, list_: list = []) -> int:
        elements = 0
        parent.delete(0, "end")
        try:
            for var in list_:
                parent.insert("end", var)
                elements += 1
        except IndexError:
            logging.warning("You don't have any gestures installed.")

        return elements

    def get_selection(self, parent: tk.Listbox):
        return parent.curselection()

    def move_in_list(self, from_: list, to: list, element: int):
        try:
            to.append(from_.pop(element))
        except IndexError:
            logging.error("This gesture don't exist in this list")

    def move_selection_to_right(self):
        selected = self.get_selection(self.left_list)
        for element in selected:
            self.move_in_list(self.left_list_vars, self.right_list_vars, element)

        self.update_both_listbox()

    def move_selection_to_left(self):
        selected = self.get_selection(self.right_list)
        for element in selected:
            self.move_in_list(self.right_list_vars, self.left_list_vars, element)

        self.update_both_listbox()

    def update_both_lists(self, left_vars, right_vars):
        self.left_list_vars = left_vars
        self.right_list_vars = right_vars

    def update_both_listbox(self):
        self.update_listbox(self.left_list, self.left_list_vars)
        self.update_listbox(self.right_list, self.right_list_vars)

    def get_all_left(self):
        return self.left_list_vars

    def get_all_right(self):
        return self.right_list_vars


class ScaleWithText(tk.Frame):
    def __init__(self,
                 parent,
                 variable=None,
                 from_=0,
                 to=1,
                 length=100,
                 digits=1,
                 resolution=1,
                 orient="horizontal",
                 text: str = ""):
        super().__init__(parent)

        self.label = tk.Label(self, text=text)
        self.label.pack(anchor="nw")

        self.scale = tk.Scale(self,
                              variable=variable,
                              from_=from_,
                              to=to,
                              length=length,
                              digits=digits,
                              resolution=resolution,
                              orient=orient)
        self.scale.pack(anchor="nw")

    def get(self):
        return self.scale.get()


class EntryWithText(tk.Frame):
    def __init__(self,
                 parent,
                 label: str = "",
                 default="",
                 var_type="str") -> None:
        super().__init__(parent)

        self.label = tk.Label(self, text=label)
        self.label.pack(side="left", )

        self.var_type = var_type

        self.entry = tk.Entry(self,
                              validate="key",
                              validatecommand=(parent.register(self.validate),
                                               '%P'))
        self.entry.pack(side="left", )
        self.entry.insert(0, str(default))

    def get(self):
        if self.var_type in (int, float) and self.entry.get() == "":
            return 0
        else:
            return self.var_type(self.entry.get())

    def validate(self, value):
        if value == "":
            return True

        if (value and " " not in value):
            try:
                self.var_type(value)
                return True
            except ValueError:
                return False
        else:
            return False


class Camera(tk.Frame):
    def __init__(self, parent, no_cam_text: str = "NO CAM") -> None:
        super().__init__(parent)

        self.image = tk.Label(self)
        self.image.pack()

        self.no_cam_text = tk.Label(self, text=no_cam_text)

    def disable_camera(self) -> None:
        self.image.pack_forget()
        self.no_cam_text.pack()

    def enable_camera(self) -> None:
        self.no_cam_text.pack_forget()
        self.image.pack()

    def update_image(self, new_image) -> None:
        img = Image.fromarray(new_image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.image.imgtk = imgtk
        self.image.configure(image=imgtk)


class TextHandler(logging.Handler):
    # I'm lazy, so i just copied this from stackoverflow and added something
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    class DuplicateFilter(object):
        def __init__(self):
            self.msgs = set()

        def filter(self, record):
            if False and record.levelno == 1:
                rv = record.msg not in self.msgs
                self.msgs.add(record.msg)
                return rv
            else:
                return True

    def __init__(self, text_widget, msg_format: str = None, date_format: str = None):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text_widget = text_widget

        self.setFormatter(logging.Formatter(msg_format, date_format))

        self.addFilter(self.DuplicateFilter())

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text_widget.insert("end", msg + "\n")

            # Autoscroll to the bottom
            self.text_widget.yview("end")
        self.text_widget.after(0, append)


class Logs(tk.LabelFrame):
    def __init__(self, parent, level: any = 0, format: str = None, date_format: str = None) -> None:
        super().__init__(parent)

        self.config(text="Logs")

        self.logs = ScrolledText.ScrolledText(self)
        self.logs.pack(expand=True, fill="both")

        self.logs.bind("<Key>", lambda _: "break")

        self.logs.config(height=10)

        logger = logging.getLogger()

        logger.addHandler(TextHandler(self.logs, format, date_format))
        logger.setLevel(level)


class BetterCheckbox(ttk.Checkbutton):
    def __init__(self, parent, state: bool = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        if state:
            self.state(["!alternate", "selected"])
        else:
            self.state(["!alternate", "!selected"])

    def get(self):
        if self.instate(["selected"]):
            return True
        else:
            return False


class SettingsWind(tk.Tk):
    def __init__(self, parent_wind=None) -> None:
        super().__init__()

        self.parent_wind = parent_wind

        self.geometry("500x500")

        self.settings_tabs = ttk.Notebook(self)
        self.settings_tabs.pack(anchor="nw")

        # Settings for camera
        self.camera_settings_tab = tk.Frame(self.settings_tabs)

        self.b_camera_id = EntryWithText(self.camera_settings_tab,
                                         label="Camera ID:",
                                         default=settings.get("CAMERA", "ID"),
                                         var_type=int)
        self.b_camera_id.pack(anchor="nw")

        self.b_brightness = ScaleWithText(self.camera_settings_tab,
                                          from_=0,
                                          to=5,
                                          length=400,
                                          digits=3,
                                          resolution=0.01,
                                          orient="horizontal",
                                          text="Brightness")
        self.b_brightness.scale.set(settings.get("CAMERA", "Brightness"))
        self.b_brightness.pack(anchor="nw", pady=10)

        self.b_resize_mult = ScaleWithText(self.camera_settings_tab,
                                           from_=0.1,
                                           to=2,
                                           length=400,
                                           digits=2,
                                           resolution=0.1,
                                           orient="horizontal",
                                           text="Resize multiplier")
        self.b_resize_mult.scale.set(settings.get("CAMERA", "ResizeMultiplier"))
        self.b_resize_mult.pack(anchor="nw", pady=10)

        self.b_max_fps = ScaleWithText(self.camera_settings_tab,
                                       from_=1,
                                       to=120,
                                       length=400,
                                       digits=3,
                                       resolution=1,
                                       orient="horizontal",
                                       text="Max FPS")
        self.b_max_fps.scale.set(settings.get("CAMERA", "MaxFPS"))
        self.b_max_fps.pack(anchor="nw", pady=10)

        # Setings for display
        self.display_settings_tab = tk.Frame(self.settings_tabs)

        self.b_show_cam = BetterCheckbox(self.display_settings_tab,
                                         state=settings.get("DISPLAY", "ShowCamera"),
                                         text="Show camera",
                                         onvalue=True,
                                         offvalue=False)
        self.b_show_cam.pack(anchor="nw")

        self.b_show_only_dots = BetterCheckbox(self.display_settings_tab,
                                               state=settings.get("DISPLAY", "ShowOnlyDots"),
                                               text="Show only dots (useful for privacy)",
                                               onvalue=True,
                                               offvalue=False)
        self.b_show_only_dots.pack(anchor="nw")

        self.b_show_fps = BetterCheckbox(self.display_settings_tab,
                                         state=settings.get("DISPLAY", "ShowFPS"),
                                         text="Show FPS",
                                         onvalue=True,
                                         offvalue=False)
        self.b_show_fps.pack(anchor="nw")

        # Settings for detection
        self.detection_settings_tab = tk.Frame(self.settings_tabs)

        self.b_max_hands = EntryWithText(self.detection_settings_tab,
                                         label="Max hands:",
                                         default=settings.get("DETECTION", "MaxHands"),
                                         var_type=int)
        self.b_max_hands.pack(anchor="nw")

        self.b_detection_confidence = ScaleWithText(self.detection_settings_tab,
                                                    from_=0.1,
                                                    to=1,
                                                    length=400,
                                                    digits=3,
                                                    resolution=0.01,
                                                    orient="horizontal",
                                                    text="Detection confidence")
        self.b_detection_confidence.scale.set(settings.get("DETECTION", "DetectionConfidence"))
        self.b_detection_confidence.pack(anchor="nw")

        self.b_tracking_confidence = ScaleWithText(self.detection_settings_tab,
                                                   from_=0.1,
                                                   to=1,
                                                   length=400,
                                                   digits=3,
                                                   resolution=0.01,
                                                   orient="horizontal",
                                                   text="Tracking confidence")
        self.b_tracking_confidence.scale.set(settings.get("DETECTION", "TrackingConfidence"))
        self.b_tracking_confidence.pack(anchor="nw")

        ttk.Button(self.detection_settings_tab, text="Update hands", command=settings.update_hands).pack(side="right", anchor="se")

        # Gestures selecting
        self.gestures_settings_tab = tk.Frame(self.settings_tabs)

        self.b_changing_gestures_state = PickWidget(self.gestures_settings_tab,
                                                  left_text="Inactive",
                                                  right_text="Active",
                                                  left_vars=settings.get("GESTURES", "NotActive"),
                                                  right_vars=settings.get("GESTURES", "Active"),)
        self.b_changing_gestures_state.pack(anchor="nw")
        ttk.Button(self.gestures_settings_tab, text="Update Gestures", command=settings.update_gestures).pack(side="right", anchor="se")

        # add all tabs in settings_tabs
        self.settings_tabs.add(self.camera_settings_tab, text="Camera")
        self.settings_tabs.add(self.display_settings_tab, text="Display")
        self.settings_tabs.add(self.detection_settings_tab, text="Detection")

        self.settings_tabs.add(self.gestures_settings_tab, text="Gestures")

        # save button
        ttk.Button(self, text="Save", command=settings.save).pack(side="right", anchor="se", padx=3, pady=3)

        self.apply_settings()

    def apply_settings(self) -> None:
        settings.set(self.b_camera_id.get(), "CAMERA", "ID")
        settings.set(self.b_brightness.get(), "CAMERA", "Brightness")
        settings.set(self.b_max_fps.get(), "CAMERA", "MaxFPS")
        settings.set(self.b_resize_mult.get(), "CAMERA", "ResizeMultiplier")

        settings.set(self.b_show_cam.get(), "DISPLAY", "ShowCamera")
        settings.set(self.b_show_only_dots.get(), "DISPLAY", "ShowOnlyDots")
        settings.set(self.b_show_fps.get(), "DISPLAY", "ShowFPS")

        settings.set(self.b_max_hands.get(), "DETECTION", "MaxHands")
        settings.set(self.b_detection_confidence.get(), "DETECTION", "DetectionConfidence")
        settings.set(self.b_tracking_confidence.get(), "DETECTION", "TrackingConfidence")

        if settings.get("DEBUG", "Debug"):
            self.parent_wind.update_interface()

        self.after(1, self.apply_settings)


class MainWind(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.logs = Logs(self, settings.get("LOGS", "LogLevel"), settings.get("LOGS", "Format"), settings.get("LOGS", "DateFormat"))
        self.logs.pack(side="bottom", anchor="s", expand=True, fill="both")

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="Open .json file", command=self.load_file)
        self.file_menu.add_command(label="Setting", command=self.open_settings)

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menubar)

    def update_image(self, img) -> None:
        if settings.get("DISPLAY", "ShowCamera"):
            self.camera.enable_camera()
            self.camera.update_image(img)
        else:
            self.camera.disable_camera()

    def open_settings(self) -> None:
        SettingsWind(self)

    def load_file(self) -> None:
        settings.read(filedialog.askopenfile(
            title="Open .json file",
            initialdir="/",
            filetypes=(
                ("json files", "*.json"),
                ("all files", "*.*"))
        ))

    def update_interface(self) -> None:
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.camera_frame = ttk.Frame(self.main_frame)
        self.camera_frame.pack(side="top", anchor="nw")

        self.camera = Camera(self.camera_frame, no_cam_text="Camera disabled or don't work")
        self.camera.pack(side="left")

    # def __init__(self) -> None:
    #     super().__init__()

    #     self.camera = Camera(self, no_cam_text="Camera disabled or don't work")
    #     self.camera.pack()

    #     self.logs = Logs(self, settings.get("LOGS", "LogLevel"), settings.get("LOGS", "Format"), settings.get("LOGS", "DateFormat"))
    #     self.logs.pack(side="left", expand=True, fill="both")

    #     self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

    #     self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
    #     self.file_menu.add_command(label="Open .ini file", command=self.load_file)
    #     self.file_menu.add_command(label="Setting", command=self.open_settings)

    #     self.menubar.add_cascade(label="File", menu=self.file_menu)

    #     self.configure(menu=self.menubar)

    # def update_image(self, img) -> None:
    #     if settings.get("DISPLAY", "ShowCamera"):
    #         self.camera.enable_camera()
    #         self.camera.update_image(img)
    #     else:
    #         self.camera.disable_camera()

    # def open_settings(self) -> None:
    #     SettingsWind()

    # def load_file(self) -> None:
    #     settings.read(filedialog.askopenfile(
    #         title="Open .ini file",
    #         initialdir="/",
    #         filetypes=(
    #             ("ini files", "*.ini"),
    #             ("all files", "*.*"))
    #     ))


class DebugWind(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.logs = Logs(self, settings.get("DEBUG", "LogLevel"), settings.get("LOGS", "Format"), settings.get("LOGS", "DateFormat"))
        self.logs.pack(side="bottom", anchor="s", expand=True, fill="both")

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="Open .json file", command=self.load_file)
        self.file_menu.add_command(label="Global setting", command=self.open_settings)
        self.file_menu.add_command(label="Debug settings", command=self.open_debug_settings)

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menubar)

    def update_image(self, img) -> None:
        if settings.get("DISPLAY", "ShowCamera"):
            self.camera.enable_camera()
            self.camera.update_image(img)
        else:
            self.camera.disable_camera()

    def open_settings(self) -> None:
        SettingsWind(self)

    def open_debug_settings(self) -> None:
        # TODO: different settings that works only in debug (another SettingsWind class??)
        tkinter.messagebox.showinfo("WIP", "This feature unavable right now, but in active development!")

    def load_file(self) -> None:
        settings.read(filedialog.askopenfile(
            title="Open .json file",
            initialdir="/",
            filetypes=(
                ("json files", "*.json"),
                ("all files", "*.*"))
        ))

    def update_debug_menu(self) -> None:
        for gesture_class in settings.ACTIVE_GESTURES_CLASSES:
            try:
                gesture_class.interface_debug(self.debug_menu)
            except Exception as e:
                print(e)

    def update_interface(self) -> None:
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.camera_frame = ttk.Frame(self.main_frame)
        self.camera_frame.pack(side="top", anchor="nw")

        self.camera = Camera(self.camera_frame, no_cam_text="Camera disabled or don't work")
        self.camera.pack(side="left")

        self.debug_menu = ttk.Notebook(self.camera_frame)
        self.debug_menu.pack(side="left", anchor="nw")

        self.update_debug_menu()


if __name__ == "__main__":

    # root = tk.Tk()
    # root.geometry("400x400")
    # btn = PickWidget(root)
    # btn.pack()

    # while True:
    #     root.update()

    camera = CameraCapture(1)

    img = camera.cap()

    root = DebugWind()

    while True:
        img = camera.cap()
        root.update_image(img)
        root.update()
