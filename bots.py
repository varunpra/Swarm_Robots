# Importing all the Needed Libraries

import cv2
import numpy as np
import argparse
from collections import deque
import serial
import time
ser=serial.Serial('/dev/cu.usbmodem1411',9600,timeout=1)
time.sleep(2)
ser.flush()
X1_Center = 0
Y1_Center = 0
X2_Center = 0
Y2_Center = 0
X3_Center = 0
Y3_Center = 0

Real_World = ""
# Defining Variables for Real World Coordinates

Real_Length_Of_Bot = 25.6
Real_Width_Of_Bot = 17.1

PTS_LENGTH = 1
def nothing():
	pass

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help = "path to the (optional) Video File")
ap.add_argument("-b","--buffer",type = int ,default = 64,help = "max buffer size")
args = vars(ap.parse_args())
pts1= deque(maxlen = PTS_LENGTH)
pts2 = deque(maxlen = PTS_LENGTH)
pts3 = deque(maxlen = PTS_LENGTH)
pts4 = deque(maxlen = PTS_LENGTH)
if not args.get("video",False):
 
	VidIn = cv2.VideoCapture(0)
else:
	VidIn = cv2.VideoCapture(args["video"])

while True:
	
    grabbed, frame = VidIn.read()
    if args.get("video") and not grabbed:
        break
#frame = cv2.resize(frame,(600,600),interpolation = cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	
    Lower_Value_Red = np.array([173,134,25])
    Upper_Value_Red = np.array([190,255,187])
    Lower_Value_Green = np.array([48,57,0])
    Upper_Value_Green = np.array([151,160,108])
#Lower_Value_Blue = np.array([46,3,53])
#Upper_Value_Blue = np.array([155,255,254])
    Lower_Value_Blue = np.array([0,118,48])
    Upper_Value_Blue = np.array([45,255,255])
	
    mask1 = cv2.inRange(hsv,Lower_Value_Red,Upper_Value_Red)
    mask2 = cv2.inRange(hsv,Lower_Value_Green,Upper_Value_Green)
    mask3 = cv2.inRange(hsv,Lower_Value_Blue,Upper_Value_Blue)
# mask4 = cv2.inRange(hsv,Lower_Value_Yellow,Upper_Value_Yellow)

    kernel = np.ones((5,5),np.uint8)

    mask1 = cv2.erode(mask1,kernel,iterations=2)
    mask1 = cv2.dilate(mask1,kernel,iterations = 2)
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_CLOSE,kernel)
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernel)
	
    mask2 = cv2.erode(mask2,kernel,iterations=2)
    mask2 = cv2.dilate(mask2,kernel,iterations = 2)
    mask2 = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernel)
    mask2 = cv2.morphologyEx(mask2,cv2.MORPH_OPEN,kernel)

    mask3 = cv2.erode(mask3,kernel,iterations=2)
    mask3 = cv2.dilate(mask3,kernel,iterations = 2)
    mask3 = cv2.morphologyEx(mask3,cv2.MORPH_CLOSE,kernel)
    mask3 = cv2.morphologyEx(mask3,cv2.MORPH_OPEN,kernel)

