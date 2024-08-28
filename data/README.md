This directory is used for testing in the development environment.
It contains the database file and the RRD files/outputs.

For running in a container, it should be replaced with a persistent volume,
perhaps using some additional symlinkery.  Note that ./data/plot needs to be
created on the container volume.
