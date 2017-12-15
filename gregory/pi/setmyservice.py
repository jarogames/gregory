#!/usr/bin/python3

from gregory.pi.config import pi_myservice
from gregory.pi.identpi import run_cmd

DEBUG=True
#DEBUG=False


# this is independent on network ...
def myservices( me ):
    print("F--- MYSERVICE ---------------------------")
    mydict=pi_myservice[ me ]
    if DEBUG: print("i... myservices for", me, mydict )
    for k,v in mydict.items():
        CMD="myservice "+k+" "+v
        print("i... ",CMD )
        out=run_cmd( CMD ) # check_output
        if DEBUG:print("i...",out)
