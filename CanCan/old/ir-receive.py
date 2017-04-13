#!/usr/bin/python

print "Hello World"

import RPi.GPIO as GPIO
import time 
from threading import Thread

GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

LED=23
IRLED=18

GPIO.setup(LED, GPIO.OUT)

# Setup the Inputs
# Button one is the selector switch.
GPIO.setup(IRLED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



#def my_callback_sel(IRLED):
#
#GPIO.add_event_detect(IRLED, GPIO.FALLING, callback=my_callback_sel, bouncetime=200)

while True:
    if GPIO.input(IRLED) == GPIO.LOW:
       time.sleep(0.0001)  # wait 10 ms to give CPU chance to do other things    
       # print("I saw the LED")
       GPIO.output(LED, False)
    else: 
       #print("I saw and object")
       GPIO.output(LED, True)
   

