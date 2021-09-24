import numpy as np
import cv2
import cv2.aruco as aruco
import imutils
import time

from _thread import *
import threading

from arucodetect import *

def main():
    # Define webcam used
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Check for compatibility. If not, force search webcam
    ret, frame = webcam.read()
    print(frame)
    try:
        if frame == None:
            webcam = cv2.VideoCapture(-1)
    except:
        print("Task Failed Successfully. Move on.")

    global state
    state = 0

    # State 0: Flying Mode
    # State 1: Location Mode
    # State 2: Orientation Mode
    # State 3: Landing Mode
    # State 4: Takeoff Mode

    while(True):
        # Grabbing frame from webcam
        _, frame = webcam.read()

        # Find ArUco markers if the state is not in orientation mode
        if state == 0 or state == 1:
            corners, ids = findArucoMarkers(frame, 4, 50)
            try:
                state, cX, cY = centerloc(frame, corners, ids)
            except:
                pass # Skip process if ArUcO code is not found
            
        # Centering Logic
        if state == 1:
            state = locationstate(cX, cY)

        # Orientation Logic
        if state == 2:
            corners, ids =  findArucoMarkers(frame, 5, 50)
            try:
                state, coordinates = cornerloc(frame, corners, ids)
                print(coordinates)
                state = 2
            except:
                pass

        if state == 3:
            print("LANDING MODE!!!")

        # Show frame in seperate box
        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Safely close all windows
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()