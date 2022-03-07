import numpy as np
import cv2

from calculations import*

# for the 4 by 4 fiducial, the center one
def centerloc2(frame, corners, ids):
    coordinates = [0]
    for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4,2))
        topLeft, topRight, bottomRight, bottomLeft = corners

        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # draw the bounding box of the ArUCo detection
        cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the
        # ArUco marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the frame
        cv2.putText(frame, f"({cX},{cY})", (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        coordinates[int(markerID)] = [cX, cY]
    return coordinates

# for the 5 by 5 fiducial, the corner ones

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
    return coordinates 

def fine_tune(coordinates1, coordinates2, frame):
    corner_cordX = coordinates2[0][0]
    corner_cordY = coordinates2[0][1]

    center_cordX = coordinates1[0][0]
    center_cordY = coordinates1[0][1]

    print(f"Corners: {corner_cordX} ,{corner_cordY}  Center = {center_cordX},{center_cordY}")

    d1 = distance(center_cordX,560,center_cordY,360)
    print("D1",d1)
    d2 = distance(center_cordX,corner_cordX,center_cordY,corner_cordY)
    print("D2",d2)
    line = cv2.line(frame,(center_cordX,center_cordY),(560,360),(0,0,0),5)
    line2 = cv2.line(frame,(center_cordX,center_cordY),(corner_cordX,corner_cordY),(0,0,0),5)


    if d1 > d2:
        print("Continue Lowering the Drone")
    elif d1 < d2:
        print(("Raise the drone up"))
    elif d1 ==d2:
        print("Distance the same, continue next step")
        if corner_cordY > 360:
            theta = arcCos(d1,d2)
            print("Rotate right by ",theta)
        elif corner_cordY < 360:
            theta = arcCos(d1,d2) 
            print("Rotate left by ",theta)
        else:
            print("Drone is in the correct position, proceed with landing")
            return 4

    cv2.imshow('Test',line)
    cv2.imshow('Test2',line2)

    return 3