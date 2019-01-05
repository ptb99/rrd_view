#!/usr/bin/env python3

## This reads a TMP36 sensor attached to a Pimoroni Automation pHat ADC
## (using the AdaFruit library for the ADS1015, which is more flexible
## than the pimoroni python3-automationhat pkg)

import time
import sys
import Adafruit_ADS1x15
from time_series import TimeSeries


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


def temp(volt):
    """Convert analog voltage to temperature in C"""
    # TMP36 reads 0V at -50C and 2V at +150C
    return 100*volt - 50


if 'debug' in sys.argv:
    DEBUG = True
else:
    DEBUG = False


ts = TimeSeries(["temp"])

if DEBUG:
    print("\nPress CTRL+C to exit.\n")
time.sleep(INTERVAL) # short pause after ads1015 class creation recommended(??)

try:
    while True:
        t = time.time()

        value = adc.read_adc(ADC_CHANNEL, gain=GAIN, data_rate=DATA_RATE)
        volts = float(value)/MAX_VALUE * GAIN_VOLTAGE / VOLT_DIVIDER
        temp_C = temp(volts)
        temp_F = 9*temp_C/5 + 32

        if DEBUG:
            form = 't={time:.3f} - val= {volt:.3f} V  ==  {temp:.3f} C / {temp_F:.3f} F'
            print (form.format(time=t, volt=volts, temp=temp_C, temp_F=temp_F))
        ts.store(t, [temp_F])

        # hang out and do nothing for a second
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    # normal to exit with ^C
    pass
