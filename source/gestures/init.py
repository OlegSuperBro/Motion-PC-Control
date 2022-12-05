from os.path import dirname, basename, isfile, isdir, join
import glob

IGNORE_LIST = ("init.py", "baseplate.py", "__pycache__")


def get_gestures():
    gestures = []
    folders = []
    current_dir = dirname(__file__)
    modules = glob.glob(join(current_dir, "*"))
    while True:
        for file in modules:
            if basename(file) in IGNORE_LIST:
                continue

            if isdir(file):
                folders.append(file)

            elif isfile(file) and basename(file).endswith(".py"):
                gestures.append(file)

        if folders:
            current_dir = folders.pop(0)
            modules = glob.glob(join(current_dir, "*"))
        else:
            break

    return gestures


if __name__ == "__main__":
    print(get_gestures())
