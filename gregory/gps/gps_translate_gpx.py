#!/usr/bin/python3
import os

FILE='amien_track.gpx'

import sys

print( 'Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))

if len(sys.argv)>1:
    FILE=str(sys.argv[1])
else:
    FILE='GraphHopper.gpx'

with open(FILE, 'r') as f:
    list=f.read().split('\n')

list2=[ x for x in list if x.find('lat')>0]


with open( os.path.splitext( FILE )[0]+".log", "w") as ff:
    for i in list2:
        if len(i.split())>2:
            y,x=i.split()[1].split('"')[1],i.split()[2].split('"')[1]
            LINE="00:00:00 UTC {} {} 0.0 km/h 0 m H000 0.0\n".format(x,y)
            print(LINE , end="")
            ff.write( LINE)
            
with open( "gps_target.log", "w") as ff:
    for i in list2:
        if len(i.split())>2:
            y,x=i.split()[1].split('"')[1],i.split()[2].split('"')[1]
            LINE="00:00:00 UTC {} {} 0.0 km/h 0 m H000 0.0\n".format(x,y)
            #print(LINE , end="")
            ff.write( LINE)
