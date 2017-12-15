#!/usr/bin/python3
#################################
#  WLAN RELATED FUNCTIONS:
#    - find SSID of wlan
#################################
import subprocess as sp
from gregory.pi import identpi

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
    if DEBUG:print("DEBUG... current essid1="+iwcon[0])
    essid=iwcon[0].split('ESSID:')[-1].rstrip() # !!!rstrip
    if DEBUG:print("DEBUG... current essid2="+essid) # OK
    essid=essid.strip('"')
    if DEBUG:print("DEBUG... current Essid3="+essid)
    return essid


def iwselect(x):
    currssid=identpi.mydata["wlan_curr"]
    if currssid!=x:
        print("i... CONNecting to ",x,"WIFI")
    else:
        print("i... ALREADY ON",x,"wifi")


def test_ssid_priorities():
    currssid=identpi.mydata["wlan_curr"]
    print("---------- currssid---------------",currssid)
    homessid=identpi.pi_home_ssid[ identpi.mydata["name"] ]
    print("---------- home ssid---------------",homessid)
    pref1=identpi.pi_pref1_ssid[ identpi.mydata["name"] ]
    print("---------- pref1 ssid---------------",homessid)
    pref2=identpi.pi_pref2_ssid[ identpi.mydata["name"] ]
    print("---------- pref2 ssid---------------",homessid)
    print("i... === priorities in ESSID:\n   1.",
          pref1,"\n   2.",pref2,"\n   H.",homessid,"\n   C.",currssid)
    if currssid==homessid:
        if DEBUG:print("i... i am on home essid")
    else:
        print("i... NOT on home essid")
    allssids=get_visible_ssids()
    con=0
    for x in allssids:
        print("   ",x)
        if pref1==x:
            print("i... Pref1 seen:",x)
            iwselect(x)
            con=con+1
            break
        if pref2==x:
            print("i... Pref2 seen:",x)
            iwselect(x)
            con=con+1
            break
        if homessid==x:
            print("i... Home seen:",x)
            iwselect(x)
            con=con+1
            break
    if con==0:print("!... NO Connection was available")
