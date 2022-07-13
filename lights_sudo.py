from pixel_ring import pixel_ring
import sys
import time

color = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]

def off():
    pixel_ring.off()

def set_color():
    pixel_ring.show([color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,
                     color[0], color[1], color[2], 0,])
    
def pulse():
    for i in range(int(sys.argv[5])):
        for j in range(12):
            pixel_ring.show(([0, 0, 0, 0] * (j-1)) + [color[0], color[1], color[2], 0] + ([0, 0, 0, 0] * (12-j)))
            time.sleep(0.05)
    
def flash():
    for i in range(int(sys.argv[5])):
        for j in range(12):
            pixel_ring.show([color[0], color[1], color[2], 0] * 12)
            time.sleep(0.05)
            pixel_ring.off()
            time.sleep(0.05)

exec(sys.argv[1] + "()")