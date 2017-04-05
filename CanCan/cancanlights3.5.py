import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar
import random
import sys
import socket

SLEEPING = 0
TRIGGERED = 1
UPDOWN = 2
FLASHING = 5
RAINBOW = 4
PURPLE = 3

state = SLEEPING
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0

s = None
try: 
    program_id = socket.gethostname()[-1]
    host = '192.168.18.18'
    port = 50000
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.setblocking(0)
	
except Exception as e:
    print "network error", e

#read command line and set mode
mode = FLASHING

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

    if s and currenttrigger and not lasttrigger:
	s.send("%s=ball\n" % program_id)
	
    try:
        data = s.recv(size)
        lhs, rhs = data.split("=", 1)
        if lhs == program_id:
            if rhs == "got_ball_message":
                print "got_ball_message";
	    elif rhs == "pattern_idle_purple":
		mode = PURPLE;
                print "pattern_idle_purple"
	    elif rhs == "pattern_ball_purple":
		mode = PURPLE;
                print "pattern_ball_purple"
	    elif rhs == "pattern_idle_rainbow":
		mode = PURPLE;
                print "pattern_ball_rainbow"
	    elif rhs == "pattern_ball_rainbow":
		mode = PURPLE;
                print "pattern_ball_rainbow"
            else:            
                sys.stdout.write(str(program_id))
                sys.stdout.write(data)
                sys.stdout.write("\n----------------------------\n")
        elif lhs == "0":
            if rhs == "hole_in_one":
                print "hole in one message received"
    except socket.error:
        pass

    if state == SLEEPING:
	state = UPDOWN
	dir = 1
	count = 0
        pos = random.randint(0, 255)
        colorspeed = 85.0/numpixels

        count += dir
        pos += dir * colorspeed
        color = colorWheel(int(pos) % 255)
        strip.setPixelColor(count, color)
        strip.setPixelColor(count + 1, 0)
        if count < 0:
            clear()
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
