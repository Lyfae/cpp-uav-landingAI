import numpy as np
import cv2
import cv2.aruco as aruco
import imutils
import time

from calculations import *


def cornerloc(frame, corners, ids):
    coordinates = [[0,0],[0,0],[0,0],[0,0]]
    for markerCorner, markerID in zip(corners, ids):
        corners = markerCorner.reshape((4,2))
        topLeft, topRight, bottomRight, bottomLeft = corners

        # convert each of the (x,y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # draw the bounding box of the ArUCo detection
        cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
        
        # compute and draw the center (x,y)-coordinates of the ArUco marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the frame
        cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # put coordinates in list
        coordinates[int(markerID)] = [cX, cY]
    return coordinates # Change back to 3 later

#find only id0 from the corners
def differential(coordinates):
    global is_id0
    global is_id1 
    global is_id2 
    global is_id3
    global data      

    xH_id0 = coordinates[0][0]
    xV_id0 = coordinates[0][1]

    xH_id1 = coordinates[1][0]
    xV_id1 = coordinates[1][1]

    xH_id2 = coordinates[2][0]
    xV_id2 = coordinates[2][1]

    xH_id3 = coordinates[3][0]
    xV_id3 = coordinates[3][1]

    # checking at id0
    id0_setxH = 560
    id0_setxV = 360

    # checking at id1
    id1_setxH = 60
    id1_setxV = 360

    # checking at id2
    id2_setxH = 560
    id2_setxV = 120

    # checking at id3
    id3_setxH = 60
    id3_setxV = 120
    
    dx_id0 = id0_setxH - xH_id0
    dy_id0 = id0_setxV - xV_id0

    dx_id1 = id1_setxH - xH_id1
    dy_id1 = id1_setxV - xV_id1

    dx_id2 = id2_setxH - xH_id2
    dy_id2 = id2_setxV - xV_id2

    dx_id3 = id3_setxH - xH_id3
    dy_id3 = id3_setxV - xV_id3

    data = [[dx_id0,dy_id0],[dx_id1,dy_id1],[dx_id2,dy_id2],[dx_id3,dy_id3]]
            
    if(dx_id0<10 and dx_id0>-5 and dy_id0<5 and dy_id0 > -10):
        is_id0 = True
    elif(dx_id1<10 and dx_id1>-5 and dy_id1<5 and dy_id1 > -10):
        is_id1 = True    
    elif(dx_id2<10 and dx_id2>-5 and dy_id2<5 and dy_id2 > -10):
        is_id2 = True    
    elif(dx_id3<10 and dx_id3>-5 and dy_id3<5 and dy_id3 > -10):
        is_id3 = True
    else: 
        print("Keep the Drone Descending\n")
        print(data)

    if is_id0 and is_id1 and is_id2 and is_id3 == True:
        print("Stop Lowering the drone. Doing One more Check")    
        return 4  
    return 3

def quadrant_logic(coordinates,c0,c1,frame):
    global d1
    global d2
    global theta
    #check to see if id0 is in the correct quadrant
    id0_cordX = coordinates[0][0]
    id0_cordY = coordinates[0][1]
    

    if id0_cordX <= 320 and id0_cordY <=240:
        print("In Quadrant 2, rotate right")
    elif id0_cordX > 320 and id0_cordY <=240:
        print("In Quadrant 1, rotate left")
    elif id0_cordX <=320 and id0_cordY > 240:
        print("In Quadrant 3, rotate right")
    else:
        #print("In correct postion, finding differentials")
        temp1,temp2 = id0_cordX,id0_cordY
        
        d1 = distance(c0,560,c1,360)
        print("D1",d1)
        d2 = distance(c0,temp1, c1,temp2)
        print("D2",d2)
        line = cv2.line(frame,(c0,c1),(560,360),(0,0,0),5)
        line2 = cv2.line(frame,(c0,c1),(temp1,temp2),(0,0,0),5)
        cv2.imshow('Test',line)
        cv2.imshow('Test2',line2)
        theta = arcCos(d1,d2)
        print("The value:",theta)
        #return 3
    return 2    



# #320x240    