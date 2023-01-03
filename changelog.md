# Changelog

## 2023.01.03.0

### Added
- Now on main interface can be added custom things (gestures should do this)
    - interface will be in different tab
    - name of tab will be defined as gesture class name by default or by returned value from **interface_debug** function

### Changed
- All image processing things now in main.py file
- Replaced useless functions in main.py
- If **settings.set** changes something it will return True
- Refactored *Changelog* for better readability

### Fixed
- Crash when *appInterface.py* launching as main file (i'm stupid this error in **if name == "main"** thing)

### Removed
- Image class (i'm idiot, it's useless)

## 2022.12.05.0

### Added
- Recursive gesture importing (Now you can make folder in folder in folder :D)
- New Image object (subclass of np.ndarray)

### Changed
- Gestures **check**, **action** and **process_image** now run without fps limit (if the limit is 10 fps, then this only affects capture)
- Camera cap now return Image object (can be used same as np.ndarray but have some useful funcs)
- Some actions in main.py moved in functions

### Fixed
- Opening more than 1 setting window

### Removed
- Process image thing (all func moved in main.py)

## 2022.12.02.0

### Changed
- Options applying automatically (except for detection and gesture cuz it takes too much time to update)

### Fixed
- Opening json don't work

## 2022.12.01.0

Really big update

### Added
- Some sort of documentation for functions (still not all).
- User interface made with tkinter.
- Gesture simplier install (just drop gesture file in *"gestures"* folder).
- New gesture format.
- Logging with **logging** module.

### Changed
- From *processImage.py* moved functions to camera.py:
    - **change_color_channel**
    - **resize_image**
    - **change_brightness**
- Reworked settings completely:
    - Save with *.json* file format
    - To get setting now use "**setting.get(value, "directory", "to", "setting")**". Exceptions:
        - Screensize (*settings.SCREEN_SIZE*)
        - Camera size (*settings.CAMERA_SIZE*)
        - Mediapipe hands and draw (*settings.MPHANDS, settings.MPDRAW*)
        - Mediapipe hand (yea it's not same as hands) (*settings.MPHAND*)
        - Active gestures classes (only for running normally)
    - To set setting value use "**setting.set(value, "directory", "to", "setting")**"
- Changed way gestures works.

### Removed
- Calculations file because now its in gestures class.
- Controller file because now it's gesture class.
- dummy file because now i know how to create empty class without this :D
