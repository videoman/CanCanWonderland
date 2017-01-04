#!/usr/bin/python

print "Hello World"
import RPi.GPIO as GPIO
import time
from pins import *
from dotstar import Adafruit_DotStar


GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

# Setup the Inputs
GPIO.setup(IRLED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(IRLED) == GPIO.LOW:
       	time.sleep(0.0001)  # wait 10 ms to give CPU chance to do other things
           
       # print("I saw the LED")
	GPIO.output(LED, False)
	strip.setPixelColor(head, 0)
	head += 1  
	if(head >= numpixels):
		head    = 0                    
	strip.show()                     # Refresh strip

    else: 
        #print("I saw an object")
        #GPIO.output(LED, True)
        strip.setPixelColor(head, color) # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)     # Turn off 'tail'
        strip.show()                     # Refresh strip
        time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)
        
        head += 1                        # Advance head position
        if(head >= numpixels):           # Off end of strip?
            head    = 0              # Reset to start
            color >>= 8              # Red->green->blue->black
            if(color == 0): color = 0xFF0000 # If black, reset to red

        tail += 1                        # Advance tail position
        if(tail >= numpixels): tail = 0  # Off end? Reset


