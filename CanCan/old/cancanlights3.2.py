import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar
import random


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

def beambreak():
    """returns true if beam is broken"""
    return GPIO.input(IRLED) == GPIO.HIGH
    
def setstatusLED(state):
    GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        strip.setPixelColor(x, color)
        
while True:
    currenttrigger = beambreak()
    setstatusLED(currenttrigger)

    if state == SLEEPING:
        if currenttrigger and not lasttrigger:
            state = TRIGGERED

    elif state == TRIGGERED:
        state = RAINBOW
        if state == UPDOWN:
            dir = 1
            count = 0
            pos = random.randint(0, 255)
            colorspeed = 85.0/numpixels
        
        elif state == FLASHING:
            count = 0
            color = 0
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
        if count >= 25:
            count = 0
            if color == 0:
                color = 170
            else:
                color = 0
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