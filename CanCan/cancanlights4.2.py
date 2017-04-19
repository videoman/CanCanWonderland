import time
from pins import *
import random
import sys
import socket
import select
if sys.platform != "darwin":
    import RPi.GPIO as GPIO
    from dotstar import Adafruit_DotStar
    

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
FIREWORKS = 6
loopFIREWORKS = 106
setupFIREWORKS = 206
FIREWORKS2 = 7
loopFIREWORKS2 = 107
setupFIREWORKS2 = 207
PURPLERAIN = 8
loopPURPLERAIN = 108
setupPURPLERAIN = 208



state = SCREENSAVER
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0
colorlength = 75.0

pole = int(sys.argv[2])
leds = 180

def setled(num, color):
    emulator.send("%d %d %d %d %d\n" % (pole, num, color[0], color[1], color[2]))
    
def show():
    emulator.send("show %d\n" % pole)

if sys.platform == "darwin":
    emulator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "connecting..."
    emulator.connect(('localhost', 5555))
    print "connected"
    
def setlight(pixel, color):
    if sys.platform != "darwin":
        strip.setPixelColor(pixel, color)        
    else:
        r = (color >> 16) & 255
        g = (color >> 8) & 255
        b = (color & 255) 
        #print color, hex(color), r, g, b
        setled(pixel, (r, g, b))    
 
    
def emulatorbeambreak():
    ready, _, _ = select.select([emulator], [], [], 0)
    if ready:
        r = emulator.recv(100)
        cmds = ""
        while r:
            cmds += r
            if r.endswith("\n"):
                break
            r = emulator.recv(100)

        if not r:
            print "disconnected"
            sys.exit()

        for cmd in cmds.splitlines():
            if cmd.startswith("ball"):
                try:
                    _, ball = r[:-1].split()
                    if int(ball) == pole:
                        return True
                except ValueError:
                    pass
    return False    
    

s = None
try: 
    program_id = socket.gethostname()[-1]
    if sys.platform == "darwin":
        host = 'localhost'
    else:
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
    if sys.platform != "darwin":
        """returns true if beam is broken"""
        return GPIO.input(IRLED) == GPIO.HIGH
    
def setstatusLED(state):
    if sys.platform != "darwin":
        GPIO.output(LED, state)

def clear():
    color = 0
    for x in range(numpixels):
        #strip.setPixelColor(x, color)
        setlight(x, color)
        
while True:
    currenttrigger = beambreak()
    setstatusLED(currenttrigger)
    
    try:
        data = s.recv(size)
        lhs, rhs = data.split("=", 1)
        if lhs == program_id:
            if rhs == "got_ball_message":
                print "got_ball_message"
            elif rhs == "set_pattern_ball_purple":
                print "set_pattern_ball_purple"
                ballmode = setupPURPLE
            elif rhs == "set_pattern_ball_flashing":
                print "set_pattern_ball_flashing"
                ballmode = setupFLASHING
            elif rhs == "set_pattern_ball_updown":
                print "set_pattern_ball_updown"
                ballmode = setupUPDOWN
            elif rhs == "set_pattern_ball_rainbow":
                print "set_pattern_ball_rainbow"
                ballmode = setupRAINBOW
            elif rhs == "set_pattern_screensaver_purple":
                print "set_pattern_screensaver_purple"
                screensavermode = loopPURPLE
            elif rhs == "set_pattern_screensaver_flashing":
                print "set_pattern_screensaver_flashing"
                screensavermode = loopFLASHING
            elif rhs == "set_pattern_screensaver_updown":
                print "set_pattern_screensaver_updown"
                screensavermode = loopUPDOWN
            elif rhs == "set_pattern_screensaver_rainbow":
                print "set_pattern_screensaver_rainbow"
                screensavermode = loopRAINBOW
            else:            
                sys.stdout.write(str(program_id))
                sys.stdout.write(data)
                sys.stdout.write("\n----------------------------\n")
        elif lhs == "0":
            if rhs == "hole_in_one":
                print "hole in one message received"
    except socket.error:
        pass

    if s and currenttrigger and not lasttrigger:
        s.send("%s=ball\n" % program_id)
        state = ballmode

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
        #strip.setPixelColor(count, color)
        #strip.setPixelColor(count + 1, 0)
        setlight(count, color)
        setlight(count + 1, 0)
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
            #strip.setPixelColor(x, colorWheel(color))
            setlight(x, colorWheel(color))
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
        #strip.setPixelColor(count, color)
        #strip.setPixelColor(count + 1, 0)
        setlight(count, color)
        setlight(count + 1, 0)
               
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
            #strip.setPixelColor(x, colorWheel(color))
            setlight(x, colorWheel(color))
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
            
            
    #FIREWORKS PATTERN
    if state == loopFIREWORKS:
        screensavermode = setupFIREWORKS
        state = setupFIREWORKS
    if state == setupFIREWORKS:
            dir = 1
            count = 0
            startpos = random.randint(0, 255)
            pos = startpos
            colorspeed = colorlength/numpixels
            cycles = 0
    if state == FIREWORKS:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED
        count += 1
        pos += dir * colorspeed
        color = colorWheel(int(pos) % 255)
        #strip.setPixelColor(count, color)
        setlight(x, colorWheel(color))
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

    #FIREWORKS2 PATTERN
    if state == loopFIREWORKS2:
        screensavermode = setupFIREWORKS2
        state = setupFIREWORKS2
    if state == setupFIREWORKS2:
            count = 0
            color = color1
            color1 = startpos
            color2 = startpos + colorlength % 255
            cycles = 0
    if state == FIREWORKS2:
        for x in range(numpixels):
            #strip.setPixelColor(x, colorWheel(color % 255))
            setlight(x, colorWheel(color))
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
            state = SCREENSAVER
            
            
    #PURPLERAIN PATTERN
    if state == loopPURPLERAIN:
        screensavermode = setupPURPLERAIN
        state = setupPURPLERAIN

    if state == setupPURPLERAIN:
        count = 0
        color = 190
        state = PURPLERAIN
        # drip
        drip_position_list = []
        drip_speed_list = []
        drip_count = 5
        for drip in range(drip_count):
            drip_position = random.randint(0, numpixels-1)
            drip_position_list.append(drip_position)
            drip_speed = random.randint(1, 4)
            drip_speed_list.append(drip_speed)
        drip_color = 190
        drip_speed = 1

    if state == PURPLERAIN:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED
        clear()
        for drip in range(drip_count):
            setlight(drip_position_list[drip]+1, 0)
            #setlight(drip_position_list[drip]+3, colorWheel(drip_color-3))
            #setlight(drip_position_list[drip]+2, colorWheel(drip_color-2))
            #setlight(drip_position_list[drip]+1, colorWheel(drip_color-1))
            setlight(drip_position_list[drip], colorWheel(drip_color))
            drip_position_list[drip] = drip_position_list[drip] - drip_speed_list[drip]
            if drip_position_list[drip] <= 0:
                drip_position_list[drip] = numpixels-1

    if sys.platform != "darwin":
        strip.show()
    
    else:
        show()


     
    
    #    print state, count, pos
    time.sleep(1.0 / 250)
    lasttrigger = currenttrigger
