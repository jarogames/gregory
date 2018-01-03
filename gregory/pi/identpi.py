#!/usr/bin/python3
####################################
#  functions and data about identification
#  IP, localtion and other stuff for RPi
#  IP for SSIDs  of internal/home networks
#
####################################
from gregory.pi import wlan
from gregory.pi.config import mydata,pi_home_ssid,pidesc,pilocat,pinames
import subprocess as sp
import os

DEBUG=True
#DEBUG=False





#def is_in_networks( ssid):
#    return ssid in networks.keys()

def get_pinames(pi):
    return pinames[pi]
def get_pidesc(pi):
    return pidesc[pi]
def get_pilocat(pi):
    return pilocat[pi]

#def ident_fill_n_write():
#    print("i... it's me, ident")
#    return 0

def get_desc( name ):
    if name in pidesc.keys():
        return pidesc[name]
    return "unknown"

def get_loc( name ):
    if name in pilocat.keys():
        return pilocat[name]
    return "somewhere"



def get_fix_ip( name , ssid="drakula5" ):
    if DEBUG:print("i... get ip",name,"@ /",ssid,"/")
    #print("DEBUG2... ",  ssid, name )
    if name in pi_home_ssid.keys():
        if DEBUG:print("DEBUG3... ",ssid,";home=",pi_home_ssid[name])
        if ssid==pi_home_ssid[name][0]: # is ssid
            return pi_home_ssid[name][1]
    return "unavailable"
    #==========



def run_cmd(CMD):
    if DEBUG:print("D... running:",CMD)
    R=sp.check_output( CMD.split() )
    return R.decode("utf8").rstrip()

def whoami():
    print("i... who am i -------------------------- ")
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









def write_z_file( num, text ):
    ftagname=os.path.expanduser( "~/z"+str(num)+"__"+text+"__" )
    with open( ftagname ,"w" ) as f:
        f.write( text )

def initialize_mydata():
    print("i... initialization mydata ...")
    ################################ NOW WLAN  ########
    curssid=wlan.get_current_ssid( )
    mydata["wlan_curr"]=curssid      # MYDATA
    ################################ NOW ID ##########
    me=whoami()  # must: fills mydata[]
    #ip=get_fix_ip( me[0] , ssid="drakula5" )
    mydata["name"]=me[0]
    mydata["ip"]=get_fix_ip( me[0], ssid=mydata["wlan_curr"] )
    mydata["desc"]=get_desc( me[0])
    mydata["loc"]=get_loc(me[0] )
    mydata["PiType"]=rpi_type(me[3])
    print("I am ",  mydata["name"] )
    print("     IP         :", mydata["ip"])
    print("     OnWlan     :", mydata["wlan_curr"])
    print("     description:", mydata["desc"])
    print("     location   :", mydata["loc"])
    print("     memory MB   ", me[1] )
    print("     CPUs        ", me[2] )
    print("     revision    ", me[3] )
    print("     TYPE        ", mydata["PiType"] )
    if not me[0] in pinames:return False
    write_z_file( 1, mydata["name"])
    write_z_file( 2, mydata["PiType"])
    #write_z_file( 3, mydata["name"]) # ipzero?
    write_z_file( 4, mydata["desc"])
    write_z_file( 5, mydata["loc"])

    return True

    
def showall():
    print("i... showing all")
    for i in sorted( pinames.keys() , key=pinames.get ):
        print( "{:8s} {}  {:14s} ... {}".format( i, pinames[i], pidesc[i], pilocat[i] ) )


        
