#!/usr/bin/python3
#################################
#  WLAN RELATED FUNCTIONS:
#    - find SSID of wlan
#################################
import os
import subprocess as sp
#from gregory.pi import config
from gregory.pi.config import mydata,pi_home_ssid,pidesc,pilocat,pinames,pi_pref1_ssid,pi_pref2_ssid

# I cannot cross ##from gregory.pi.identpi import run_cmd

import time

DEBUG=True
#DEBUG=False

def run_cmd(CMD):
    if DEBUG:print("D... running:",CMD)
    R=sp.check_output( CMD.split() )
    return R.decode("utf8").rstrip()



def get_wlans():
    if DEBUG:print("F--- get wlans: -----------------")
    CMD="/sbin/ifconfig"
    ifcon=sp.check_output( CMD ).decode("utf8").split("\n")
    wlans=[ x for x in ifcon if x.find("Link encap:Ethernet")>0 ]
    #if DEBUG: print("DEBUG... wlans", wlans)
    wlans=[ x.split()[0] for x in wlans if x[0]=="w" ] # ONLY WIFI
    return wlans

def eliminate_wlans():
    if DEBUG:print("eliminate ???????????")
    return

def get_visible_ssids():
    if DEBUG:print("F--- get visible eesids: ------------")
    wlans=get_wlans()
    if len(wlans)>1:
        eliminate_wlan0() # only one wlan iface available
        wlans=get_wlans()
    CMD="/sbin/iwlist "+wlans[0]+" scan"
    iwcon=sp.check_output( CMD.split() ).decode("utf8").split("\n")
    essids=[x for x in iwcon if x.find("ESSID:")>0]
    essids=[x.split(":")[-1].strip('"') for x in essids]
    #if DEBUG:print("DEBUG... visible essids: ",essids)
    if DEBUG:
        print("i... get visible eesids:" , end="")
        print(essids)
    return essids
    

def get_current_ssid():
    if DEBUG:print("F--- get current ssid  ----------------")
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




def iwselect(x , ip ):
    if DEBUG:print("F--- iwselect ",x,"ip=",ip," --------------")
    currssid=mydata["wlan_curr"]
    if currssid!=x:
        print("i... CONNecting to ",x,"WIFI")
        passfile="/etc/wpa_supplicant/"+x+".conf"
        print("i... checking ",passfile)
        if not os.path.isfile( passfile ):
            print("!... NO ",passfile,"  ... returns")
            return
        ####### MUST BE ON RPI ###########
        CMD="sudo kill wpa_supplicant"
        run_cmd( CMD )
        CMD="sudo ifdown wlan"
        run_cmd( CMD )
        CMD='sudo wpa_supplicant -Dwext -wlan0 -c "'+passfile+'"'
        time.sleep(3)
        CMD="sudo ifup wlan0"
        run_cmd( CMD )
        CMD="sudo ifconfig wlan0 "+ip+" up"
        run_cmd( CMD )
    else:
        print("i... ALREADY ON",x,"wifi")




    
def test_ssid_priorities():
    if DEBUG:print("F--- test_ssid_priorities --------------")
    currssid=mydata["wlan_curr"]
    if DEBUG:print("---------- currssid---------------",currssid)
    homessid=pi_home_ssid[ mydata["name"] ]
    if DEBUG:print(".... home ssid  ",homessid)
    pref1=pi_pref1_ssid[ mydata["name"] ]
    if DEBUG:print(".... pref1 ssid ",pref1)
    pref2=pi_pref2_ssid[ mydata["name"] ]
    if DEBUG:print(".... pref2 ssid ",pref2)
    print("i... === priorities in ESSID:\n   1.",
          pref1,"\n   2.",pref2,"\n   H.",homessid,"\n   C.",currssid)
    if currssid==homessid:
        if DEBUG:print("i... i am on home essid")
    else:
        print("i... NOT on home essid")
    allssids=get_visible_ssids()
    connect_to=""
    connect_ip=""
    print("s...  searching in ",allssids )
    for x in allssids:
        if len(homessid)>0 and homessid[0]==x:
            print("i... Home seen:",x)
            connect_to=x
            connect_ip=homessid[1]
    for x in allssids:
        if len(pref2)>0 and pref2[0]==x:
            print("i... Pref2 seen:",x)
            connect_to=x
            connect_ip=pref2[1]
    for x in allssids:
        if len(pref1)>0 and pref1[0]==x:
            print("i... Pref1 seen:",x)
            connect_to=x
            connect_ip=pref1[1]
    iwselect( connect_to , connect_ip)
    
    if connect_to=="":print("!... NO Connection was available")