# mask4 = cv2.erode(mask4,kernel,iterations=2)
#mask4 = cv2.dilate(mask4,kernel,iterations = 2)
#mask4 = cv2.morphologyEx(mask4,cv2.MORPH_CLOSE,kernel)
#mask4 = cv2.morphologyEx(mask4,cv2.MORPH_OPEN,kernel)

    (_,cnts1,_) = cv2.findContours(mask1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    (_,cnts2,_) = cv2.findContours(mask2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    (_,cnts3,_) = cv2.findContours(mask3.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#(_,cnts4,_) = cv2.findContours(mask4.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
    center1 = []
    center2 = []
    center3 = []
#center4 = []


    if len(cnts1) > 0:
        c1 = max(cnts1,key=cv2.contourArea)
        x1,y1,w1,h1 = cv2.boundingRect(c1)
        M1 = cv2.moments(c1)
        center1 = [int(M1["m10"]/M1["m00"]),int(M1["m01"]/M1["m00"])]
        cv2.rectangle(frame,(int(x1),int(y1)),(int(x1+w1),int(y1+h1)),(0,0,255),3)
		# Calculating the Pixel Width of the Bot
		
        Pixel_Length_Of_Red_Bot = float(y1+h1)-float(y1)
        Pixel_Width_Of_Red_Bot= float(x1+w1) - float(x1)

		# Calculating the Multiplication Factor

        For_Length1 = float(Real_Length_Of_Bot/Pixel_Length_Of_Red_Bot)
        For_Width1 = float(Real_Width_Of_Bot/Pixel_Width_Of_Red_Bot)

		# Now Calculating the Real World Coordinates of the Center of the Object 
		
        X1_Center = int(For_Width1 * center1[0])
        Y1_Center = int(For_Length1 * center1[1])

        # X4_Center = 0
        #Y4_Center = 0

        Real_World_Red_Bot_Center = [X1_Center,Y1_Center]
        print ("Red Bot Coordinates Are",Real_World_Red_Bot_Center)
    #ser.write(Real_World_Red_Bot_Center)

    if len(cnts2) > 0:
        c2 = max(cnts2,key=cv2.contourArea)
        x2,y2,w2,h2 = cv2.boundingRect(c2)
        M2 = cv2.moments(c2)
        center2 = [int(M2["m10"]/M2["m00"]),int(M2["m01"]/M2["m00"])]
        cv2.rectangle(frame,(int(x2),int(y2)),(int(x2+w2),int(y2+h2)),(0,255,0),3)

		# Calculating the Pixel Width of the Bot
		
        Pixel_Length_Of_Green_Bot = float(y2+h2)-float(y2)
        Pixel_Width_Of_Green_Bot= float(x2+w2) - float(x2)

		# Calculating the Multiplication Factor

        For_Length2 = float(Real_Length_Of_Bot/Pixel_Length_Of_Green_Bot)
        For_Width2 = float(Real_Width_Of_Bot/Pixel_Width_Of_Green_Bot)

		# Now Calculating the Real World Coordinates of the Center of the Object 
		
        X2_Center = int(For_Width2 * center2[0])
        Y2_Center = int(For_Length2 * center2[1])

        # X4_Center = 0
        #Y4_Center = 0

        Real_World_Green_Bot_Center = [X2_Center,Y2_Center]
        print (" Green Bot Coordinates Are",Real_World_Green_Bot_Center)
    #ser.write(Real_World_Green_Bot_Center)

    if len(cnts3) > 0:
        c3 = max(cnts3,key=cv2.contourArea)
        x3,y3,w3,h3 = cv2.boundingRect(c3)
        M3 = cv2.moments(c3)
        center3 = [int(M3["m10"]/M3["m00"]),int(M3["m01"]/M3["m00"])]
        cv2.rectangle(frame,(int(x3),int(y3)),(int(x3+w3),int(y3+h3)),(255,0,0),3)

		# Calculating the Pixel Width of the Bot
		
        Pixel_Length_Of_Blue_Bot = float(y3+h3)-float(y3)
        Pixel_Width_Of_Blue_Bot= float(x3+w3) - float(x3)

		# Calculating the Multiplication Factor

        For_Length3 = float(Real_Length_Of_Bot/Pixel_Length_Of_Blue_Bot)
        For_Width3 = float(Real_Width_Of_Bot/Pixel_Width_Of_Blue_Bot)

		# Now Calculating the Real World Coordinates of the Center of the Object 
		
        X3_Center = int(For_Width3 * center3[0])
        Y3_Center = int(For_Length3 * center3[1])


        Real_World_Blue_Bot_Center = [X3_Center,Y3_Center]
        print ("Blue  Bot Coordinates Are ",Real_World_Blue_Bot_Center)
    #ser.write(Real_World_Blue_Bot_Center)
    
#if len(cnts4) > 0:
#c4 = max(cnts4,key=cv2.contourArea)
# x4,y4,w4,h4 = cv2.boundingRect(c4)
# M4 = cv2.moments(c4)
#center4 = [int(M4["m10"]/M4["m00"]),int(M4["m01"]/M4["m00"])]
#cv2.rectangle(frame,(int(x4),int(y4)),(int(x4+w4),int(y4+h4)),(51,100,80),3)

		# Calculating the Pixel Width of the Bot
		
        #Pixel_Length_Of_Yellow_Bot = float(y4+h4)-float(y4)
        # Pixel_Width_Of_Yellow_Bot= float(x4+w4) - float(x4)

		# Calculating the Multiplication Factor

#For_Length4 = float(Real_Length_Of_Bot/Pixel_Length_Of_Yellow_Bot)
#For_Width4 = float(Real_Width_Of_Bot/Pixel_Width_Of_Yellow_Bot)

		# Now Calculating the Real World Coordinates of the Center of the Object 
		
        #X4_Center = int(For_Width4 * center4[0])
        #Y4_Center = int(For_Length4 * center4[1])
        # X1_Center = 0
        # Y1_Center = 0
        # X3_Center = 0
        # Y3_Center = 0
        # X2_Center = 0
        # Y2_Center = 0

# Real_World_Yellow_Bot_Center = [X4_Center,Y4_Center]
# print ("Yellow  Bot Coordinates Are ",Real_World_Yellow_Bot_Center)
    #ser.write(Real_World_Yellow_Bot_Center)
    X1_Center=str(X1_Center)

    Y1_Center=str(Y1_Center)

    X2_Center=str(X2_Center)

    Y2_Center=str(Y2_Center)

    X3_Center=str(X3_Center)

    Y3_Center=str(Y3_Center)

    ser.write(bytes(X1_Center,encoding='ascii'))
    ser.write(b',')
    ser.write(bytes(Y1_Center,encoding='ascii'))
    ser.write(b',')
    ser.write(bytes(X2_Center,encoding='ascii'))
    ser.write(b',')
    ser.write(bytes(Y2_Center,encoding='ascii'))
    ser.write(b',')
    ser.write(bytes(X3_Center,encoding='ascii'))
    ser.write(b',')
    ser.write(bytes(Y3_Center,encoding='ascii'))
    ser.write(b'%')
    pts1.appendleft(center1)
    pts2.appendleft(center2)
    pts3.appendleft(center3)
# pts4.appendleft(center4)


    for i in range(1,len(pts1)):
        if pts1[i-1] is None or pts1[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
        cv2.line(frame,pts1[i-1],pts1[i],(0,255,0),thickness)

    for i in range(1,len(pts2)):
        if pts2[i-1] is None or pts2[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
        cv2.line(frame,pts2[i-1],pts2[i],(0,255,0),thickness)

    for i in range(1,len(pts3)):
        if pts3[i-1] is None or pts3[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
        cv2.line(frame,pts3[i-1],pts3[i],(0,255,0),thickness)

#for i in range(1,len(pts4)):
# if pts4[i-1] is None or pts4[i] is None:
#    continue

#thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
#cv2.line(frame,pts4[i-1],pts4[i],(0,255,0),thickness)
	
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mask1',mask1)
    cv2.imshow('mask2',mask2)
    cv2.imshow('mask3',mask3)
#cv2.imshow('mask4',mask4)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break


cv2.destroyAllWindows()
VidIn.release()
ser.close()
