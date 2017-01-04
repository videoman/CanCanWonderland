import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar


SLEEPING = 0
TRIGGERED = 1
ANIMATING = 2
UP = 3
DOWN = 4

dir = UP
state = SLEEPING
count = 0
lasttrigger = 0
r = 255
g = 0
b = 0
step = 2

def beambreak():
    """returns true if beam is broken"""
    return GPIO.input(IRLED) == GPIO.HIGH
    
def setstatusLED(state):
    GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        strip.setPixelColor (x, color)
        
def goup():
    global count
    global b
    global r
    count += 1
    b += step
    r -= step
    color = makeColor(r, g, b)
    strip.setPixelColor (count, color)
    
def godown():
    global count
    global b
    global r
    count -= 1
    b -= step
    r += step
    color = makeColor(r, g, b)
    strip.setPixelColor (count, color)
    strip.setPixelColor (count + 1, 0)

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
        
        if dir == UP:
            goup()
                   
        if dir == DOWN:
            godown()
            
        if count < 0:
            clear()
            state = SLEEPING
            dir = UP
            
        if count == numpixels:
            dir = DOWN
            godown()


    strip.show()
    print state, dir, count, r, g, b
    time.sleep(1.0 / 90)
    lasttrigger = currenttrigger 