import cv2
import numpy as np
import time

load_from_disk = True
if load_from_disk:
    penval = np.load('penval.npy')


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

pen_img = cv2.resize(cv2.imread('pen.png',1), (100, 100))
eraser_img = cv2.resize(cv2.imread('eraser.jpg',1), (100, 100))

kernel= np.ones((5,5),np.uint8)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

canvas = None

#removing the shadow
backgroundobject = cv2.createBackgroundSubtractorMOG2( detectShadows = False )

# This threshold determines the amount of disruption in background.
background_threshold = 600

# A variable which tells you if you're using a pen or an eraser.
switch = 'Pen'

last_switch = time.time()

x1,y1=0,0

noiseth = 800

wiper_thresh = 40000
clear = False

while(1):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1 ) 

    if canvas is None:
        canvas = np.zeros_like(frame)

    top_left = frame[0: 100, 0: 100]
    fgmask = backgroundobject.apply(top_left)