from Adafruit_I2C import Adafruit_I2C
import time
import RPi.GPIO as GPIO
from pins import *
from dotstar import Adafruit_DotStar
import random
import sys


#Possible sensor addresses (suffix correspond to DIP switch positions)
SENSOR_ADDR_OFF_OFF = 0x26
SENSOR_ADDR_OFF_ON = 0x22
SENSOR_ADDR_ON_OFF = 0x24
SENSOR_ADDR_ON_ON = 0x20

#Set the sensor address here
sensorAddr = SENSOR_ADDR_ON_ON


SLEEPING = 0
TRIGGERED = 1
UPDOWN = 2
FLASHING = 3
RAINBOW = 4
FIREWORKS = 5
FIREWORKS2 = 6

state = SLEEPING
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0
cycles = 0
endpos = 0
startpos = 0
colorlength = 75.0

#read command line and set mode
mode = FLASHING

if len(sys.argv) > 1:
    mode = int(sys.argv[1])

class sensor:
    def __init__(self, addr, bus):
        self.i2c = Adafruit_I2C(0x20, bus=1)
        #starts sensor watching proximity
        self.i2c.write8(0x3, 0xFE)
        
    def check(self):
        val = self.i2c.readU8(0)
        # the second bit is true, nothing is detected
        if val & 0x2:
            print "Nothing"
            return False
            
        else:
            print "Something"
            return True
            
            
mysensor = sensor(0x20, 1)
    
def setstatusLED(state):
    GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        strip.setPixelColor(x, color)

while True:
    #sensor checks for ball
    currenttrigger = mysensor.check()
    setstatusLED(currenttrigger)
    
    #sleeping mode looks for trigger
    if state == SLEEPING:
        if currenttrigger and not lasttrigger:
            state = TRIGGERED
    #triggered mode sends it to one of the light programs
    elif state == TRIGGERED:
        state = mode
        #updown lights
        if state == UPDOWN:
            dir = 1
            count = 0
            pos = random.randint(0, 255)
            colorspeed = colorlength/numpixels
        #flashing between 2 colors
        elif state == FLASHING:
            count = 0
            color = color1
            color1 = random.randint(0,255)
            color2 = random.randint(0,255)
            cycles = 0
        #rainbow lights
        elif state == RAINBOW:
            dir = 1
            count = 0
            pos = 0
            colorspeed = 210/numpixels
        #fireworks lights
        elif state == FIREWORKS:
            dir = 1
            count = 0
            startpos = random.randint(0, 255)
            pos = startpos
            colorspeed = colorlength/numpixels
            cycles = 0
        #fireworks2
        elif state == FIREWORKS2:
            count = 0
            color = color1
            color1 = startpos
            color2 = startpos + colorlength % 255
            cycles = 0

    #clears lights and picks a random color and then cycles through the colors around color wheel
    elif state == UPDOWN:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        
        count += dir
        pos += dir * colorspeed
        color = colorWheel(int(pos) % 255)
        strip.setPixelColor(count, color)
        strip.setPixelColor(count + 1, 0)
        if count < 0:
            clear()
            state = SLEEPING
            
        if count == numpixels:
            dir = -1
            
    #clears lights flashes between two random colors
    elif state == FLASHING:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        for x in range(numpixels):
            strip.setPixelColor(x, colorWheel(color))
        count += 1
        if count >= 10:
            count = 0
            if color == color1:
                color = color2
            else:
                color = color1
            cycles += 1
            
        if cycles >= 8:
            clear()
            state = SLEEPING
            
    #cycles through whole rainbow
    elif state == RAINBOW:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        
        count += dir
        pos += dir * colorspeed
        color = colorWheel(pos)
        strip.setPixelColor(count, color)
        strip.setPixelColor(count + 1, 0)
               
        if count < 0:
            clear()
            state = SLEEPING
            
        if count == numpixels:
            dir = -1
            
    #cycles through fireworks
    elif state == FIREWORKS:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED
        count += 1
        pos += dir * colorspeed
        color = colorWheel(int(pos) % 255)
        strip.setPixelColor(count, color)
        if count >= numpixels:
            endpos = pos
            pos = startpos
            cycles += 1
            count = 0
            clear()
            
        if cycles >= 3:
            clear()
            count = 0
            color1 = startpos + int(colorlength % 255)
            color2 = startpos + int(colorlength + 20 % 255)
            color = color1
            cycles = 0
            state = FIREWORKS2

    #fireworks2
    elif state == FIREWORKS2:
        for x in range(numpixels):
            strip.setPixelColor(x, colorWheel(color % 255))
        count += 1
        if count >= 20:
            count = 0
            if color == color1:
                color = color2
            else:
                color = color1
            cycles += 1
            
        if cycles >= 10:
            clear()
            
            cycles = 0
            state = SLEEPING
            


    strip.show()
    print pos
    time.sleep(1.0 / 150)
    lasttrigger = currenttrigger 


