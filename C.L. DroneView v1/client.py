# Autonomous Pi Drone Controller
# Christopher Lai, UAV BANSHEE Robotics Team
# Version: v2

import socket
from turtle import update, width
import cv2
import cv2.aruco as aruco
import pickle
import struct
from _thread import *
import threading
import tkinter as tk

# Custom Dependencies
from arucodetect import *

# Global Variables
isFrameBtnPressed = False
isFrameOpen = False

# Connect to Server (commment this out until needed)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = '192.168.254.134' # paste your server ip address here
PORT = 8009
s.connect((HOST,PORT))

# [THREAD] tkinter
def tkinter():
    # TKINTER DEFUALT SETTINGS
    HEIGHT = 400
    WIDTH = 600
    BGCOLOR = 'black'
    BTCOLOR = 'black'
    TITLECOLOR = '#E556E6'
    SUBTITLECOLOR = '#914FA6'
    BTNLABELCOLOR = 'white'
    REFRESH_RATE = 50

    # INITIALIZATION
    # Create the program window (root)
    root = tk.Tk()
    root.resizable(False, False)
    main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=BGCOLOR, highlightthickness=0)
    main_canv.pack()

    # ICONS (Courtesy of Icons8.com)
    camera_icon = tk.PhotoImage(file='icons/camera.png')
    activate_icon = tk.PhotoImage(file='icons/record.png')

    # LABEL
    title = tk.Label(main_canv, text="DroneView V1", font=('courier new',24,'bold'), justify='center', bg=BGCOLOR, fg=TITLECOLOR)
    title.place(relx=0.5,rely=0.085,anchor='center')

    subtitle = tk.Label(main_canv, text="UAV BANSHEE Robotics Team", font=('courier new',20), justify='center', bg=BGCOLOR, fg=SUBTITLECOLOR)
    subtitle.place(relx=0.5,rely=0.175,anchor='center')

    frame_label = tk.Label(main_canv, text="Open/Close\nDrone Camera", font=('courier new',14), justify='center', bg=BGCOLOR, fg=SUBTITLECOLOR)
    frame_label.place(relx=0.3,rely=0.625,anchor='center')

    move_label = tk.Label(main_canv, text="Toggle Panic\nMode On/Off", font=('courier new',14), justify='center', bg=BGCOLOR, fg=SUBTITLECOLOR)
    move_label.place(relx=0.7,rely=0.625,anchor='center')

    # BUTTON FUNCTIONS
    def toggleFrame():
        global isFrameBtnPressed
        isFrameBtnPressed = True

    def propmove():
        s.send(bytes('y', 'utf-8'))
        print("Drone Props Moved!")

    # BUTTON DECLARATIONS
    # Frame Button
    display_frame = tk.Button(main_canv, image = camera_icon, command=toggleFrame, justify='center', padx=10, pady=10, bg=BTCOLOR, fg='#9e8d8f')
    display_frame.place(relx=0.3, rely=0.45,anchor='center')

    # Move Motor
    sc_mask = tk.Button(main_canv, image = activate_icon, command=propmove, justify='center', padx=10, pady=10, bg=BTCOLOR, fg='#9e8d8f')
    sc_mask.place(relx=0.7,rely=0.45,anchor='center')

    # Exit Button
    exitButton = tk.Button(main_canv, text="EXIT", font=('courier new',18,'bold'), command=exit, justify='center', padx=40, pady=10, bg='#de2828', fg='white')
    exitButton.place(relx=0.5,rely=.865,anchor='center')

    # UPDATE (recursive function to update numbers)
    def updateData():
        root.after(REFRESH_RATE, updateData)

    # UPDATE/REFRESH
    root.after(REFRESH_RATE, updateData)

    # LOOP
    root.mainloop()

# [MAIN] Main Function. Where everything happens.
def main():   
    # Set up and start tkinter UI
    tkinter_thread = threading.Thread(target = tkinter)
    tkinter_thread.start()

    # Global Variables
    global isFrameBtnPressed
    global isFrameOpen
    
    # Setup variables to recieve frame information
    data = b""
    payload_size = struct.calcsize("Q")

    # Loop forever
    while True:
        while len(data) < payload_size:
            packet = s.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += s.recv(4*1024)
        
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        try:
            corners, ids =  findArucoMarkers(frame, 5, 50)
            coordinates = cornerloc(frame, corners, ids)
        except Exception as e:
            # print(f"No Codes Found! Error: {e}")
            pass
        if isFrameOpen:
            cv2.imshow("Drone Cam",frame)

        if isFrameBtnPressed:
            if not isFrameOpen:
                isFrameOpen = True
            else:
                isFrameOpen = False
                cv2.destroyWindow('Drone Cam')
            isFrameBtnPressed = False        
        # cv2.imshow("Drone Cam", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    s.close()

if __name__ == "__main__":
    main()