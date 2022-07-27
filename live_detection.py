
"""
Cam Videos to be placed in this order:
        -----------------
        |       |       |
        |   3   |   4   |
        |       |       |
        -----------------
        |       |       |
        |   1   |   2   |
        |       |       |
        -----------------

Cam 1 needs to be removed/omitted as it doesn't run on same FPS as others.
"""
from pprint import pprint

import cv2
import numpy as np
from All_ROI import RegionOfInterest as roi
import boto3
from PIL import Image
import io
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

client = boto3.client('textract', region_name="us-east-2")


# VARIABLES
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# SCENES = ['Scene_1', 'Scene_2', 'Scene_3']
SCENE = 'Scene_2'
# SCENE = np.random.choice(SCENES)

# video1 = rf'/home/richard/TensorFlow-2.x-YOLOv3/IMAGES/{SCENE}/Cam_1.mp4'
# vid1 = cv2.VideoCapture(video1)

# video2 = rf'/home/richard/TensorFlow-2.x-YOLOv3/IMAGES/{SCENE}/Cam_2.mp4'
video2 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_2.mp4'
vid2 = cv2.VideoCapture(video2)
# video3 = rf'/home/richard/TensorFlow-2.x-YOLOv3/IMAGES/{SCENE}/Cam_3.mp4'
video3 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_3.mp4'
vid3 = cv2.VideoCapture(video3)

# video4 = rf'/home/richard/TensorFlow-2.x-YOLOv3/IMAGES/{SCENE}/Cam_4.mp4'
video4 = rf'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\Scene\BusStopArm_Video\{SCENE}\Cam_4.mp4'
vid4 = cv2.VideoCapture(video4)

blank = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)        # uint8 shows actual frame

