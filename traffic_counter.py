import cv2
import numpy as np
import pymouse
backsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False) #background subtraction to isolate moving cars
capture = cv2.VideoCapture("traffic.mp4") #change to destination on your pc
kernel = np.ones((11,11),np.uint8)
cv2.namedWindow('image')
minArea=1
upper = 20
lower = 100
while True:
    ret, frame = capture.read()
    frame = cv2.GaussianBlur(frame,(5,5),1)
    if not ret:
    	break
    fgmask = backsub.apply(frame, None, 0.001)
    fg = cv2.medianBlur(fgmask,5)
    fg = cv2.GaussianBlur(fg,(5,5),1)
    fg = cv2.GaussianBlur(fg,(5,5),1)
    closing = cv2.morphologyEx(fg,cv2.MORPH_OPEN,kernel)
    closing = cv2.erode(closing,kernel,iterations = 1)
    #closing = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel) 
    closing = cv2.GaussianBlur(closing,(7,7),0)
        #erosion to erase unwanted small contours
    x, contours , something = cv2.findContours(closing.copy() ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i=0
    for c in contours:
        if cv2.contourArea(c) > 10:
            i=i+1
            cv2.drawContours( frame , [c], 0 ,(0,255,0),2)
    cv2.putText(frame,'COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2)
    cv2.imshow("image", frame)
    cv2.imshow("background sub", fgmask)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break
