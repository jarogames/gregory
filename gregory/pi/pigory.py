#!/usr/bin/python3
import subprocess as sp
import os

print("... gregory pi....")

def get_fix_ip( name , ssid="drakula5" ):
    pinames={ "pim":   10, 
              "_pi__1":11, 
              "pi4":   12, 
              "_pi__2":13, 
              "pib":   14,
              "_pi__3":15,
              "pix2":  16,
              "pix3":  17 }
    pinames={ "pim":"mobile1", 
              "pi3":"======", 
              "pi4":"KOSTEL2", 
              "_pi__2":"=====", 
              "pib":"CAM_OUT_LEFT",
              "_pi__3":"=====",
              "pix2":"VOICE",
              "pix3":"MOBILE2" }
    print("i... get ip",name,"@",ssid)
    if name in pinames.keys():
        return "192.168.0."+str( pinames[name] )
    return "192.168.0.0"



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
    #print( "REV",rev )
    rev=rev[0].split()[-1]
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



me=whoami()
ip=get_fix_ip( me[0]  )
print("I am ", me[0] , ip )
print("     memory MB ", me[1] )
print("     CPUs      ", me[2] )
print("     revision  ", me[3] )
print("     TYPE      ", rpi_type(me[3]) )
ftagname=os.path.expanduser( "~/__"+rpi_type(me[3])+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )
