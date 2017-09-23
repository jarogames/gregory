#!/usr/bin/env python3
#
# i have main dir. gregory. subdirectory mymod
# in setup: packages=['gregory','mymod'],
import mymod.mymod as mymod  #.py appended automatically if local
#import 
#import gps.gps

mymod.argparse_ini()
mymod.argparse_fin()
mymod.logging_ini()
mymod.logging_fin()

from mymod.mymod import logger,logger_head
from mymod.mymod import command_parser_init,command_parser_step

import os
import subprocess
import time


#from mymod import logge0,args,command_parser_init,command_parser_step
#from mymod import command_parser_init,command_parser_step

#################################
#
#  MAIN
#
#################################
if __name__ == "__main__":
    #- init command parser
    poller,receiver,collecter_data=command_parser_init()
    x=0
    while 1==1:
        #logger.info("entering parser") # wait 100ms fin c.p.step
        cmd=command_parser_step(poller,receiver,collecter_data,x)
        if len(cmd)>0:print(">",cmd)
        if cmd=="q": break
        x=x+1
