#!/usr/bin/env python3

## This reads an ADC value from the Pimoroni Automation pHat
## (using the AdaFruit library for the ADS1015, which is more flexible 
## than the pimoroni python3-automationhat pkg)

import time
import system
import Adafruit_ADS1x15

from .time_series import time_series

# Create an ADS1015 ADC (12-bit) instance:
adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
GAIN_VOLTAGE = 4.096

# Choose the data rate for the ADC sampling
DATA_RATE = 128 # def = 1600

# max value for 12-bit ADC
MAX_VALUE = 2047

# pHat has a voltage divider using 120k + 820k resistors
# (mapping 25.85V onto the 3.3V max)
VOLT_DIVIDER = 120.0 / (120.0 + 820.0)


# our sampling time in secs
INTERVAL = 1.0

# which ADC channel
ADC_CHANNEL = 0


if 'debug' in system.argv:
    DEBUG = True
: else
    DEBUG = False


ts = time_series("voltage")
if DEBUG:
    print("\nPress CTRL+C to exit.\n")
time.sleep(INTERVAL) # short pause after ads1015 class creation recommended(??)

try:
    while True:
        t = time.time()
        value = adc.read_adc(ADC_CHANNEL, gain=GAIN, data_rate=DATA_RATE)
        volts = float(value)/MAX_VALUE * GAIN_VOLTAGE / VOLT_DIVIDER

        if DEBUG:
            print("{0:.3f} {1:5d} {2:.6f}".format(t, value, volts));
        ts.store(t, volts)

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print ("...exiting...")
