import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar
import random
import sys


SLEEPING = 0
TRIGGERED = 1
UPDOWN = 3
FLASHING = 5
RAINBOW = 4
PURPLE = 2
PURPLERAIN = 6

state = SLEEPING
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0

#read command line and set mode
mode = UPDOWN

if len(sys.argv) > 1:
    mode = int(sys.argv[1])

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
        drip_position_list = []
        drip_speed_list = []
        drip_start_position = 179
	state = PURPLERAIN
	
    if state == PURPLERAIN
	
	drip_random = random.randint(1, 100)
        if drip_random <= 5:
            drip_position_list.append(drip_start_position)
            drip_speed = random.randint(1, 3)  
            drip_speed_list.append(drip_speed)

        for drip in range(len(drip_position_list)):
            if drip >= len(drip_position_list):
                break
            if drip_position_list[drip] + drip_speed_list[drip] + 3 <= 179:
                strip.setPixelColor(drip_position_list[drip]+drip_speed_list[drip] + 3, 0)            
            if drip_position_list[drip] + drip_speed_list[drip] + 2 <= 179:
                strip.setPixelColor(drip_position_list[drip]+drip_speed_list[drip] + 2, 0)
            if drip_position_list[drip] + drip_speed_list[drip] + 1 <= 179:
                strip.setPixelColor(drip_position_list[drip]+drip_speed_list[drip] + 1, 0)
            if drip_position_list[drip] + drip_speed_list[drip] <= 179:
                strip.setPixelColor(drip_position_list[drip]+drip_speed_list[drip], 0)
            if drip_position_list[drip] + 3 <= 179:
                strip.setPixelColor(drip_position_list[drip]+3, makeColor(25, 0, 75))
            if drip_position_list[drip] + 2 <= 179:
                strip.setPixelColor(drip_position_list[drip]+2, makeColor(75, 0, 125))
            if drip_position_list[drip] + 1 <= 179:
                strip.setPixelColor(drip_position_list[drip]+1, makeColor(125, 0, 175))
            strip.setPixelColor(drip_position_list[drip], makeColor(205, 0, 255))
            #print drip_position_list[drip]
            drip_position_list[drip] = drip_position_list[drip] - drip_speed_list[drip]
            if drip_position_list[drip] <= 0:
                del drip_position_list[drip]
                del drip_speed_list[drip]


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
	
	elif state == PURPLE:
	    count = 0
	    color = 190
        
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
    elif state == PURPLE:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        for x in range(numpixels):
            strip.setPixelColor(x, colorWheel(color))
        count += 1
        if count >= 150:
            clear()
            state = SLEEPING
        

    strip.show()
#    print state, count, pos
    time.sleep(1.0 / 250)
    lasttrigger = currenttrigger 
