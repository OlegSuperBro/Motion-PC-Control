from controller import *

dots = None
            
SU = None

def parse(gestures: dict, dots: list, SU: float = 1):
    for key in gestures.keys():
        for line in gestures.get(key):
            try:
                result = eval(line[0])
            except:
                return
            else:
                if result:
                    line[1](dots, *line[2])