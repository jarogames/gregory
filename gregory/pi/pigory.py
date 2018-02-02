#!/usr/bin/python3
from gregory.pi import identpi
from gregory.pi import wlan
from gregory.pi import prerequisites as prq
from gregory.pi import setmyservice as smys

# SDDISK:
# http://www.pidramble.com/wiki/benchmarks/microsd-cards
# http://www.pidramble.com/wiki/benchmarks/microsd-cards


import subprocess as sp
import os
import argparse
###############################################
# 1. checks SSIDs current, availables
# 2. checks who am i - hostname .....
# 3. checks and installs prerequisites
#---------------------------------------
# 4. create swarm: zmq
#    . list of functioning (CAMSON,TEMP,ALIVELIST,motion)
#    . who is alive ?
#    . fullfill tasks with myservice on/off ?
#---------------------------------------
#  . ? pgp signature verification ?
#
# HARDEN?
# ufw firewall ?
#https://www.digitalocean.com/community/questions/best-practices-for-hardening-new-sever-in-2017
###############################################


#####################################
#  ARGUMENTS
#####################################
parser=argparse.ArgumentParser(description="")
parser.add_argument('-s','--show', action="store_true", help='')
parser.add_argument('--debug', action="store_true", help='')#,required=True
args=parser.parse_args()

print("\n")
print("=====================================================")
print("============ Pi Gregory.... PIGORY ==================")

####################   show all
if args.show:
    identpi.showall()
    quit()


print("==============INIT MYDATA=========================")
if not identpi.initialize_mydata():
    print("!... NOT IN LIST, quitting ...................")
    quit()
print("==============WLAN TEST=========================")
wlan.test_ssid_priorities()

########################################################
#    install prerequisites with pip3
########################################################

p=prq.check_prerequisites()  # pip3 (--user) ;  apt ???
print("i... Prerequisites needed:", p)
result=prq.install_prerequisites(p)
if len(result)>0:
    print("ERROR:...",result)
    quit()

############################################################
#  setmyservice :  perm, stop, restart (start?)
############################################################
smys.myservices( identpi.mydata["name"] )

########################################################
#    now it is possible to do whatever,  **mydata** is filled
########################################################



#  BASICALY

# 1.  check ESSID to switch (easier than from iwselect)
# 2.  check others lives
# 3.  wait for command
# 4.  report (to all) - message instantiate, display
