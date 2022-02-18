from subprocess import Popen
import serial
import time
import threading
import time

def connect_bluetooth():
    Popen("sudo rfcomm connect hci0 98:D3:11:F8:64:35", shell=True)

try:
    port = serial.Serial("/dev/rfcomm0", baudrate=9600)
except:
    connect_bluetooth = threading.Thread(target=connect_bluetooth)
    connect_bluetooth.start()
    time.sleep(10)
    port = serial.Serial("/dev/rfcomm0", baudrate=9600)

at_home = True

def im_home():
    global at_home
    at_home = not at_home

def init_door_detector(door_detected):

    i = 0

    while 1:
        data = port.readline(1024)
        i+=1

        if i > 300 and data and "door_trigger" in str(data):
            i = 0
            door_detected()
            im_home()

