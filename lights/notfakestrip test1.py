import time
from dotstar import Adafruit_DotStar

numpixels = 96 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapin   = 23
clockpin  = 24
strip     = Adafruit_DotStar(numpixels, datapin, clockpin, order="bgr")

class fakeStrip:
    def __init__(self, len):
        self.len = len
        self.data = [" "] * len

    def setPixelColor(self, pos, color):
        if color:
            self.data[pos] = "*"
        else:
            self.data[pos] = " "

    def show(self):
        print "".join(self.data)

# strip = fakeStrip(50)

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle


head  = 0               # Index of first 'on' pixel
tail  = -10             # Index of last 'off' pixel
color = 0xFF0000        # 'On' color (starts red)
pixels = 50
delay = .001

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


while True:
    
    for j in reversed(range(pixels)):
        for i in range(j):
            strip.setPixelColor(i, 0xFF0000)
            strip.show()
            strip.setPixelColor(i, 0)
            time.sleep(delay)
        strip.setPixelColor(i, 0xFF0000)


