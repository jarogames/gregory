#!/usr/bin/python3
####################################
#  functions and data about identification
#  IP, localtion and other stuff for RPi
#  IP for SSIDs  of internal/home networks
#
####################################
import subprocess as sp
import os

DEBUG=True
DEBUG=False

mydata={ "name":"", "ip":"" , "desc":""}
networks={ "drakula5":"192.168.0.",
           "Lenovo PHAB2":"192.168.43."}

pinames={ "pim":   10, 
          "_pi__1":11, 
          "pi4":   12, 
          "pi3":   13, 
          "pib":   14,
          "pix1":  15,
          "pix2":  16,
          "pix3":  17,
          "pix4":  18,
          "edie":  117 }
pidesc={ "pim":"mobile1", 
          "_pi__1":"------", 
          "pi4" :"KOSTEL2", 
          "pi3" :"CAM_OUT_LEFTG",
          "pib" :"CAM_OUT_RIGHT",
          "pix1":"AUDIO_TOUCHSCR",
          "pix2":"VOICE",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"SOLAR_PANEL" ,
          "edie":"ntb"
}
pilocat={ "pim":"mobile", 
          "_pi__1":"------", 
          "pi4" :"kostel2", 
          "pi3" :"garage_attic",
          "pib" :"outside_pillar",
          "pix1":"garage",
          "pix2":"kitchen",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"garden",
          "edie":"work"
}

def is_in_networks( ssid):
    return ssid in networks.keys()

def get_pinames(pi):
    return pinames[pi]
def get_pidesc(pi):
    return pidesc[pi]
def get_pilocat(pi):
    return pilocat[pi]

def ident_fill_n_write():
    print("i... it's me, ident")
    return 0

def get_fix_ip( name , ssid="drakula5" , desc=False, loc=False):
    #print("i... get ip",name,"@",ssid)
    if desc==False and loc==False:
        #print("DEBUG2... ",  ssid, name )
        if name in pinames.keys():
            if DEBUG:print("DEBUG3... ",  ssid )
            if ssid in networks:
                prefix=networks[ssid]
            else:
                prefix="192.168.0."
            mydata["ip"]=prefix+str( pinames[name] )
            return mydata["ip"]
        return "unassigned"
    #==========
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
    mydata["name"]=hname
    
    memtot=run_cmd("cat /proc/meminfo")
    memtot=memtot.split("\n")[0].split()[1]
    memtot=int(memtot)/1024 # MB

    cpuinfo=run_cmd("cat /proc/cpuinfo")
    cpuinfo=cpuinfo.split("\n")
    ncpu=[ x for x in cpuinfo if x.find("processor")==0 ]
    if DEBUG:print("DEBUG", ncpu)
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


def showall():
    print("i... showing all")
    for i in sorted( pinames.keys() , key=pinames.get ):
        print( "{:8s} {}  {:14s} ... {}".format( i, pinames[i], pidesc[i], pilocat[i] ) )
