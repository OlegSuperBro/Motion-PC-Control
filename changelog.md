# Changelog

## 2022.12.01.0

Really big update

### Added
- Some sort of documentation for functions (still not all).
- User interface made with tkinter.
- Gesture simplier install (just drop jesture file in "gestures" folder).
- New gesture format.
- Logging with logging module.

### Changed
- From processImage.py moved functions to camera.py:
    - change_color_channel
    - resize_image
    - change_brightness
- Reworked settings completely:
    - Save with json file format
    - To get setting now use "setting.get(value, "directory", "to", "setting")". Exceptions:
        - Screensize (settings.SCREEN_SIZE)
        - Camera size (settings.CAMERA_SIZE)
        - Mediapipe hands and draw (settings.MPHANDS, settings.MPDRAW )
        - Mediapipe hand (yea it's not same as hands) (settings.MPHAND)
        - Active gestures classes (only for running normally)
    - To set setting value use "setting.set(value, "directory", "to", "setting")"
- Changed way gestures works.

### Removed
- Calculations file because now its in gestures class.
- Controller file because now it's gesture class.
- dummy file because now i know how to create empty class without this :D