import socket
import cv2 
import pickle
import struct
import serial
import time

from _thread import *
import threading

# Global Variables
DATA_AMOUNT = 8
mainlist = []
for i in range(0, DATA_AMOUNT):
    mainlist.append(i)

# [THREAD] Code for the pi to recieve data from the client
def datarecv_client(conn, nano):
    print("Client Data Retrieval Thread Activated!")

    while True:
        try:
            msg = conn.recv(16).decode('utf-8') # Recieve data from the client
            if not msg:
                pass
            else:
                print(msg)
                nano.write(msg.encode('utf-8')) # Send data directly to arduino (single character only)
                nano.flush()
        except Exception as e:
            print(f"Error: {e}. Could not send data into arduino")
            
# [THREAD] Code for the pi to receive data from the nano
def datarecv_nano(conn, nano):
    print("Arduino Nano Data Retrieval Thread Activated!")
    global mainlist

    while True:
        data = nano.readline().decode('utf-8').split()
        if not data:
            print("No data found!")
        else:
            try:
                for x in range(0, DATA_AMOUNT):
                    mainlist[x] = data[x]
                print(mainlist)
            except:
                print(f"Letters detected: {data}")

# [THREAD] Takes camera feed and throws it into the socket between client-server
def servproc(conn, addr):
    print("Server Control Function Activated!")
    while True:
        if conn:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                # print(mainlist)
                img,frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                # print(message)
                conn.sendall(message)
                
                # cv2.imshow('TRANSMITTING VIDEO',frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    conn.close()

# [MAIN] Main function, where everything happens
def main():
    # Setup Server Variables
    HOST = '192.168.254.134'  # Standard loopback interface address (localhost)
    PORT = 8009        # Port to listen on (non-privileged ports are > 1023)
    BUFFER_SIZE = 8162 
    TIME_OUT = 10
    SENSOR_COUNT = 1

    # Bind to Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) #Bind system socket
    s.listen(SENSOR_COUNT) #Listen for up to SENSOR_COUNT connections
    s.settimeout(TIME_OUT) 
    print("Listening on %s:%s..." % (HOST, str(PORT)))

    # Server Activation
    conn,addr = s.accept()
    print('GOT CONNECTION FROM:',addr)

    # Setup Serial Connection
    RFreceiver = serial.Serial("/dev/ttyUSB0", 9600) # Data coming into pi at 9600 baud

    # Thread it (Send camera data to client)
    thread_server = threading.Thread(target = servproc, args = (conn, addr))
    thread_server.start()

    # Thread it again (Receive manual controller data from nano)
    thread_RF = threading.Thread(target = datarecv_nano, args = (conn, RFreceiver))
    thread_RF.start()

    # Thread it again again (Recieve autonomous client data, send to nano for drone control)
    thread_client = threading.Thread(target = datarecv_client, args = (conn, RFreceiver))
    thread_client.start()

if __name__ == "__main__":
    main()