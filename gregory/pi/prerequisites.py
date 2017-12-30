#!/usr/bin/python3

import subprocess as sp
import os   # devnul 

DEBUG=True

packages={}
####   WHAT I CONSIDER CRUCIAL FOR RPI ##################
packages['blessings']='from blessings import Terminal ... color terminal, moving cursor'
packages['prettytable']='ASCII pretty tables'
packages['matplotlib']='import matplotlib.pyplot as plt'
packages['numpy']='import numpy as np'
packages['pandas']='import pandas as pd'
packages['pyserial']='? serial read, arduino...?'
packages['pyzmq']='! also aptitude install libzmq5 libczmq3'
packages['serf_master']='serf package python module'
# packages['xvbfwrapper']=''
# packages['zenipy']=''
# packages['youtube-dl']=''
# packages['mps-youtube']=''
# packages['staticmap']=''
# packages['scipy']=''
# packages['iminuit']=''
# packages['h5py?']=''
# packages['Flask']=''
# packages['imutils']='opencv image transforms'
# packages['logzero']=''
# packages['lxml']=''
# packages['pexpect']='commandline child communication (ftp...)'
# packages['Pillow']='python image lib, fork'
# packages['svgwrite']='SVG drawing module'
# packages['pyswarm']='particle swarm optimization w.constraints/pyswarms'
# packages['']=''
# packages['']=''
# packages['']=''



def check_prerequisites():
    if DEBUG:print("F--- Prerequisites: -------------------")
    CMD="pip3 list --format=legacy"  # pip 9.0.1 starts to complain
    CMD="pip3 list"                  # pip 1.5 doesnt know --format
    all=sp.check_output( CMD.split() ).decode("utf8").rstrip().split("\n")
    #print(all)
    all=[ x.split()[0] for x in all ]
    #print(all)
    needed=[]
    for p in packages.keys():
        if DEBUG:print("ck ... {:15s} ...".format(p),end="")
        if p in all:
            if DEBUG:print("[OK]")
        else:
            if DEBUG:print("[!!]")
            needed.append(p)
            #################  FANTSTIC  ERROR CODE CHECK ######
        # FNULL=open( os.devnull,"w")
        # try:
        #     res=sp.check_call( CMD.split() , stdout=FNULL )
        # except sp.CalledProcessError:
        #     print("PAC...",p,"...",packages[p])
        #     needed.append( p )
        # #if DEBUG:print(":... {}".format(p) )
    return needed


def install_prerequisites( prers ):
    errors=[]
    for p in prers:
        CMD="pip3 install "+p+" --user"
        if DEBUG:print("D...",CMD)
        try:
            res=sp.check_call( CMD.split() )
        except sp.CalledProcessError:
            print("ERR...",p,"...",packages[p])
            errors.append( p )
        if DEBUG:print("ERRORS:",errors)
    return errors
