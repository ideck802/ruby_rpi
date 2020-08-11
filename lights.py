import RPi.GPIO as GPIO
import apa102
from time import sleep

led = apa102.APA102(num_led=3)

color = [255, 0, 0]

def on():
    led.set_pixel(0, color[0], color[1], color[2], 50)
    led.set_pixel(1, color[0], color[1], color[2], 50)
    led.set_pixel(2, color[0], color[1], color[2], 50)
    led.show()
    
def off():
    led.set_pixel(0, 0, 0, 0, 50)
    led.set_pixel(1, 0, 0, 0, 50)
    led.set_pixel(2, 0, 0, 0, 50)
    led.show()

def set_color(red = 0, green = 0, blue = 0):
    global color
    color = [red, green, blue]

def pulse(times):
    divide = 40
    for i in range(times):
        for x in range(divide):
            led.set_pixel(0, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.set_pixel(1, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.set_pixel(2, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.show()
            sleep(0.05)
            
        for x in range(divide, -1, -1):
            led.set_pixel(0, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.set_pixel(1, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.set_pixel(2, round((color[0]/divide)*x), round((color[1]/divide)*x), round((color[2]/divide)*x), 50)
            led.show()
            sleep(0.05)

def flash(times):
    for i in range(times):
        led.set_pixel(0, color[0], color[1], color[2], 50)
        led.set_pixel(1, color[0], color[1], color[2], 50)
        led.set_pixel(2, color[0], color[1], color[2], 50)
        led.show()
        sleep(0.08)
        
        off()
        sleep(0.08)

#led.set_pixel(0, 0, 0, 0, 50)
#led.set_pixel(1, 0, 0, 0, 50)
#led.set_pixel(2, 0, 0, 0, 50)
#led.show()