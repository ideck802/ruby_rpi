import RPi.GPIO as GPIO
import os
from pixel_ring import pixel_ring
from time import sleep

color = [255, 0, 0]

    
def off():
    os.system("sudo python3 lights_sudo.py " + "off " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " 0")

def set_color(red = 0, green = 0, blue = 0):
    pass
    #pixel_ring.set_color(None, red, green, blue)

def pulse(times):
    os.system("sudo python3 lights_sudo.py " + "pulse " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(times))

def flash(times):
    os.system("sudo python3 lights_sudo.py " + "flash " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(times))


#set_color(color[0], color[1], color[2])
os.system("sudo python3 lights_sudo.py " + "off " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " 0")
os.system("sudo python3 lights_sudo.py " + "flash " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(5))
    
    
#led.set_pixel(0, 0, 0, 0, 50)
#led.set_pixel(1, 0, 0, 0, 50)
#led.set_pixel(2, 0, 0, 0, 50)
#led.show()