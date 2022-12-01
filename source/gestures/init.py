from os.path import dirname, basename, isfile, join
import glob


# TODO: make directories for gestures and scan them

def get_gestures():
    modules = glob.glob(join(dirname(__file__), "*.py"))
    return [basename(f)[:-3] for f in modules if isfile(f) and
            (basename(f) not in ("init.py", "baseplate.py"))]


if __name__ == "__main__":
    get_gestures()

# i copied this from stack overflow and idk what is this, but it works
