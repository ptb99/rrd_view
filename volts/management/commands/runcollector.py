from django.core.management.base import BaseCommand

import subprocess


class Command(BaseCommand):
    help = 'run the collector script to log data into the RRD file'

    # Note: this will typically be a symlink to the real script
    script = "./collector/collector.py"

    def handle(self, *args, **options):
        cmd = "nohup {0} 2>&1 >/dev/null".format(self.script)
        subprocess.Popen(cmd, shell=True)
