#!/usr/bin/python3
from gregory.pi import identpi
from gregory.pi import wlan
import subprocess as sp
import os
import argparse

#####################################
#  ARGUMENTS
#####################################
parser=argparse.ArgumentParser(description="")
parser.add_argument('-s','--show', action="store_true", help='')
parser.add_argument('--debug', action="store_true", help='')#,required=True
args=parser.parse_args()



####################   show all
if args.show:
    identpi.showall()
    quit()

####################   find ssid ### GO THROUGH
curssid=wlan.get_current_ssid( )
ssidok=identpi.is_in_networks( curssid )
print( "i... i am on a known {:14s} wifi network ... {}".format(curssid,ssidok) )
allssids=wlan.get_visible_ssids()
for x in allssids:
    ssidok=identpi.is_in_networks( x )
    print( "i... visible wifi    {:14s} is known     ... {}".format(x,ssidok) )

    
####################    ME #  FILL ALL # MAKE FILES ######
me=identpi.whoami()  # must: fills mydata[]
ip=identpi.get_fix_ip( me[0] , ssid="drakula5" )
desc=identpi.get_fix_ip( me[0], desc=True )
loca=identpi.get_fix_ip( me[0], loc=True )
rpitype=identpi.rpi_type(me[3])
print("I am ", me[0] )
print("     IP         :", ip)
print("     description:", desc)
print("     location   :", loca)
print("     memory MB   ", me[1] )
print("     CPUs        ", me[2] )
print("     revision    ", me[3] )
print("     TYPE        ", rpitype )

ftagname=os.path.expanduser( "~/z1__"+me[0]+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )

ftagname=os.path.expanduser( "~/z2__"+rpitype+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )

ftagname=os.path.expanduser( "~/z3__"+ip+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )

ftagname=os.path.expanduser( "~/z4__"+desc+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )

ftagname=os.path.expanduser( "~/z5__"+loca+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )


########################################################
#    now it is possible to do whatever,  **mydata** full
########################################################

 
