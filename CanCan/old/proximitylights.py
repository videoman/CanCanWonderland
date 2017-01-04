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

state = SLEEPING
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0

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

    currenttrigger = mysensor.check()
    setstatusLED(currenttrigger)

    if state == SLEEPING:
        if currenttrigger and not lasttrigger:
            state = TRIGGERED

    elif state == TRIGGERED:
        state = mode
        if state == UPDOWN:
            dir = 1
            count = 0
            pos = random.randint(0, 255)
            colorspeed = 85.0/numpixels
        
        elif state == FLASHING:
            count = 0
            color = color1
            color1 = random.randint(0,255)
            color2 = random.randint(0,255)
            cycles = 0
            
        elif state == RAINBOW:
            dir = 1
            count = 0
            pos = 0
            colorspeed = 210/numpixels
        
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
            
    elif state == FLASHING:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        for x in range(numpixels):
            strip.setPixelColor(x, colorWheel(color))
        count += 1
        if count >= 20:
            count = 0
            if color == color1:
                color = color2
            else:
                color = color1
            cycles += 1
            
        if cycles >= 8:
            clear()
            state = SLEEPING
    
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
            
        

    strip.show()
    print state, count, pos
    time.sleep(1.0 / 90)
    lasttrigger = currenttrigger 


