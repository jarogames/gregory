#!/usr/bin/python3
#################################
#  WLAN RELATED FUNCTIONS:
#    - find SSID of wlan
#################################
import subprocess as sp
DEBUG=True
DEBUG=False

def get_wlans():
    CMD="/sbin/ifconfig"
    ifcon=sp.check_output( CMD ).decode("utf8").split("\n")
    wlans=[ x for x in ifcon if x.find("Link encap:Ethernet")>0 ]
    #if DEBUG: print("DEBUG... wlans", wlans)
    wlans=[ x.split()[0] for x in wlans if x[0]=="w" ] # ONLY WIFI
    return wlans

def eliminate_wlans():
    print("???????????")
    return

def get_visible_ssids():
    wlans=get_wlans()
    if len(wlans)>1:
        eliminate_wlan0() # only one wlan iface available
        wlans=get_wlans()
    CMD="/sbin/iwlist "+wlans[0]+" scan"
    iwcon=sp.check_output( CMD.split() ).decode("utf8").split("\n")
    essids=[x for x in iwcon if x.find("ESSID:")>0]
    essids=[x.split(":")[-1].strip('"') for x in essids]
    if DEBUG:print("DEBUG... visible essids: ",essids)
    return essids
    

def get_current_ssid():
    wlans=get_wlans()
    if len(wlans)>1:
        eliminate_wlan0() # only one wlan iface available
        wlans=get_wlans()
    CMD="/sbin/iwconfig "+wlans[0]
    iwcon=sp.check_output( CMD.split() ).decode("utf8").split("\n")
    essid=iwcon[0].split()[-1].split(":")[-1]
    essid=essid.strip('"')
    if DEBUG:print("DEBUG... essid="+essid)
    return essid
    