output_path = r'.\IMAGES\ROI\test.mp4'
codec = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(output_path, codec, 25, (SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    # ret1, frame1 = vid1.read()
    ret2, frame2 = vid2.read()
    ret3, frame3 = vid3.read()
    ret4, frame4 = vid4.read()

    # print(int(SCREEN_HEIGHT / 2))
    # print(int(SCREEN_WIDTH) - 20)

    # frame resize
    # frame1 = cv2.resize(frame1, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
    frame2 = cv2.resize(frame2, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
    frame3 = cv2.resize(frame3, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
    frame4 = cv2.resize(frame4, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))

    blank[0:int(SCREEN_HEIGHT / 2), 0:int(SCREEN_WIDTH / 2)] = frame3[:, :]
    blank[0:int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = frame4[:, :]
    # blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), 0:960] = frame1[:, :]
    blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = frame2[:, :]

    cv2.line(blank, (0, 200), (350, 200), (0, 0, 255), 2)
    cv2.line(blank, (0, 400), (350, 400), (0, 0, 255), 2)

    ''' BSA Sign                      --> ( A x A dimension) '''
    b1, b2 = roi().BSA(scene=SCENE)
    cv2.rectangle(blank, b1, b2, (0, 0, 255), 2)
    roi_bsa = blank[b1[1]:b2[1], b1[0]:b2[0]]

    # ---------------------------------------------------------------------------------
    ''' License Plate '''
    image = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)

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
    LP_Text = str()

    for i in range(length):
        pred_x = resp.get('predictions')[i]['x']
        pred_y = resp.get('predictions')[i]['y']
        pred_w = resp.get('predictions')[i]['width']
        pred_h = resp.get('predictions')[i]['height']

        bbox.append((pred_x, pred_y, pred_w, pred_h))

        for item in bbox:
            x, y, w, h = item

            LT_x = int(x) - int(w / 2)
            LT_y = int(y) - int(h / 2)

            RB_x = int(x + (w / 2))
            RB_y = int(y + (h / 2))

            pt1 = (LT_x, LT_y)
            pt2 = (RB_x, RB_y)

            # print(pt1, pt2)

            # ROI Logic
            # if LT_x <= int(SCREEN_WIDTH / 3):
            #     if int(SCREEN_HEIGHT / 4) <= LT_y <= int(3 * SCREEN_HEIGHT / 4):

            if LT_x <= 350:
                # print('hi')
                if 200 <= LT_y <= 400:
                    # print('Uninterpreted')
                    cv2.imwrite(r"./IMAGES/ROI/LP.jpg", blank[LT_y:RB_y, LT_x:RB_x])
                    # cv2.rectangle(img, (int(x)-50, int(y)-20), (int(x + w)-50, int(y + h)-20), (0, 0, 255), 2)
                    cv2.rectangle(blank, pt1, pt2, (0, 0, 255), 2)

                    import boto3

                    client = boto3.client('textract',region_name="us-east-2")
                    imgfilename = r"./IMAGES/ROI/LP.jpg"
                    # print("hello")
                    # def get_file_from_filepath(filename):
                    with open(imgfilename, 'rb') as imgfile:
                        imageBytes = bytearray(imgfile.read())
                        # print(type(imageBytes))

                    # imgbyte = get_file_from_filepath(imgfilename)

                    result = client.detect_document_text(Document={'Bytes': imageBytes})
                    shri = result['Blocks']

                    text_arr = []

                    for item in shri:
                        if item["BlockType"] == "LINE":
                            text_arr.append(item['Text'])

                    for txt in text_arr:
                        print(txt)

                        cv2.putText(blank, txt, (LT_x, LT_y - 4), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 255, 0),
                                    1, lineType=cv2.LINE_AA)
                        LP_Text = txt
                    # print('text predicted as :'.capitalize(), LP_Text)

                import json
                import pprint
                from TestX9 import append_all_contents_2
                from TestX7 import store_detected_events_2
                try:
                    with open('alpr_raw_detect_2.json', mode='r') as f2:
                        json_data = json.load(f2)
                        sensor_dict_start = json_data["Export"]["Sensors"][1]['DateTimeStart']
                        # print(f'sensor_dict: {sensor_dict_start}, sensor_dict: {sensor_dict_stop}')

                        # cv2.circle(blank, (int(pred_x), int(pred_y)), 10, (0, 0, 255), -1)
                        # cv2.circle(blank, (int(pred_w), int(pred_h)), 10, (0, 255, 0), -1)
                        if LP_Text != '':
                            result_dict = append_all_contents_2(text=LP_Text, conf=resp.get('predictions')[i]['confidence'],
                                x=pred_x, y=pred_y, w=pred_w, h=pred_h, timestamp=f'{sensor_dict_start}')
                            store_detected_events_2(result_dict)    # writes to json file
                            print(result_dict)

                except json.JSONDecodeError as e:
                    print(e.msg)


    # GPS ROI
    g1, g2 = roi().GPS(scene=SCENE)
    cv2.rectangle(blank, g1, g2, (0, 0, 255), 2)
    roi_gps = blank[g1[1]:g2[1], g1[0]:g2[0]]

    # Date ROI
    d1, d2 = roi().Date(scene=SCENE)
    cv2.rectangle(blank, d1, d2, (0, 0, 255), 2)
    roi_date = blank[d1[1]:d2[1], d1[0]:d2[0]]

    # Time ROI
    t1, t2 = roi().Time(scene=SCENE)
    cv2.rectangle(blank, t1, t2, (0, 0, 255), 2)
    roi_time = blank[t1[1]:t2[1], t1[0]:t2[0]]
    cv2.imwrite(r"time.jpg", roi_time)

    # Experimentals
    # jeet = {'predictions': [
    #     {'x': 111.0, 'y': 509.0, 'width': 208, 'height': 44, 'class': 'license_plate', 'confidence': 0.403}],
    #         'image': {'width': 960, 'height': 540}}  # for in jeet:
    # mainList = []
    # LP_text = 'BS-342'
    # for i in range(len(jeet['predictions'][0].items())):
    #     if "class" in jeet['predictions'][0].keys():
    #         continue
    #     else:
    #         print('new for loop')
    #         x = jeet['predictions'][i].get('x')
    #         y = jeet['predictions'][i].get('y')
    #         w = jeet['predictions'][i].get('width')
    #         h = jeet['predictions'][i].get('height')
    #         conf = jeet['predictions'][i].get('confidence')
    #         print(x, y, w, h, conf)
    # ts = '2022-01-05 15:56:22'

    if output_path != '':
        out.write(blank)

    cv2.imshow('blank', blank)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # vid1.release()
        vid2.release()
        vid3.release()
        vid4.release()
        break

cv2.destroyAllWindows()