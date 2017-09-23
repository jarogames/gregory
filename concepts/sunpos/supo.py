#!/usr/bin/python3
from pylab import *
from sunposition import observed_sunpos
from datetime import datetime

#evaluate on a 2 degree grid
#lon  = linspace(-180,180,181)
#lat = linspace(-90,90,91)
#LON, LAT = meshgrid(lon,lat)
#at the current time
LAT=37.6287
LON=15.1749
now = datetime.utcnow()
res = observed_sunpos(now,LAT,LON,0)[:2] #discard RA, dec, H
print(res[0])
