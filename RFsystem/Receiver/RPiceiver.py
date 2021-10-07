import sys
import serial
import time
import socket

from _thread import *
import threading

def Main():
    serNano = serial.Serial("/dev/ttyUSB0", 115200)
    while(True):
        try:
            data = serNano.readline().decode('utf-8').split()
            print(data)
        except KeyboardInterrupt as e:
            print(e)
            break

if __name__ == '__main__': 
    Main() 