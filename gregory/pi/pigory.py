#!/usr/bin/python3
import subprocess as sp
import os
import argparse

DEBUG=True
DEBUG=False

print("... gregory pi....")

parser=argparse.ArgumentParser(description="")
parser.add_argument('-s','--show', action="store_true", help='')
parser.add_argument('--debug', action="store_true", help='')#,required=True
args=parser.parse_args()


pinames={ "pim":   10, 
          "_pi__1":11, 
          "pi4":   12, 
          "pi3":   13, 
          "pib":   14,
          "pix1":  15,
          "pix2":  16,
          "pix3":  17,
          "pix4":  18 }
pidesc={ "pim":"mobile1", 
          "_pi__1":"------", 
          "pi4" :"KOSTEL2", 
          "pi3" :"CAM_OUT_LEFTG",
          "pib" :"CAM_OUT_RIGHT",
          "pix1":"AUDIO_TOUCHSCR",
          "pix2":"VOICE",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"SOLAR_PANEL" 
}
pilocat={ "pim":"mobile", 
          "_pi__1":"------", 
          "pi4" :"kostel2", 
          "pi3" :"garage_attic",
          "pib" :"outside_pillar",
          "pix1":"garage",
          "pix2":"kitchen",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"garden" 
}


def get_fix_ip( name , ssid="drakula5" , desc=False, loc=False):
    #print("i... get ip",name,"@",ssid)
    if desc==False and loc==False:
        if name in pinames.keys():
            return "192.168.0."+str( pinames[name] )
        return "unassigned"
    if desc:
        if name in pidesc.keys():
            return pidesc[name]
        return "unknown"
    if loc:
        if name in pilocat.keys():
            return pilocat[name]
        return "somewhere"



def run_cmd(CMD):
    print("x... running:",CMD)
    R=sp.check_output( CMD.split() )
    return R.decode("utf8").rstrip()

def whoami():
    print("i... who am i : ")
    hname=run_cmd("hostname")
    memtot=run_cmd("cat /proc/meminfo")
    memtot=memtot.split("\n")[0].split()[1]
    memtot=int(memtot)/1024 # MB

    cpuinfo=run_cmd("cat /proc/cpuinfo")
    cpuinfo=cpuinfo.split("\n")
    ncpu=[ x for x in cpuinfo if x.find("processor")>=0 ]
    ncpu=int(ncpu[-1].split()[-1] )+1
    rev=[ x for x  in cpuinfo if x.find("Revision")>=0 ]
    if DEBUG:print( "Revision",rev )
    if len(rev)>0:
        rev=rev[0].split()[-1]
    else:
        rev="unknown_rev"
    return hname,memtot,ncpu,rev


def rpi_type( rev ):
    if rev=="a22082": return "Pi3B_china"
    if rev=="a02082": return "Pi3B_UK"
    if rev=="9000C1": return "PiZeroW"
    if rev=="a01041": return "Pi2B_1.1_UK"
    if rev=="a21041": return "Pi2B_1.1_china"
    if rev=="0015": return "PiA+"
    if rev=="900032": return "PiB+"
    if rev=="0010": return "PiB+"
    if rev=="0013": return "PiB+"
    return "unknown_type"
#    if cpu==4 and mem>512:
#        if 1==1: return "pi2B"
#        if 1==2: return "pi3B"



###########   show
if args.show:
    print("i... showing all")
    for i in sorted( pinames.keys() , key=pinames.get ):
        print( "{:8s} {}  {:14s} ... {}".format( i, pinames[i], pidesc[i], pilocat[i] ) )
    quit()

    
    
me=whoami()
ip=get_fix_ip( me[0] , ssid="drakula5" )
desc=get_fix_ip( me[0], desc=True )
loca=get_fix_ip( me[0], loc=True )
print("I am ", me[0] )
print("     IP         :", ip)
print("     description:", desc)
print("     location   :", loca)
print("     memory MB   ", me[1] )
print("     CPUs        ", me[2] )
print("     revision    ", me[3] )
print("     TYPE        ", rpi_type(me[3]) )

ftagname=os.path.expanduser( "~/z1__"+me[0]+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )

ftagname=os.path.expanduser( "~/z2__"+rpi_type(me[3])+"__" )
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
