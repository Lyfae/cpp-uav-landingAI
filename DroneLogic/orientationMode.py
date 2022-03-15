import numpy as np
import cv2

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
        print("In correct postion, Proceed to next step")
        return 3
    return 2    





# #320x240    