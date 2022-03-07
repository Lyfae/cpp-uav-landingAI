#code for the server
import socket
import cv2
import pickle
import struct
import imutils

#create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
host_ip = '192.168.1.12'

#connection output status
print("Host IP:", host_ip)

#set port and socket
port = 5000
socket_address = (host_ip,port)

#binding the socket
server_socket.bind(socket_address)

#socket listen
server_socket.listen(5)
print("Listening At: ",socket_address)

#socket accept
try:
    while True:
        client_socket,addr = server_socket.accept()
        print("Getting Connetion From:", addr)
        #upon successful connection
        if client_socket:
            vid = cv2.VideoCapture(0)
            #while video feed is opened
            while(vid.isOpened()):
                img,frame = vid.read()
                frame = imutils.resize(frame,width=320)
                a = pickle.dumps(frame)           
                message = struct.pack("Q",len(a)) + a
                client_socket.sendall(message)
                cv2.imshow("Transmitting Video",frame)
                key = cv2.waitKey(1) & 0xFF

                #closing socket 
                if key == ord('q'):
                    client_socket.close()
except KeyboardInterrupt:
    pass

