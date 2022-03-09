#code for the client

from http import client
import socket
import cv2
import pickle
import struct
import imutils
import numpy as np

#create socket
client_data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
host_ip = 'localhost'
port = 9999

#connection
client_data_socket.connect((host_ip,port)) # this value is a tuple

print("Connection Successful")
# #socket accept
# try:
#     while True:
#         client_socket,addr = client_data_socket.accept()
#         print("Getting Connetion From:", addr)
#         #upon successful connection
#         if client_socket:
#             vid = cv2.VideoCapture(0)
#             #while video feed is opened
#             while(vid.isOpened()):
#                 img,frame = vid.read()
#                 frame = imutils.resize(frame,width=320)
#                 a = pickle.dumps(frame)           
#                 message = struct.pack("Q",len(a)) + a
#                 client_socket.sendall(message)
#                 cv2.imshow("Transmitting Video",frame)
#                 key = cv2.waitKey(1) & 0xFF

#                 #closing socket 
#                 if key == ord('q'):
#                     client_socket.close()
# except KeyboardInterrupt:
#     pass
