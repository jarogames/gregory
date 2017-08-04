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
#import threading
import threading
#####import context
import zmq

#from mymod import logge0,args,command_parser_init,command_parser_step
from mymod import command_parser_init,command_parser_step

## From gps_socket (my) global variable should be loaded.
from gps_socket import translate_gps_line, gps_info

import keypress 
#################################
# procedures for threading:
#################################
def gps_poll():
    context =  zmq.Context.instance()
    # receive from master
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://gps_poll")
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    #string = receiver.recv()
    logger.info("in     gps_poll thread")
    while (1==1):
        #time.sleep(0.1)
        translate_gps_line()
        event = poller.poll(100)
        if event:
            string=receiver.recv()
        else:
            string=""
        #logger.info(string)
        if string==b'q':break
    logger.error("OUT of gps_poll thread")
    return


def kpress():
    context =  zmq.Context.instance()
    # receive from master
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://kpress_poll")
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    #string = receiver.recv()
    logger.info("in     kpress_poll thread (i cannot exit now!!!)")
    #### THE BIG LOOP================
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://127.0.0.1:5558")
    regs=0
    while (1==1):
        #time.sleep(0.1)
        keypress.producer_onestep(zmq_socket,True,True,regs)
        regs=1
        event = poller.poll(100)
        if event:
            string=receiver.recv()
        else:
            string=""
        #logger.info(string)
        if string==b'q':break
    logger.error("OUT of kpress_poll thread")
    return
#################################
#
#  MAIN
#
#################################
if __name__ == "__main__":
    # Prepare our context and sockets
    context = zmq.Context.instance()
    s_gps = context.socket(zmq.PAIR)
    s_gps.bind("inproc://gps_poll")
    context2 = zmq.Context.instance()
    s_key = context2.socket(zmq.PAIR)
    s_key.bind("inproc://kpress_poll")
    ############################## what should be initialized
    #                            # DO NOW:
    ### 1st thread - i would love to poll USB and fill GPS
    #   global variable
    t_gps_poll = threading.Thread(target=gps_poll)
    t_gps_poll.start()
    keypress.consumer_id=0
    t_keypress = threading.Thread(target=kpress)
    t_keypress.start()
    ################## - init command parser
    poller,receiver,collecter_data=command_parser_init()
    x=0
    ######### here all commands will pass in an infinite loop 
    while 1==1:
        # STATUS LINE HERE
        if gps_info['fix']=='+' and gps_info['dist']>0.:
            print(' '+gps_info['fix']+gps_info['timex']+
              " ({:6.4f},{:6.4f}){:6.1f} km/h {:6.1f} m H{:03.0f}  {:.1f}        ".format( gps_info['XCoor'],gps_info['YCoor'],gps_info['speed']*1.852,gps_info['altitude'],gps_info['course'],  gps_info['dist']*1000  ) ,end='\r')
            #here-  some distance was made from the last call
        else:
            print( "{} ".format(gps_info['fix']) , end="\r")


        #logger.info("entering parser") # wait 100ms fin c.p.step
        cmd=command_parser_step(poller,receiver,collecter_data,x)
        if len(cmd)>0:print(">",cmd)
        if cmd!="":s_gps.send_string(cmd)
        if cmd!="":s_key.send_string(cmd)
        if cmd=="q": break
        x=x+1
    #t_gps_poll.exit()
    #t_keypress.exit()
