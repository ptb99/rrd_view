from django.core.management.base import BaseCommand

import time
import random
import rrdtool


class Command(BaseCommand):
    help = 'Create a dummy RRD file for testing purposes'

    def handle(self, *args, **options):
        # params
        filename = "./data/values.rrd"
        base = 12.0
        amplitude = 0.5
        num_secs = 2 * 3600     # 2 hrs
        end = int(time.time())
        start = end - num_secs

        # create voltage.rrd
        rrdtool.create(filename,
                       "--step", "1",
                       "--start", "{0:d}".format(start),
                       "DS:volts:GAUGE:20:U:U",
                       "RRA:AVERAGE:0.5:1:1200",    # 20min of 1-sec
                       "RRA:AVERAGE:0.5:60:2400",   # 4hr of 1-min
                       "RRA:AVERAGE:0.5:300:2016",  # 7d of 5-min
                       "RRA:AVERAGE:0.5:1800:1440") # 1mon of 30-min

        # fill with points
        for i in range(num_secs):
            v = base + random.uniform(-1*amplitude, amplitude)
            rrdtool.update(filename, "{0:d}:{1:f}".format(int(start)+i+1, v) )
