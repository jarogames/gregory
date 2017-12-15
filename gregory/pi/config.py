########## HERE SHOULD BE ALL ABOUT ME #####
# HOME NETWORK  drakula + ip
# preffered network 1   + ip
# preffered network 2   + ip
mydata={ "name":"",
         "ip":"" ,
         "desc":"",
         "loc":"",
         "PiType":"",
         "wlan_curr":""}


# fixed IPs for predefined networks
#networks={ "drakula5":"192.168.0.",
#           "Lenovo PHAB2":"192.168.43."
#          }



pinames={ "pim":   "10", 
          "_pi__1":"11", 
          "pi4":   "12", 
          "pi3":   "13", 
          "pib":   "14",
          "pix1":  "15",
          "pix2":  "16",
          "pix3":  "17",
          "pix4":  "18",
          "fedo":  "117"
}

homessid="drakula5"
pi_home_ssid={ "pim":   [homessid,"192.168.0."+pinames["pim"]], 
               "_pi__1":[homessid,"192.168.0."+pinames["_pi__1"]],
               "pi4":   [homessid,"192.168.0."+pinames["pi4"]],
               "pi3":   [homessid,"192.168.0."+pinames["pi3"]], 
               "pib":   [homessid,"192.168.0."+pinames["pib"]],
               "pix1":  [homessid,"192.168.0."+pinames["pix1"]],
               "pix2":  [homessid,"192.168.0."+pinames["pix2"]],
               "pix3":  [homessid,"192.168.0."+pinames["pix3"]],
               "pix4":  [homessid,"192.168.0."+pinames["pix4"]],
               "fedo":  [homessid,"192.168.0."+pinames["fedo"]]
}

prefssid1="Lenovo PHAB2"
pi_pref1_ssid={ "pim":  [prefssid1,"192.168.43."+pinames["pim"]],  
               "_pi__1":[prefssid1,"192.168.43."+pinames["_pi__1"]],
               "pi4":   [prefssid1,"192.168.43."+pinames["pi4"]],
               "pi3":   [],
               "pib":   [],
               "pix1":  [],
               "pix2":  [],
               "pix3":  [prefssid1,"192.168.43."+pinames["pix3"]],  
               "pix4":  [prefssid1,"192.168.43."+pinames["pix4"]],  
               "fedo":  []
#               "fedo":  ["Magor","192.168.0.111"]
}


prefssid2="jerg_hack"
pi_pref2_ssid={ "pim":  [prefssid2,"192.168.43."+pinames["pim"]],   
               "_pi__1":[prefssid2,"192.168.43."+pinames["_pi__1"]],
               "pi4":   [prefssid2,"192.168.43."+pinames["pi4"]],
               "pi3":   [],
               "pib":   [],
               "pix1":  [],
               "pix2":  [],
               "pix3":  [prefssid2,"192.168.43."+pinames["pix3"]],  
               "pix4":  [prefssid2,"192.168.43."+pinames["pix4"]],  
               "fedo":  []
}


pidesc={ "pim":"mobile1", 
          "_pi__1":"------", 
          "pi4" :"KOSTEL2", 
          "pi3" :"CAM_OUT_LEFTG",
          "pib" :"CAM_OUT_RIGHT",
          "pix1":"AUDIO_TOUCHSCR",
          "pix2":"VOICE",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"SOLAR_PANEL" ,
          "fedo":"gigabyte"
}


pilocat={ "pim":"mobile", 
          "_pi__1":"------", 
          "pi4" :"kostel2", 
          "pi3" :"garage_attic",
          "pib" :"outside_pillar",
          "pix1":"garage",
          "pix2":"kitchen",
          "pix3":"MOBILE_CAM_2" ,
          "pix4":"garden",
          "fedo":"home"
}

# this should be run in update
pi_myservice={ "pim": {}, 
          "_pi__1":{}, 
          "pi4":   {}, 
          "pi3":   {}, 
          "pib":   {},
          "pix1":  {},
          "pix2":  {},
          "pix3":  {"CAMSON20":"perm"},
          "pix4":  {},
          "fedo":  {"test":"start"}
}



