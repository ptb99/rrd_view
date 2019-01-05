#!/usr/bin/env python3

## This reads an MCP3008 ADC attached to a TMP36 sensor using the library
## from Adafruit (https://github.com/adafruit/Adafruit_Python_MCP3008)


import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from time_series import TimeSeries


# switch between HW SPI pins vs SW bit-banged gen-purpose pins
use_hw_spi = True

# SPI pins in SW mode
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25



def voltage(adc):
    """Convert 10-bit ADC integer value to a voltage"""
    MAX = 1023
    REF = 3.3 # volts
    return float(adc)/MAX * REF


def temp(volt):
    """Convert analog voltage to temperature in C"""
    # TMP36 reads 0V at -50C and 2V at +150C
    return 100*volt - 50


# which channel to read
TARGET_ADC = 0

# our sampling time in secs
INTERVAL = 1.0


if use_hw_spi:
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))
else:
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

ts = TimeSeries(["voltage", "temp"])
print("\nPress CTRL+C to exit.\n")

try:
    while True:
        # read the analog pin
        value = mcp.read_adc(TARGET_ADC)
        volt = voltage(value)
        temp_C = temp(volt)
        temp_F = 9*temp_C/5 + 32

        t = time.time()

        form = 't={time:.3f} - val= {volt:.3f} V  ==  {temp:.3f} C / {temp_F:.3f} F'
        print (form.format(time=t, volt=volt, temp=temp_C, temp_F=temp_F))

        ts.store(t, [volt, temp_F])

        # hang out and do nothing for a second
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    # normal to exit with ^C
    pass
