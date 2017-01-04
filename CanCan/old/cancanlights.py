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

def beambreak():
    """returns true if beam is broken"""
    return GPIO.input(IRLED) == GPIO.HIGH
    
def setstatusLED(state):
    GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        strip.setPixelColor (x, color)     

while True:
    currenttrigger = beambreak()
    setstatusLED(currenttrigger)

    if state == SLEEPING:	
        if currenttrigger and not lasttrigger:
            state = TRIGGERED

    elif state == TRIGGERED:
        state = ANIMATING
        count = 0

    elif state == ANIMATING:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        elif count == numpixels:
            clear()
            state = SLEEPING
        else:
            count += 1
            color = makeColor(255, 0, 255)
            strip.setPixelColor (count, color)
    
    strip.show()
    print state, count
    time.sleep(1.0 / 50)
    lasttrigger = currenttrigger 