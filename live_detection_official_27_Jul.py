
import os
import cv2
import numpy as np
from All_ROI import RegionOfInterest as roi
import boto3
from PIL import Image
import io
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from append_json import append_all_contents_2
from store_json_event import store_detected_events_2, store_detected_events_2_backup
from datetime import datetime

client = boto3.client('textract', region_name="us-east-2")

# VARIABLES
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SCENE = 'Scene_2'

video2 = rf'{os.getcwd()}\Scene\BusStopArm_Video\{SCENE}\Cam_2.mp4'
video3 = rf'{os.getcwd()}\Scene\BusStopArm_Video\{SCENE}\Cam_3.mp4'
video4 = rf'{os.getcwd()}\Scene\BusStopArm_Video\{SCENE}\Cam_4.mp4'

vid2 = cv2.VideoCapture(video2)
vid3 = cv2.VideoCapture(video3)
vid4 = cv2.VideoCapture(video4)

blank = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)  # uint8 shows actual frame
output_path = rf".\IMAGES\ROI\test.mp4"
codec = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(output_path, codec, 25, (SCREEN_WIDTH, SCREEN_HEIGHT))


img_path_lp = rf"{os.getcwd()}/IMAGES/ROI/LP.jpg"
img_path_time = rf"{os.getcwd()}/IMAGES/ROI/time.jpg"
img_path_dtime = rf"{os.getcwd()}/IMAGES/ROI/dtime.jpg"

# if not os.path.exists(img_path_lp) and not os.path.exists(img_path_time) and not os.path.exists(img_path_dtime):
#     with open(img_path_lp, mode='w'):
#         pass
#     with open(img_path_time, mode='w'):
#         pass
#     with open(img_path_dtime, mode='w'):
#         pass


def Roboflow(frame):
    ''' License Plate '''
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    LT_x, LT_y, RB_x, RB_y = 0, 0, 0, 0

    # Convert to JPEG Buffer
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")

    # Build multipart form and post request
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

    response = requests.post("https://detect.roboflow.com/lic-plates/2?api_key=DmdaAV7Z3yTdZAk5GiNI", data=m,
                             headers={'Content-Type': m.content_type})

    resp = response.json()

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


def perform_all_json_processes(lp_txt, time_text):
    if lp_txt is not None and time_text is not None:
        # print(lp_txt + " is the text", time_text + ' is the time')
        result_dict = append_all_contents_2(text=lp_txt, conf=conf, x=x1, y=y1, w=x2, h=y2, timestamp=f'{bsa_start_date} {time_text}')
        print(result_dict)
        print('saving to', f2.name)
        # store_detected_events_2(result_dict)
        store_detected_events_2_backup(result_dict)

try:
    with open("alpr_raw_detect_2.json", mode='r') as f2:
        json_data = json.load(f2)
        sensor_dict = json_data["Export"]["Sensors"]
        for item in sensor_dict:
            if item.get('EventName') == "Stop Arm ST":
                bsa_start_date = str(item.get('DateTimeStart')).split(" ")[0]

                bsa_start_time = item.get('DateTimeStart')
                start_time = datetime.strptime(bsa_start_time, "%Y-%m-%d %H:%M:%S")

                bsa_stop_time = str(item.get('DateTimeStop'))
                stop_time = datetime.strptime(bsa_stop_time, "%Y-%m-%d %H:%M:%S")
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
                    # print(f'screen dims: {blank.shape[:2]}')
                    # Calling roboflow to detect the LP in frame 3
                    x1, y1, x2, y2, conf = Roboflow(frame3)
                    # Drawing lines on Screen
                    cv2.line(blank, (0, 200), (350, 200), (0, 0, 255), 2)
                    cv2.line(blank, (0, 400), (350, 400), (0, 0, 255), 2)

                    if x1 <= 350:
                        # print('hi')
                        if 200 <= y1 <= 400:
                            try:
                                # Time ROI
                                t1, t2 = roi().Time(scene=SCENE)
                                roi_time = blank[t1[1]:t2[1], t1[0]:t2[0]]
                                cv2.imwrite(img_path_time, roi_time)
                                cv2.rectangle(blank, t1, t2, (0, 0, 255), 2)

                                # DateTime ROI
                                dt1, dt2 = roi().DateTime(scene=SCENE)
                                roi_dtime = blank[dt1[1]:dt2[1], dt1[0]:dt2[0]]
                                cv2.imwrite(img_path_dtime, roi_dtime)
                                cv2.rectangle(blank, dt1, dt2, (0, 0, 255), 2)

                                time_text = image_to_text(img_path_time)

                                time_txt_cvt = datetime.strptime(str(time_text), '%H:%M:%S')
                                actual_timestamp = bsa_start_date + ' ' + str(time_txt_cvt).split(' ')[1]
                                ats = datetime.strptime(actual_timestamp, "%Y-%m-%d %H:%M:%S")
                                # print('converted time text:', time_txt_cvt)
                                # print('actual time (ats):', ats)
                                lp_txt = image_to_text(img_path_lp)

                                if start_time <= ats <= stop_time:
                                    cv2.imwrite(img_path_lp, blank[y1:y2, x1:x2])
                                    cv2.rectangle(blank, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                    perform_all_json_processes(lp_txt, time_text)

                                else:
                                    print('stop arm sign closed..'.capitalize())

                            except ValueError:
                                print('-----------------')
                                pass

                    cv2.imshow('blank', blank)

                    out.write(blank)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        # vid1.release()
                        vid2.release()
                        vid3.release()
                        vid4.release()
                        break

                cv2.destroyAllWindows()

except json.JSONDecodeError as e:
    print(e.msg)