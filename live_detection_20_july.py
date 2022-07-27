
"""
PROJECT WORKFLOW:
------------------

1. Reading JSON
2. Extracting date-time
3. Finding StopArm event and its timestamp
4. Finding actual time from the frame and comparing it with StopArm timestamp
5. If in time range, detect vehicle and call Roboflow for LP detection
6. If LP detected, get its text from Textract
7. Format the proper timestamp and LP text and append everything in actual JSON with only 1 instance of the violated vehicle LP
"""

# All IMPORTS
import cv2
import numpy as np
import os
from All_ROI import RegionOfInterest as roi
import boto3
from PIL import Image
import io
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from append_json import append_all_contents_2
from store_json_event import store_detected_events_2
from datetime import datetime, time
import time


# VARIABLES
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SCENE = 'Scene_2'

# video1 = rf'D:\AshutoshFulzele\AF\Projects\_Datasets_\AutomaticNumberPlateRecognition\BusStopArm\BusStopArm_Video\{SCENE}\Cam_1.mp4'
# vid1 = cv2.VideoCapture(video1)

video2 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_2.mp4'
vid2 = cv2.VideoCapture(video2)

video3 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_3.mp4'
vid3 = cv2.VideoCapture(video3)

video4 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_4.mp4'
vid4 = cv2.VideoCapture(video4)
# vid4 = cv2.VideoCapture(10.18.1.103)

blank = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)  # uint8 shows actual frame
output_path = rf".\IMAGES\ROI\test.mp4"
codec = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(output_path, codec, 25, (SCREEN_WIDTH, SCREEN_HEIGHT))


img_path_lp = rf"{os.getcwd()}\IMAGES\ROI\LP.jpg"
img_path_time = rf"{os.getcwd()}\IMAGES\ROI\time.jpg"
img_path_dtime = rf"{os.getcwd()}\IMAGES\ROI\dtime.jpg"
# print('current dir:', os.getcwd())

# Drawing lines on Screen
cv2.line(blank, (0, 200), (350, 200), (0, 0, 255), 2)
cv2.line(blank, (0, 400), (350, 400), (0, 0, 255), 2)

EVENT_ARR = list()


''' DETECTING LP FROM VEHICLES '''
def Roboflow(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    LT_x, LT_y, RB_x, RB_y = 0, 0, 0, 0

    # Convert to JPEG Buffer
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")

    # Build multipart form and post request
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

    # response = requests.post("https://detect.roboflow.com/anpr_lic_2/2?api_key=nBgZlgcjKa2ZqiW6YrTr", data=m, headers={'Content-Type': m.content_type})
    response = requests.post("https://detect.roboflow.com/lic-plates/2?api_key=DmdaAV7Z3yTdZAk5GiNI", data=m,
                             headers={'Content-Type': m.content_type})

    # print(response)
    resp = response.json()
    # print(resp)

    length = len(resp.get('predictions'))
    bbox = []
    # LP_Text = str()
    pred_conf = 0
    for i in range(length):
        pred_x = resp.get('predictions')[i]['x']
        pred_y = resp.get('predictions')[i]['y']
        pred_w = resp.get('predictions')[i]['width']
        pred_h = resp.get('predictions')[i]['height']
        pred_conf = resp.get('predictions')[i]['confidence']
        bbox.append((pred_x, pred_y, pred_w, pred_h, pred_conf))

        for item in bbox:
            x, y, w, h, conf = item

            LT_x = int(x - (w / 2))
            LT_y = int(y - (h / 2))

            RB_x = int(x + (w / 2))
            RB_y = int(y + (h / 2))

    return LT_x, LT_y, RB_x, RB_y, pred_conf


''' IMAGE TO TEXT CONVERSION '''
def image_to_text(filepath):
    client = boto3.client('textract', region_name="us-east-2")

    with open(filepath, 'rb') as imgfile:
        imageBytes = bytearray(imgfile.read())

    result = client.detect_document_text(Document={'Bytes': imageBytes})
    elements = result['Blocks']

    text_arr = []

    for item in elements:
        if item["BlockType"] == "LINE":
            text_arr.append(item['Text'])

    for text in text_arr:
        return text


''' MAIN LOOP '''
try:
    # Loading and reading JSON file
    with open('alpr_raw_detect_2.json', mode='r') as f2:
        json_data = json.load(f2)
        sensor_dict = json_data["Export"]["Sensors"]

        # Finding the appropriate key-value pairs from the JSON
        for item in sensor_dict:
            if item.get('EventName') == "Stop Arm ST":
                event_dict = {"Event": item.get('EventName'), "DT_Start": item.get('DateTimeStart'), "DT_Stop": item.get('DateTimeStop')}
                EVENT_ARR.append(event_dict)
                bsa_start_date = str(item.get('DateTimeStart')).split(" ")[0]

                # --------------------
                bsa_start_time = item.get('DateTimeStart')
                start_time = datetime.strptime(bsa_start_time, "%Y-%m-%d %H:%M:%S")
                # --------------------

                bsa_stop_time = str(item.get('DateTimeStop'))
                stop_time = datetime.strptime(bsa_stop_time, "%Y-%m-%d %H:%M:%S")

                print(EVENT_ARR[-1])

                while True:
                    # ret1, frame1 = vid1.read()
                    ret2, frame2 = vid2.read()
                    ret3, frame3 = vid3.read()
                    ret4, frame4 = vid4.read()

                    # frame resize
                    # frame1 = cv2.resize(frame1, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
                    frame2 = cv2.resize(frame2, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
                    frame3 = cv2.resize(frame3, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
                    frame4 = cv2.resize(frame4, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))

                    blank[0:int(SCREEN_HEIGHT / 2), 0:int(SCREEN_WIDTH / 2)] = frame3[:, :]
                    blank[0:int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = frame4[:, :]
                    # blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), 0:960] = frame1[:, :]
                    blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = frame2[:, :]


# experience in tampering own working code and then blaming others for it
# experience in writing illogical code with full confidence and showing the errors generated to the clients



                    cv2.imshow('blank', blank)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        # vid1.release()
                        vid2.release()
                        vid3.release()
                        vid4.release()
                        break

                cv2.destroyAllWindows()









except RuntimeError as e:
    pass




