#!/usr/bin/python3
import subprocess as sp
import os

print("i... gregory pi....")


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
print("I am ", me[0] )
print("     memory MB ", me[1] )
print("     CPUs      ", me[2] )
print("     revision  ", me[3] )
print("     TYPE      ", rpi_type(me[3]) )
ftagname=os.path.expanduser( "~/__"+rpi_type(me[3])+"__" )
with open( ftagname ,"w" ) as f:
    f.write( " ".join( str(me) ) )
