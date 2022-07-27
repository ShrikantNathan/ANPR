import random
from datetime import datetime
import json
import pprint
# Experimental


# This file is for backup only
def append_all_contents():
    jeet = {'predictions': [
        {'x': 111.0, 'y': 509.0, 'width': 208, 'height': 44, 'class': 'license_plate', 'confidence': 0.403}],
        'image': {'width': 960, 'height': 540}}  # for in jeet:
    mainList = []
    LP_text = f'TEXT-{random.randint(200, 1001)}'
    ts = '2022-01-05 15:56:22'

    x = jeet['predictions'][0].get('x')
    y = jeet['predictions'][0].get('y')
    w = jeet['predictions'][0].get('width')
    h = jeet['predictions'][0].get('height')
    conf = jeet['predictions'][0].get('confidence')
    mainList.append((LP_text, (str(round(conf * 100, 2)) + ' %'), int(x), int(y), int(w), int(h), ts))
    # print(mainList)
    json_contents = ["Text", "Confidence", "Center_X", "Center_Y", "Width", "Height", "TimeStamp"]
    # mainList.append((f'text:{LP_text}', (str(round(conf * 100, 2)) + ' %'), int(x), int(y), int(w), int(h), ts))
    mainDict = {k: v for k, v in zip(json_contents, mainList[0])}
    print(mainDict)


# This file is in use
def append_all_contents_2(text, conf, x, y, w, h, timestamp):
    mainList = [(text, int(round(conf * 100, 2)), int(x), int(y), int(w), int(h), timestamp)]
    # print(mainList)
    json_contents = ["Text", "Confidence", "Center_X", "Center_Y", "Width", "Height", "TimeStamp"]
    mainDict = {k: v for k, v in zip(json_contents, mainList[0])}
    # print(mainDict)
    return mainDict
