#!/usr/bin/python3

from gregory.pi import identpi  # pi_myservice

DEBUG=True
#DEBUG=False


# this is independent on network ...
def myservices( me ):
    print("F--- MYSERVICE ---------------------------")
    mydict=identpi.pi_myservice[ me ]
    if DEBUG: print("i... myservices for", me, mydict )
    for k,v in mydict.items():
        CMD="myservice "+k+" "+v
        print("i... ",CMD )
        out=identpi.run_cmd( CMD ) # check_output
        if DEBUG:print("i...",out)
