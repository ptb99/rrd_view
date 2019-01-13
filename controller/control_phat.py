#!/usr/bin/env python3

## The idea here is to control the relay on a Pimoroni Automation pHat in
## order to turn the heat on/off and maintain a target temperature.

import sys
import time
import itertools
import rrdtool
import RPi.GPIO as GPIO



class Recipe(object):
    """Series of Temperature and Duration steps"""
    def __init__(self, args):
        assert(len(args) > 0)
        self.vals = itertools.zip_longest(args[::2], args[1::2])

    def values(self):
        """Return the iterator to our list of pairs (temp,dur)"""
        return self.vals


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
        # write to GPIO
        GPIO.output(self.RELAY_PIN, 1 if on_off else 0)


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
        for (target, dt) in self.recipe.values():

            # Record the start of current recipe step
            self.start = time.time()
            # if dt for recipe step is None, then go forever
            if dt:
                self.done = self.start + float(dt)
            else:
                self.done = None

            while True:
                # maybe check a flag for new recipe we need to update to?

                if self.get_temp() < float(target):
                    self.heater(True)
                else:
                    self.heater(False)

                time.sleep(self.TIME_INTVL)
                if self.done and time.time() > self.done:
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

    if len(sys.argv) < 2:
        # sample recipe for testing
        recipe = Recipe([85.0, 60*60])
    else:
        recipe = Recipe(sys.argv[1:])

    ## recipe.values() iterator is a 1-pass - need to fix this
    # print ("Running with recipe:")
    # for (temp, dur) in recipe.values():
    #     print("  {0:.1f} F for {1:.0f} sec".format(float(temp),float(dur)))

    c = Control(recipe)
    c.run()
