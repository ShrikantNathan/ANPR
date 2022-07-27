
"""
        -----------------
        |       |       |
        |   1   |   2   |
        |       |       |
        -----------------
        |       |       |
        |   3   |   4   |
        |       |       |
        -----------------

"""



import cv2
import numpy as np

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

blank = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)        # uint8 shows actual frame

# IMAGES
img1 = r'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\randompics\AI.png'
img2 = r'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\randompics\alml_1.jpg'
img3 = r'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\randompics\OIP.jpg'
img4 = r'C:\Users\ShrikantViswanathan\PycharmProjects\ALPR\randompics\OIP2.jpg'


i1 = cv2.imread(img1)
i2 = cv2.imread(img2)
i3 = cv2.imread(img3)
i4 = cv2.imread(img4)


I1 = cv2.resize(i1, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
I2 = cv2.resize(i2, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
I3 = cv2.resize(i3, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
I4 = cv2.resize(i4, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))


blank[0:int(SCREEN_HEIGHT / 2), 0:int(SCREEN_WIDTH / 2)] = I1[:, :]
blank[0:int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = I2[:, :]
blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), 0:int(SCREEN_WIDTH / 2)] = I3[:, :]
blank[int(SCREEN_HEIGHT / 2):int(SCREEN_HEIGHT), int(SCREEN_WIDTH / 2): int(SCREEN_WIDTH)] = I4[:, :]

cv2.imshow('blank', blank)
cv2.waitKey(0)