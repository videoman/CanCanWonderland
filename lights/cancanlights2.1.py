import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar


SLEEPING = 0
TRIGGERED = 1
ANIMATING = 2

state = SLEEPING
count = 0
lasttrigger = 0
r = 255
g = 0
b = 0
step = 3

def beambreak():
    """returns true if beam is broken"""
    return GPIO.input(IRLED) == GPIO.HIGH
    
def setstatusLED(state):
    GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        strip.setPixelColor (x, color)     
        
def up():
    global count
    global b
    count += 1
    b += step
    color = makeColor(r, g, b)
    strip.setPixelColor (count, color)
    

while True:
    currenttrigger = beambreak()
    setstatusLED(currenttrigger)

    if state == SLEEPING:	
        if currenttrigger and not lasttrigger:
            state = TRIGGERED

    elif state == TRIGGERED:
        state = ANIMATING
        count = 0
        r = 255
        g = 0
        b = 0

    elif state == ANIMATING:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        elif count == numpixels:
            clear()
            state = SLEEPING
        else:
            up()
    
    strip.show()
    print r, g, b
    time.sleep(1.0 / 50)
    lasttrigger = currenttrigger 