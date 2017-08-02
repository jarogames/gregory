#!/usr/bin/env python3
import mymod  #.py appended automatically

mymod.argparse_ini()
mymod.argparse_fin()
mymod.logging_ini()
mymod.logging_fin()
from mymod import logger,logger_head


import os
import subprocess
import time


#from mymod import logge0,args,command_parser_init,command_parser_step
from mymod import command_parser_init,command_parser_step

#################################
#
#  MAIN
#
#################################
if __name__ == "__main__":
    #logge0.info('====== START argument=%s ====',args.book)  # start LOG file
    #- init command parser
    poller,receiver,collecter_data=command_parser_init()
    x=0
    while 1==1:
        #logger.info("entering parser")
        cmd=command_parser_step(poller,receiver,collecter_data,x)
        if len(cmd)>0:print(">",cmd)
        if cmd=="q": break
        x=x+1
