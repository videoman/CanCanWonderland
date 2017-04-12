
import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar
import random
import sys
import socket

SCREENSAVER = 0
UPDOWN = 2
loopUPDOWN = 102
setupUPDOWN = 202
PURPLE = 3
loopPURPLE = 103
setupPURPLE = 203
RAINBOW = 4
loopRAINBOW = 104
setupRAINBOW = 204
FLASHING = 5
loopFLASHING = 105
setupFLASHING = 205



state = SCREENSAVER
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

#read command line and set screensavermode
screensavermode = FLASHING

if len(sys.argv) > 1:
    screensavermode = int(sys.argv[1])

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
                print "got_ball_message"
            elif rhs == "set_pattern_ball_purple":
                print "set_pattern_ball_purple"
                screensavermode = setupPURPLE
            elif rhs == "set_pattern_ball_flashing":
                print "set_pattern_ball_flashing"
                screensavermode = setupFLASHING
            else:            
                sys.stdout.write(str(program_id))
                sys.stdout.write(data)
                sys.stdout.write("\n----------------------------\n")
        elif lhs == "0":
            if rhs == "hole_in_one":
                print "hole in one message received"
    except socket.error:
        pass

    if state == SCREENSAVER:
        state = screensavermode
        
    #UPDOWN PATTERN
    if state == loopUPDOWN:
        screensavermode = setupUPDOWN
        state = setupUPDOWN
        
    if state == setupUPDOWN:
        dir = 1
        count = 0
        pos = random.randint(0, 255)
        colorspeed = 85.0/numpixels
        state = UPDOWN
        
    if state == UPDOWN:
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
            state = SCREENSAVER
            
        if count == numpixels:
            dir = -1
            
    #PURPLE PATTERN
    if state == loopPURPLE:
        screensavermode = setupPURPLE
        state = setupPURPLE

    if state == setupPURPLE:
        count = 0
        color = 190
        state = PURPLE

    if state == PURPLE:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED 
        for x in range(numpixels):
            strip.setPixelColor(x, colorWheel(color))
        count += 1
        if count >= 150:
            clear()
            state = SCREENSAVER
    
    #RAINBOW PATTERN        
    if state == loopRAINBOW:
        screensavermode = setupRAINBOW
        state = setupRAINBOW
        
    if state == setupRAINBOW:
        dir = 1
        count = 0
        pos = 0
        colorspeed = 210/numpixels
        state = RAINBOW
        
    if state == RAINBOW:
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
            state = SCREENSAVER
            
        if count == numpixels:
            dir = -1

    #FLASHING PATTERN
    if state == loopFLASHING:
        screensavermode = setupFLASHING
        state = setupFLASHING
        
    if state == setupFLASHING:
        count = 0
        color = color1
        color1 = random.randint(0,255)
        color2 = random.randint(0,255)
        cycles = 0
        state = FLASHING
        
    if state == FLASHING:
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
            state = SCREENSAVER
            
            
        

    strip.show()
#    print state, count, pos
    time.sleep(1.0 / 250)
    lasttrigger = currenttrigger
