import numpy as np
import cv2
import cv2.aruco as aruco
import imutils
import time


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
    return 2, coordinates # Change back to 3 later

#find only id0 from the corners
def rotation(coordinates):
    xH = coordinates[0][0]
    xV = coordinates[0][1]
    
    if(xH < 518):
        print("rotate left")
        if(xH > 610):
            print("rotate right")
    elif(xV < 380):
        print("rotate right")
        if(xV > 460):
            print("rotate left")
    else:
        print("Drone is in position")
        #return 3  
    #we will put this together once we figure some things out. 