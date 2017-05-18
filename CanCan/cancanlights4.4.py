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
ballmode = setupPURPLE
TRIGGERED = 1

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

sockbufs = {}

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
                    print "ball message coming through"
                    _, ball = r[:-1].split()
                    if int(ball) == pole:
                        print "ball message from simulator is for this pole"
                        return True
                except ValueError:
                    pass
    return False    
    
s = None
try: 
    program_id = pole
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
    else:
        return emulatorbeambreak()
    
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
<<<<<<< HEAD
        #data = s.recv(size)
        sb = sockbufs.get(repr(s), "") + s.recv(1024)
        print sb
        sockbufs[repr(s)] = ""
        for cmd in sb.splitlines(1):
            if not cmd.endswith("%"):
                sockbufs[repr(s)] = cmd
                break
            cmd = cmd[:-1]
            try:
                print "cmd " + cmd
                # try to read a command
                if cmd.startswith("set_pattern"):
                    _, pattern_message = cmd.split()
                    lhs, rhs = pattern_message.split("=", 1)
                    print lhs, "\n", rhs
                    if lhs == "0":
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
                            state = loopPURPLE
                        elif rhs == "set_pattern_screensaver_flashing":
                            print "set_pattern_screensaver_flashing"
                            screensavermode = loopFLASHING
                            state = loopFLASHING
                            print "state set_pattern_screensaver_flashing state=",state
                        elif rhs == "set_pattern_screensaver_updown":
                            print "set_pattern_screensaver_updown"
                            screensavermode = loopUPDOWN
                            state = loopUPDOWN
                        elif rhs == "set_pattern_screensaver_rainbow":
                            print "set_pattern_screensaver_rainbow"
                            screensavermode = loopRAINBOW
                            state = loopRAINBOW
                        else:            
                            sys.stdout.write(str(program_id))
                            sys.stdout.write("\n----------------------------\n")
                else:
                    pole, num, r, g, b = cmd.split()
                    setled(int(pole), int(num), (int(r), int(g), int(b)))
            except ValueError:
                print "got invalid", repr(cmd)
                raise
                continue


                #print "state change state=",state
=======
        data = s.recv(size)
        #print repr(data)
        if data == "": raise socket.error()
        lhs, rhs = data.split("=", 1)
        print lhs, "\n", rhs
        if lhs == "0":
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
                state = loopPURPLE
            elif rhs == "set_pattern_screensaver_flashing":
                print "set_pattern_screensaver_flashing"
                screensavermode = loopFLASHING
                state = loopFLASHING
                print "state set_pattern_screensaver_flashing state=",state
            elif rhs == "set_pattern_screensaver_updown":
                print "set_pattern_screensaver_updown"
                screensavermode = loopUPDOWN
                state = loopUPDOWN
            elif rhs == "set_pattern_screensaver_rainbow":
                print "set_pattern_screensaver_rainbow"
                screensavermode = loopRAINBOW
                state = loopRAINBOW
            else:            
                sys.stdout.write(str(program_id))
                sys.stdout.write(data)
                sys.stdout.write("\n----------------------------\n")
        #print "state change state=",state
>>>>>>> 79e1d04fe6b6410e4b79503f96b243b2b547970a
    except socket.error:
        #print "no message"
        pass
    
    if s and currenttrigger and not lasttrigger:
        ball_message = "%s=ball" % program_id
        print "44444444444444444444\n"
        print ball_message
        s.send(ball_message)
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
            endpos = 0
            colorspeed = colorlength/numpixels
            cycles = 0
            colorlength = 75.0
            state = FIREWORKS
            
    if state == FIREWORKS:
        if currenttrigger and not lasttrigger:
            clear()
            state = TRIGGERED
        count += 1
        pos += dir * colorspeed
        color = colorWheel(int(pos) % 255)
        #strip.setPixelColor(count, color)
        setlight(pos, colorWheel(color))
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
            state = SCREENSAVER

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
        drip_position_list = []
        drip_speed_list = []
        drip_start_position = 179
        state = PURPLERAIN

    if state == PURPLERAIN:
    
        drip_random = random.randint(1, 100)
        if drip_random <= 5:
            drip_position_list.append(drip_start_position)
            drip_speed = random.randint(1, 3)  
            drip_speed_list.append(drip_speed)

        for drip in range(len(drip_position_list)):
            if drip >= len(drip_position_list):
                break
            if drip_position_list[drip] + drip_speed_list[drip] + 3 <= 179:
                setlight(drip_position_list[drip]+drip_speed_list[drip] + 3, 0)            
            if drip_position_list[drip] + drip_speed_list[drip] + 2 <= 179:
                setlight(drip_position_list[drip]+drip_speed_list[drip] + 2, 0)
            if drip_position_list[drip] + drip_speed_list[drip] + 1 <= 179:
                setlight(drip_position_list[drip]+drip_speed_list[drip] + 1, 0)
            if drip_position_list[drip] + drip_speed_list[drip] <= 179:
                setlight(drip_position_list[drip]+drip_speed_list[drip], 0)
            if drip_position_list[drip] + 3 <= 179:
                setlight(drip_position_list[drip]+3, makeColor(25, 0, 75))
            if drip_position_list[drip] + 2 <= 179:
                setlight(drip_position_list[drip]+2, makeColor(75, 0, 125))
            if drip_position_list[drip] + 1 <= 179:
                setlight(drip_position_list[drip]+1, makeColor(125, 0, 175))
            setlight(drip_position_list[drip], makeColor(205, 0, 255))
            #print drip_position_list[drip]
            drip_position_list[drip] = drip_position_list[drip] - drip_speed_list[drip]
            if drip_position_list[drip] <= 0:
                del drip_position_list[drip]
                del drip_speed_list[drip]

    if sys.platform != "darwin":
        strip.show()
    
    else:
        show()

    #print "end of while loop state=",state
     
    
    print state, count, pos, cycles
    time.sleep(1.0 / 250)
    lasttrigger = currenttrigger
