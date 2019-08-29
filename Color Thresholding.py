import cv2
import numpy as np
import argparse
from collections import deque
PTS_LENGTH = int(input('Enter The number of Points='))
def nothing():
	pass

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help = "path to the (optional) Video File")
ap.add_argument("-b","--buffer",type = int ,default = 64,help = "max buffer size")
args = vars(ap.parse_args())
pts = deque(maxlen = PTS_LENGTH)

if not args.get("video",False):
 
	VidIn = cv2.VideoCapture(0)
else:
	VidIn = cv2.VideoCapture(args["video"])

cv2.namedWindow('TrackBars For HSV Values')
cv2.createTrackbar('Hmin','TrackBars For HSV Values',0,255,nothing)
cv2.createTrackbar('Smin','TrackBars For HSV Values',0,255,nothing)
cv2.createTrackbar('Vmin','TrackBars For HSV Values',0,255,nothing)
cv2.createTrackbar('Hmax','TrackBars For HSV Values',0,255,nothing)
cv2.createTrackbar('Smax','TrackBars For HSV Values',0,255,nothing)
cv2.createTrackbar('Vmax','TrackBars For HSV Values',0,255,nothing)

while True:
	
    grabbed, frame = VidIn.read()
    if args.get("video") and not grabbed:
        break
    frame = cv2.resize(frame,(600,600),interpolation = cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)



    Hmin = cv2.getTrackbarPos('Hmin','TrackBars For HSV Values')
    Smin = cv2.getTrackbarPos('Smin','TrackBars For HSV Values')
    Vmin = cv2.getTrackbarPos('Vmin','TrackBars For HSV Values')
    Hmax = cv2.getTrackbarPos('Hmax','TrackBars For HSV Values')
    Smax = cv2.getTrackbarPos('Smax','TrackBars For HSV Values')
    Vmax = cv2.getTrackbarPos('Vmax','TrackBars For HSV Values')
	
    print (Hmin,Smin,Vmin,Hmax,Smax,Vmax)
    Lower_Value = np.array([Hmin,Smin,Vmin])
    Upper_Value = np.array([Hmax,Smax,Vmax])
	
    mask = cv2.inRange(hsv,Lower_Value,Upper_Value)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)

    result = cv2.bitwise_and(frame,frame,mask=mask)

	#edges = cv2.Canny(mask,100,100)
	
    (_,cnts,_)= cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(frame,contours,-1,(0,255,0),3)
    center = None
	
    if len(cnts) > 0:
        c = max(cnts,key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        x1,y1,w,h = cv2.boundingRect(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        print (x1,y1,w,h)
        if radius > 10:
            cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,0),3)

            cv2.circle(frame,center,5,(0,0,255),-1)
            cv2.rectangle(frame,(int(x1),int(y1)),(int(x1+w),int(y1+h)),(0,255,0),2)

    print ("The Current center of the Object is =",center)
    pts.appendleft(center)
    for i in range(1,len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
        cv2.line(frame,pts[i-1],pts[i],(0,255,0),thickness)

	
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mask',mask)
    if cv2.waitKey(60):
        break

cv2.destroyAllWindows()
VidIn.release()
