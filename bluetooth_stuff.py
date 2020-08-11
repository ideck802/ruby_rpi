import serial

port = serial.Serial("/dev/rfcomm0", baudrate=9600)
    
def turnoff():
    port.write('0'.encode('utf-8'))
    
def turnon():
    port.write('1'.encode('utf-8'))