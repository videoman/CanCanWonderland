from Adafruit_I2C import Adafruit_I2C
import time

#Possible sensor addresses (suffix correspond to DIP switch positions)
SENSOR_ADDR_OFF_OFF = 0x26
SENSOR_ADDR_OFF_ON = 0x22
SENSOR_ADDR_ON_OFF = 0x24
SENSOR_ADDR_ON_ON = 0x20

#Set the sensor address here
sensorAddr = SENSOR_ADDR_ON_ON

i2c = Adafruit_I2C(0x20, bus=1)

#starts sensor watching proximity
i2c.write8(0x3, 0xFE)

while True:
    
    val = i2c.readU8(0)
    # the second bit is true, nothing is detected
    if val & 0x2:
        print "Nothing"
    
    else:
        print "Something"
    
    time.sleep(.5)


