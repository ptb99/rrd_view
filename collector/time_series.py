#! /usr/bin/env python3

## Wrapper for the python-rrdtool package (which is a thin wrapper around
## the rrdtool CLI)

import rrdtool
import time
import os.path


class TimeSeries(object):
    """wrapper class for simple RRD storage of a few metrics"""

    def __init__(self, names):
        """Create the RRD file based on given name"""
        self.names = names
        if len(names) == 0:
            raise RuntimeError("Must provide a list of 1+ names")

        # Keep this hard-wired to 1-sec, so that the rollup charts below
        # come out to sensible values (1-min/5-min/etc)
        self.intvl=1

        # Hardcode this for simplicity
        self.filename = "./data/values.rrd"

        # we want to preserve any previous data on restarts
        if os.path.exists(self.filename):
            return

        base_args = []
        for n in names:
            base_args.append("DS:"+ n + ":GAUGE:20:U:U")
        base_args.append(
            [ "RRA:AVERAGE:0.5:1:1200",    # 20min of 1-sec
              "RRA:AVERAGE:0.5:60:2400",   # 4hr of 1-min
              "RRA:AVERAGE:0.5:300:2016",  # 7d of 5-min
              "RRA:AVERAGE:0.5:1800:1440"] # 1mon of 30-min
        )
        rrdtool.create(self.filename,
                       "--step", str(self.intvl), 
                       "--start", "{0:d}".format(int(time.time()-self.intvl)),
                       "--no-overwrite",
                       *base_args)


    def store(self, time, values):
        """Store 1 time-series point in the RRD"""
        if len(values) != len(self.names):
            raise RuntimeError("values list does not match self.names list")
        arg = "{0:d}".format(int(time))
        for val in values:
            arg = "{0:s}:{1:f}".format(arg, val)
        rrdtool.update(self.filename, arg)


if __name__ == '__main__':

    # for a test, plot load avg
    import os

    ts = TimeSeries(["load1", "load2", "load3"])

    for i in range(60):
        t = time.time()
        x = os.getloadavg()
        print("DBG: ", t, x)
        ts.store(t, x)
        time.sleep(1)
