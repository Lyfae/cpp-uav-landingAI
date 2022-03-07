#code for the client

from http import client
import socket
import cv2
import pickle
import struct

#create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
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

        #displaying our received frame
        cv2.imshow("Received",frame)
        
        #exitting 
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    #close the socket
    client_socket.close()

except KeyboardInterrupt:
    pass

        

