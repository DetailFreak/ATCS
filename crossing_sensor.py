import cv2
import numpy as np
import imutils
import requests

capture = cv2.VideoCapture("crossing.mp4")
#capture = cv2.VideoCapture(0)

kernel = np.ones((7,7),np.uint8)
backsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

def maskContoursOf( frame ):
	ret = []
	fg = backsub.apply(frame,None,0.01)
	fg = cv2.medianBlur(fg,5)
	opening = cv2.morphologyEx(fg,cv2.MORPH_OPEN,kernel)
	x, contours , something = cv2.findContours(opening.copy() ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return [opening , contours]

def largestContour( cnts ):
	if not cnts:
		return False
	max_area = cv2.contourArea(cnts[0])
	cntm = cnts[0]
	for c in cnts:
		if cv2.contourArea(c) > max_area :
			max_area = cv2.contourArea(c)
			cntm = c
	return [max_area , cntm]


on , frame = capture.read()
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
halfx = frame_width/2
halfy = frame_height/2

state = 'none'
lower_lim = 100
upper_lim = 2000
state_prev = 'none'

while on:
	mask, cnts = maskContoursOf(frame)
	if cnts:
		max_area, cntm = largestContour(cnts)	 
	if upper_lim < lower_lim:
		if lower_lim < 10:
			lower_lim = 10;
		upper_lim = lower_lim+5	
	if max_area > lower_lim and max_area < upper_lim:
		M = cv2.moments(cntm)
		x = int (M["m10"] / M["m00"]) 
		y = int (M["m01"] / M["m00"])
		if state != 'CALIBRATION': 
			if y < (halfy - 0.1*halfy):
				state_prev = state
				state = 'OPEN'
			elif y > (halfy + 0.1*halfy):
				state_prev = state
				state = 'CLOSED'
			else:
				state_prev = state;
				state = 'CHANGING'
		params = {'devid':'v8003741FEF384B5','status':state}
		if state != state_prev:
			requests.get('http://api.pushingbox.com/pushingbox',params)

		cv2.circle(frame,(x,y), 3, (255,255,255), -1)
		cv2.drawContours( frame , [cntm], 0 ,(0,255,0),2)
		cv2.drawContours( mask , [cntm], 0 , (0,255,0),2)
	
	if state == 'OPEN':
		color = (0,200,0)
	elif state == 'CLOSED':
		color = (0,0,200)
	elif state =='CALIBRATION':
		color = (255,255,255)
	else: color = (100,100,100)
		
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,'STATE : ' + state ,(frame_width/2,50), font, 1,color,2,cv2.LINE_AA)
	cv2.putText(frame,'max area: ' + str(upper_lim) ,(10,25), font, 0.5,(0,0,255),1,cv2.LINE_AA)
	cv2.putText(frame,'min area: ' + str(lower_lim) ,(10,50), font, 0.5,(0,255,0),1,cv2.LINE_AA)
	
	cv2.imshow("frame",frame)
	cv2.imshow("foreground",mask)

	on , frame = capture.read()
	key = ' '
	key = cv2.waitKey(5)
	if key==ord('q'):
		break
	elif key==ord('k'):
		upper_lim+=5
	elif key==ord('j'):
		upper_lim-=5
	elif key==ord('a'):
		lower_lim+=5
	elif key==ord('s'):
		lower_lim-=5
	elif key==ord(';'):
		upper_lim+=100
	elif key==ord('l'):
		upper_lim-=100
	elif key==ord('f'):
		lower_lim+=100
	elif key==ord('d'):
		lower_lim-=100
