#! /usr/bin/env python3

## Wrapper for the python-rrdtool package (which is a thin wrapper around
## the rrdtool CLI)

import rrdtool
import time
import os.path


class time_series(object):
    """wrapper class for simple RRD storage of 1 metric"""

    def __init__(self, name, intvl=1):
        """Create the RRD file based on given name"""
        self.filename = name + ".rrd"
        # we want to preserve any previous data on restarts
        if not os.path.exists(self.filename):
            # the RRA lines actually depend on intvl, need to come up w/ logic
            rrdtool.create(self.filename, 
                       "--step", str(intvl), 
                       "--start", "{0:d}".format(int(time.time()-intvl)),
                       "--no-overwrite",
                       "DS:"+ name + ":GAUGE:20:U:U",
                       "RRA:AVERAGE:0.5:1:1200",    # 20min of 1-sec
                       "RRA:AVERAGE:0.5:60:2400",   # 4hr of 1-min
                       "RRA:AVERAGE:0.5:300:2016",  # 7d of 5-min
                       "RRA:AVERAGE:0.5:1800:1440") # 1mon of 30-min

    def store(self, time, value):
        """Store 1 time-series point in the RRD"""
        rrdtool.update(self.filename, 
                       "{0:d}:{1:f}".format(int(time), value) )




if __name__ == '__main__':

    # for a test, plot load avg
    import os

    ts = time_series("load", 1)

    for i in range(60):
        t = time.time()
        x = os.getloadavg()[0]
        print("DBG: ", t, x)
        ts.store(t, x)
        time.sleep(1)
