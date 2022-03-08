#code for the client

from http import client
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np

#create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
# host_ip = '192.168.1.11'
port = 9999

#connection
client_socket.connect((host_ip,port)) # this value is a tuple
data = b""
#Q unsigned long int that takes 8 bytes
payload_size = struct.calcsize("Q") #set as string

try:
    while True:
        while len(data) < payload_size:
            #receiving the packets and appending them into the data
            packet = client_socket.recv(4*1024) #4k of byte buffer
            if not packet:
                break

            #adding packet to data
            data += packet
        #first 8 bytes contain size of packet message 
        packed_msg_size = data[:payload_size]
        #rest of data contains video frame
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]

        #looping til we receive all the data from the frame
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        #frame data is recovered
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        # Apply Grayscale
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Apply Gaussian Blur
        blur = cv2.GaussianBlur(grayscale, (9,9), 0)
    
        # Create Mask/Threshold
        threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 23, 3)
    
        # Find contours
        contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

		# Loop for all contours
        contnum = 0
        objectID = 0
        for c in contours:
            area = cv2.contourArea(c)
            # Only display contour for those having an area threshold of > 1000
            if area > 2500:
                contnum += 1
                M = cv2.moments(c)
                try:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                except:
                    print("Contour not found!")
    
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 7, (0,0,0), -1)
                cv2.putText(frame, "ID: " + str(objectID), (cX - 23, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                cv2.putText(frame, "Location: ({}, {})".format(cX, cY), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    
                objectID += 1
    
        # Display number of contours detected
        cv2.putText(frame, "# of contours: {}".format(contnum), (450, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)


        #displaying our received frame
        cv2.imshow("Received",frame)
        cv2.imshow("Threshhold",threshold)
        
        #exitting 
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    #close the socket
    client_socket.close()

except KeyboardInterrupt:
    pass

        