

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

import cv2
import numpy as np
from All_ROI import RegionOfInterest as roi

# VARIABLES
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SCENE = 'Scene_1'


# video1 = rf'D:\AshutoshFulzele\AF\Projects\_Datasets_\AutomaticNumberPlateRecognition\BusStopArm\BusStopArm_Video\{SCENE}\Cam_1.mp4'
# vid1 = cv2.VideoCapture(video1)

# video2 = rf'D:\AshutoshFulzele\AF\Projects\_Datasets_\AutomaticNumberPlateRecognition\BusStopArm\BusStopArm_Video\{SCENE}\Cam_2.mp4'
video2 = rf'C:\Users\ShrikantViswanathan\Downloads\BusStopArm_Video_Cams\BusStopArm_Video\{SCENE}\Cam_2.mp4'
vid2 = cv2.VideoCapture(video2)
video3 = rf'C:\Users\ShrikantViswanathan\Downloads\BusStopArm_Video_Cams\BusStopArm_Video\{SCENE}\Cam_3.mp4'
# video3 = rf'D:\AshutoshFulzele\AF\Projects\_Datasets_\AutomaticNumberPlateRecognition\BusStopArm\BusStopArm_Video\{SCENE}\Cam_3.mp4'
vid3 = cv2.VideoCapture(video3)

# video4 = rf'D:\AshutoshFulzele\AF\Projects\_Datasets_\AutomaticNumberPlateRecognition\BusStopArm\BusStopArm_Video\{SCENE}\Cam_4.mp4'
video4 = rf'C:\Users\ShrikantViswanathan\Downloads\BusStopArm_Video_Cams\BusStopArm_Video\{SCENE}\Cam_4.mp4'
vid4 = cv2.VideoCapture(video4)

blank = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)        # uint8 shows actual frame

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

    ''' BSA Sign                      --> ( A x A dimension) '''
    b1, b2 = roi().BSA(scene=SCENE)
    cv2.rectangle(blank, b1, b2, (0, 0, 255), 2)
    roi_bsa = blank[b2[0]:b2[1], b1[0]:b1[1]]

    # GPS ROI
    g1, g2 = roi().GPS(scene=SCENE)
    cv2.rectangle(blank, g1, g2, (0, 0, 255), 2)
    roi_gps = blank[g2[0]:g2[1], g1[0]:g1[1]]

    # Date ROI
    d1, d2 = roi().Date(scene=SCENE)
    cv2.rectangle(blank, d1, d2, (0, 0, 255), 2)
    roi_date = blank[d2[0]:d2[1], d1[0]:d1[1]]

    # Time ROI
    t1, t2 = roi().Time(scene=SCENE)
    cv2.rectangle(blank, t1, t2, (0, 0, 255), 2)
    roi_time = blank[t2[0]:t2[1], t1[0]:t1[1]]

    # cv2.imshow('bsa', bsa)
    # cv2.imshow('gps', roi_gps)
    # cv2.imshow('ts', roi_time)
    cv2.imshow('blank', blank)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        # vid1.release()
        vid2.release()
        vid3.release()
        vid4.release()
        break

cv2.destroyAllWindows()
