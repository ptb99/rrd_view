#!/usr/bin/env python3

## The idea here is to control the relay on a Pimoroni Automation pHat in
## order to turn the heat on/off and maintain a target temperature.

import sys
import time
import rrdtool
import RPi.GPIO as GPIO

#from ..volts.models import recipe_step


class Relay(object):
    """Wrapper for GPIO commands to control the heater relay"""

    # For pHat, there is only 1 relay, using GPIO 16
    RELAY_PIN = 16

    def __init__(self):
        # do GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT, initial=0)

    def output(self, on_off):
        # write to GPIO (invert logic, since I used the NC line)
        GPIO.output(self.RELAY_PIN, 0 if on_off else 1)


class Control(object):
    """Temp controller to turn on/off heater to maintain target temp"""

    # Time interval to update heater on/off
    TIME_INTVL = 10

    def __init__(self, recipe):
        """Create the controller instance to implement recipe"""
        self.recipe = recipe
        self.relay = Relay()


    def run(self):
        """Perdiodically check temp and adjust on/off"""
        for (dt, target) in self.recipe:

            # Record the start of current recipe step
            self.start = time.time()
            self.done = self.start + dt

            while True:
                # maybe check a flag for new recipe we need to update to?

                if self.get_temp() < target:
                    self.heater(True)
                else:
                    self.heater(False)

                time.sleep(self.TIME_INTVL)
                if time.time() > self.done:
                    break

        # Turn off the heater when the recipe is done
        self.heater(False)


    def heater(self, state):
        """Turn relay (heater) on or off"""
        print ("DBG: Control.heater(): GPIO set to ", state)
        self.relay.output(state)


    def get_temp(self):
        """Retrieve latest time-averaged temp reading"""
        vals = rrdtool.lastupdate("values.rrd")
        # maybe should use .fetch() to get a 5-min avg?
        temp = vals['ds']['temp']

        print ("DBG: Controller.get_temp():", vals['date'], temp)

        return temp


if __name__ == '__main__':

    # sample recipe for testing
    recipe = (120*60, 85.0)

    if len(sys.argv) > 2:
        recipe = (sys.argv[2], sys.argv[1])
    if len(sys.argv) == 2:
        recipe = (recipe[0], sys.argv[1])

    print ("Running Control with recipe {0:.1f} F for {1:.0f} sec".format(
        recipe[1], recipe[0]))
    c = Control([recipe])
    c.run()
