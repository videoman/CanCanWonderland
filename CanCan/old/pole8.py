#! /usr/bin/python3
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO
from pins import *
from dotstar import Adafruit_DotStar
import random
import threading
import sys
import select
import time
import socket

#Possible sensor addresses (suffix correspond to DIP switch positions)
SENSOR_ADDR_OFF_OFF = 0x26
SENSOR_ADDR_OFF_ON = 0x22
SENSOR_ADDR_ON_OFF = 0x24
SENSOR_ADDR_ON_ON = 0x20

#Set the sensor address here
sensorAddr = SENSOR_ADDR_ON_ON

# Light stuff
SLEEPING = 0
TRIGGERED = 1
UPDOWN = 2
FLASHING = 3
RAINBOW = 4
FIREWORKS = 5
FIREWORKS2 = 6

state = SLEEPING
count = 0
lasttrigger = 0
step = 2
pos = 0
color1 = 0
color2 = 0
cycles = 0
endpos = 0
startpos = 0
colorlength = 75.0

#read command line and set mode
mode = FLASHING



class sensor:
    def __init__(self, addr, bus):
        self.i2c = Adafruit_I2C(0x20, bus=1)
        #starts sensor watching proximity
        self.i2c.write8(0x3, 0xFE)
        
    def check(self):
        val = self.i2c.readU8(0)
        # the second bit is true, nothing is detected
        if val & 0x2:
            #print "Nothing"
            return False
            
        else:
            #print "Something"
            return True


# placeholder class to deal with the process that manages
class LightStrip (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        print "Exiting " + self.name
    def hole_in_one_pattern(self):
        self.clear()
        print "\n()()()()()()()()()()()()\n"
        print "Make the hole in one lights go"
        print "\n()()()()()()()()()()()()\n"
        
        for x in range(numpixels):
            strip.setPixelColor(x, 255)
        strip.show()
        time.sleep(1)
        self.clear()
    def ball_sensed(self):
        self.clear()
        print "\n()()()()()()()()()()()()\n"
        print "I saw a ball"
        print "\n()()()()()()()()()()()()\n"
        pattern = random.randint(0, 1)
        if pattern:
            self.updown()
        else:
            self.flashing()
        #for x in range(numpixels):
        #    strip.setPixelColor(x, 30)
        #strip.show()
        time.sleep(1)
        self.clear()
    def clear(self):
        color = 0
        for x in range(numpixels):
            strip.setPixelColor(x, color)
        strip.show()
    def updown(self):
        print "\n()()()()()()()()()()()()\n"
        print "UPDOWN"
        print "\n()()()()()()()()()()()()\n"
        dir = 1
        count = 0
        pos = random.randint(0, 255)
        colorspeed = colorlength/numpixels
        for x in range(numpixels):
            time.sleep(1.0/150.0)
            count += dir
            pos += dir * colorspeed
            color = colorWheel(int(pos) % 255)
            strip.setPixelColor(count, color)
            strip.show()
        dir = -1
        for x in reversed(range(numpixels)):
            time.sleep(1.0/150.0)
            count += dir
            pos += dir * colorspeed
            color = colorWheel(int(pos) % 255)
            strip.setPixelColor(count+1, 0)
            strip.setPixelColor(count, color)
            strip.show()
            
    def flashing(self):
        print "\n()()()()()()()()()()()()\n"
        print "FLASHING"
        print "\n()()()()()()()()()()()()\n"
        pos = random.randint(0,255)
        color1 = colorWheel(int(pos) % 255)
        print "color1 is %d" % color1
        pos2 = random.randint(0,255)
        color2 = colorWheel(int(pos2) % 255)
        print "color2 is %d" % color2
        for z in range(1, 8):
            for x in range(numpixels):
                strip.setPixelColor(x, color1)
            strip.show()
            time.sleep(1.0/5)
            for y in range(numpixels):
                strip.setPixelColor(y, color2)
            strip.show()
            time.sleep(1.0/5)
        
    
#            strip.setPixelColor(count + 1, 0)
#            if count < 0:
#                clear()
#                state = SLEEPING
#                
#            if count == numpixels:
#                dir = -1



"""Check for input every 0.1 seconds. Treat available input
immediately, but do something else if idle."""


mysensor = sensor(0x20, 1)

program_id = 1
host = 'localhost'
port = 50000
size = 1024
global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.setblocking(0)

# files monitored for input
read_list = [sys.stdin]
# select() should wait for this many seconds for input.
# A smaller number means more cpu usage, but a greater one
# means a more noticeable delay between input becoming
# available and the program starting to work on it.
timeout = 0.1 # seconds
last_work_time = time.time()
data = "default data"

def treat_input(linein):
  global last_work_time
  global s
  global pole
  print("Sending message from prompt:", linein)
  message_to_send = str(program_id) + "=" + linein
  s.send(message_to_send)
  try:
    data = s.recv(size)
    print("Message received after prompt send:", data)
    lhs, rhs = data.split("=", 1)
    print("lhs:", lhs)
    print("rhs:", rhs)
    if lhs == program_id:
      if rhs == "got_message":
        print ""
      else:            
        sys.stdout.write(str(program_id))
        sys.stdout.write("data is:" + data + ":")
        sys.stdout.write("\n=======================\n")
    elif lhs == "0":
      if rhs == "hole_in_one":
        pole.hole_in_one_pattern()
  except socket.error:
    pass
  sys.stdout.write("\n++++++++++++++++++++++++\n")
  #time.sleep(1) # working takes time
  print('Done')
  last_work_time = time.time()

def idle_work():
  global last_work_time
  global s
  global pole
  now = time.time()
  currenttrigger = mysensor.check()
  if currenttrigger:
    message_to_send = str(program_id) + "=" + "ball0"
    pole.ball_sensed()
    s.send(message_to_send)
  #s.send(message_to_send)
  try:
    data = s.recv(size)
    lhs, rhs = data.split("=", 1)
    lhs, rhs = data.split("=", 1)
    if lhs == program_id:
      if rhs == "got_message":
        print ""
      else:            
        sys.stdout.write(str(program_id))
        sys.stdout.write(data)
        sys.stdout.write("\n----------------------------\n")
    elif lhs == "0":
      if rhs == "hole_in_one":
        pole.hole_in_one_pattern()
  except socket.error:
    pass
    
  # do some other stuff every 2 seconds of idleness
  if now - last_work_time > 2:
    last_work_time = now

def main_loop():
  global read_list
  global pole
  pole = LightStrip(1, "Pole", 1)
  # while still waiting for input on at least one file
  while read_list:
    ready = select.select(read_list, [], [], timeout)[0]
    if not ready:
      idle_work()
    else:
      for file in ready:
        line = file.readline()
        if not line: # EOF, remove file from input list
          read_list.remove(file)
        elif line.rstrip(): # optional: skipping empty lines
          treat_input(line)

try:
    main_loop()
except KeyboardInterrupt:
  pass