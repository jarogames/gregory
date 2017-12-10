#!/usr/bin/python3
import subprocess as sp

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
    return hname,memtot,ncpu

def rpi_type( cpu,mem):
    if cpu==4 and mem>512:
        if 1==1: return "pi2B"
        if 1==2: return "pi3B"

me=whoami()
print("I am ", me[0] )
print("     memory MB ", me[1] )
print("     CPUs      ", me[2] )
print("I am ", me[0] )
