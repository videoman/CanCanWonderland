#!/usr/bin/python

print "Hello World"
import RPi.GPIO as GPIO
import time
from dotstar import Adafruit_DotStar

numpixels = 30 # Number of LEDs in strip

#from threading import Thread
#from neopixel import *		

GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

LED=16
IRLED=12
# Here's how to control the strip from any two GPIO pins:
datapin   = 10
clockpin  = 11
strip     = Adafruit_DotStar(numpixels, datapin, clockpin)


#LED_COUNT = 6
#LED_PIN = 18
#LED_FREQ_HZ = 800000
#LED_DMA = 5
#LED_BRIGHTNESS = 255
#LED_INVERT = False

#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,  LED_BRIGHTNESS)
#strip.begin()
#def colorWipe(strip, color, wait_ms=50):
#	for i in range(strip.numPixels()):
#		strip.setPixelColor(i, color)
#		strip.show()
#		time.sleep(wait_ms/1000.0)

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

head  = 0               # Index of first 'on' pixel
tail  = -10             # Index of last 'off' pixel
color = 0xFF0000        # 'On' color (starts red)
pixels = 30
delay = .01

GPIO.setup(LED, GPIO.OUT)

# Setup the Inputs
# Button one is the selector switch.
GPIO.setup(IRLED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



#def my_callback_sel(IRLED):
#
#GPIO.add_event_detect(IRLED, GPIO.FALLING, callback=my_callback_sel, bouncetime=200)

def makeColor(r, g, b):
    return (r << 16) + (g << 8) + b

def colorWheel(wheelPos):
    if wheelPos < 85:
        return makeColor(wheelPos * 3, 255 - wheelPos * 3, 0)
    elif wheelPos < 170:
        wheelPos -= 85
        return makeColor(0, wheelPos * 3, 255 - wheelPos * 3)
    else:
        wheelPos -= 170
        return makeColor(255 - wheelPos * 3, 0, wheelPos * 3)

def prog1():
    for j in reversed(range(pixels)):
        for i in range(j):
            strip.setPixelColor(i, 0xFF0000)
            strip.show()
            strip.setPixelColor(i, 0)
            time.sleep(delay)
        strip.setPixelColor(i, 0xFF0000)



while True:
    if GPIO.input(IRLED) == GPIO.LOW:
       	time.sleep(0.0001)  # wait 10 ms to give CPU chance to do other things    
        # print("I saw the LED")
	GPIO.output(LED, False)
    for j in reversed(range(pixels)):
        for i in range(j):
            strip.setPixelColor(i, 0)
            strip.show()
            time.sleep(delay)

	#colorWipe(strip, Color(0,255,0))
    else: 
        #print("I saw an object")
        #GPIO.output(LED, True)  
        prog1()
        
