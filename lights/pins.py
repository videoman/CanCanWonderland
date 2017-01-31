from dotstar import Adafruit_DotStar
import RPi.GPIO as GPIO

LED=16
IRLED=12
datapin   = 10
clockpin  = 11
numpixels = 180 # Number of LEDs in strip

strip     = Adafruit_DotStar(numpixels, datapin, clockpin, order="bgr")
strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle

head  = 0               # Index of first 'on' pixel
tail  = -10             # Index of last 'off' pixel
color = 0xFF0000        # 'On' color (starts red)

def makeColor(r, g, b):
    return (r << 16) + (g << 8) + b

def colorWheel(wheelPos):
    """
    0 is red, 85 is green, 170 is blue
    """
    if wheelPos < 85:
        return makeColor(255 - wheelPos * 3, wheelPos * 3, 0)

    elif wheelPos < 170:
        wheelPos -= 85
        return makeColor(0, 255 - wheelPos * 3, wheelPos * 3)

    else:
        wheelPos -= 170
        return makeColor(wheelPos * 3, 0, 255 - wheelPos * 3)


GPIO.setmode(GPIO.BCM)
# Turn off warnings...
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)

# Setup the Inputs
GPIO.setup(IRLED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
